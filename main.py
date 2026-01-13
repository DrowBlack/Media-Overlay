import customtkinter as ctk
from PIL import Image, ImageTk
import winsdk.windows.media.control as wmc
from winsdk.windows.storage.streams import DataReader
import asyncio
import threading
import math
import time
import io

# --- CONFIGURATION ---
WINDOW_W = 340
WINDOW_H = 100
POS_X = 20
POS_Y = 80
TIMEOUT_SECONDS = 4
FADE_SPEED = 0.08
TRANS_COLOR = "#000001" 
# --------   ----------

class MediaOverlay(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.attributes('-alpha', 0.0) 
        
        self.configure(fg_color=TRANS_COLOR)
        self.attributes('-transparentcolor', TRANS_COLOR)
        
        self.geometry(f"{WINDOW_W}x{WINDOW_H}+{POS_X}+{POS_Y}")

        self.main_frame = ctk.CTkFrame(
            self, 
            fg_color="#090321", 
            bg_color=TRANS_COLOR, 
            border_width=1, 
            border_color="white", 
            corner_radius=8  
        )
        self.main_frame.pack(fill="both", expand=True)
        
        # Grid Düzeni
        self.main_frame.grid_columnconfigure(0, weight=0)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.cover_label = ctk.CTkLabel(self.main_frame, text="", width=80, height=80)
        self.cover_label.grid(row=0, column=0, padx=12, pady=8, sticky="ns")

        self.info_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.info_frame.grid(row=0, column=1, padx=(0, 15), pady=10, sticky="nsew")

        self.title_lbl = ctk.CTkLabel(self.info_frame, text="Waiting...", font=("Segoe UI", 15, "bold"), text_color="white", anchor="w")
        self.title_lbl.pack(fill="x", pady=(2,0))

        self.artist_lbl = ctk.CTkLabel(self.info_frame, text="", font=("Segoe UI", 12), text_color="#bbbbbb", anchor="w")
        self.artist_lbl.pack(fill="x")

        self.wave_canvas = ctk.CTkCanvas(self.info_frame, height=25, bg="#090321", highlightthickness=0)
        self.wave_canvas.pack(fill="x", side="bottom", pady=(5, 5))

        self.current_song_id = None
        self.last_playing_status = None
        self.show_until = 0
        self.current_alpha = 0.0
        self.target_alpha = 0.0
        
        self.duration = 1
        self.position = 0
        self.phase = 0
        self.is_playing = False
        
        self.fade_loop()

    def update_metadata(self, title, artist, duration, position, is_playing, thumb_data):
        new_id = f"{title}-{artist}"
        status_changed = (is_playing != self.last_playing_status)
        song_changed = (new_id != self.current_song_id)

        if song_changed or status_changed:
            self.current_song_id = new_id
            self.last_playing_status = is_playing
            
            self.show_until = time.time() + TIMEOUT_SECONDS
            self.target_alpha = 1.0
            self.deiconify()
            
            if len(title) > 22: title = title[:22] + "..."
            self.title_lbl.configure(text=title)
            self.artist_lbl.configure(text=artist)
            
            if song_changed:
                if thumb_data:
                    try:
                        img = Image.open(io.BytesIO(thumb_data))
                        img = img.resize((70, 70))
                        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(70, 70))
                        self.cover_label.configure(image=ctk_img)
                    except:
                        self.cover_label.configure(image=None)
                else:
                    self.cover_label.configure(image=None)

        self.duration = duration
        self.position = position
        self.is_playing = is_playing
        
        if time.time() > self.show_until:
            self.target_alpha = 0.0

    def fade_loop(self):
        if abs(self.current_alpha - self.target_alpha) > 0.01:
            if self.current_alpha < self.target_alpha:
                self.current_alpha = min(self.current_alpha + FADE_SPEED, 1.0)
            else:
                self.current_alpha = max(self.current_alpha - FADE_SPEED, 0.0)
            
            self.attributes('-alpha', self.current_alpha)
            
            if self.current_alpha <= 0.01 and self.target_alpha == 0.0:
                self.withdraw()
        
        self.after(20, self.fade_loop)

    def draw_wave(self):
        self.wave_canvas.delete("all")
        w = self.wave_canvas.winfo_width()
        h = self.wave_canvas.winfo_height()
        
        if w < 2: return

        ratio = 0 if self.duration <= 0 else self.position / self.duration
        filled_w = int(w * ratio)
        mid_y = h / 2
        
        if filled_w > 0:
            points = []
            shift = self.phase if self.is_playing else 0
            for x in range(0, filled_w, 2):
                y = mid_y + 4 * math.sin(0.15 * x - shift)
                points.append(x)
                points.append(y)
            
            self.wave_canvas.create_line(points, fill="#555555", width=4, smooth=True)
            self.wave_canvas.create_line(points, fill="white", width=2, smooth=True)

        if filled_w < w:
            self.wave_canvas.create_line(filled_w, mid_y, w, mid_y, fill="#333333", width=2)

        if self.is_playing:
            self.phase += 0.4

async def get_media_session():
    sessions = await wmc.GlobalSystemMediaTransportControlsSessionManager.request_async()
    return sessions.get_current_session()

async def media_loop(app):
    while True:
        try:
            session = await get_media_session()
            if session:
                props = await session.try_get_media_properties_async()
                timeline = session.get_timeline_properties()
                playback = session.get_playback_info()

                title = props.title if props.title else "Unknown"
                artist = props.artist if props.artist else ""
                dur = timeline.end_time.total_seconds() if timeline.end_time else 1
                pos = timeline.position.total_seconds() if timeline.position else 0
                playing = playback.playback_status == wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus.PLAYING

                thumb_data = None
                if props.thumbnail:
                    stream = await props.thumbnail.open_read_async()
                    if stream:
                        reader = DataReader(stream)
                        await reader.load_async(stream.size)
                        thumb_data = bytes(reader.read_buffer(stream.size))

                app.after(0, lambda: app.update_metadata(title, artist, dur, pos, playing, thumb_data))
        except:
            pass
        await asyncio.sleep(0.5)

def anim_loop(app):
    while True:
        try:
            app.after(0, app.draw_wave)
            time.sleep(0.04)
        except:
            break

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = MediaOverlay()
    
    t1 = threading.Thread(target=lambda: asyncio.run(media_loop(app)), daemon=True)
    t1.start()
    
    t2 = threading.Thread(target=anim_loop, args=(app,), daemon=True)
    t2.start()
    
    app.mainloop()