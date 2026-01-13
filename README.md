Harika, projeni GitHub'da yayınlaman için gereken profesyonel dosyaları hazırladım.

### 1. `README.md` Dosyası

Bu dosya, projenin "vitrini"dir. İnsanlar projene girdiğinde uygulamanın ne işe yaradığını, nasıl kurulacağını ve özelliklerini buradan okurlar. Standart olarak İngilizce hazırladım (GitHub'da genelde İngilizce kullanılır), istersen Türkçeye çevirebilirsin.

Bir dosya oluştur, adını **`README.md`** koy ve içine şunları yapıştır:

```markdown
# 🎵 Modern Windows Media Overlay

A sleek, lightweight, and customizable "Now Playing" overlay for Windows 10/11. It displays the current song's title, artist, and album art with a smooth animated waveform and fade effects.

![Preview](preview.png)
*(Note: Don't forget to add a screenshot of your app here and name it preview.png)*

## ✨ Features

- **Modern UI:** Rounded corners with a transparent background (no jagged edges).
- **Animated Waveform:** A smooth, sine-wave animation that syncs with the song's progress.
- **Dynamic Metadata:** Automatically fetches cover art, title, and artist from Windows Media Controls (Spotify, YouTube, SoundCloud, etc.).
- **Smart Visibility:** - Appears automatically when the song changes or pauses/plays.
  - Fades out smoothly after a few seconds of inactivity.
- **Soft Rendering:** Anti-aliased lines and borders for a high-quality look.

## 📦 Requirements

- Python 3.10+
- Windows 10 or Windows 11 (Required for `winsdk`)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/media-overlay.git](https://github.com/your-username/media-overlay.git)
   cd media-overlay

```

2. **Install dependencies:**
```bash
start setup.bat

```

## 🎮 Usage

Simply run the main script:

```bash
start start.bat

```

The overlay will appear on the top-left of your screen (customizable) whenever you play music on Spotify, Chrome, or any supported media player.

## ⚙️ Configuration

You can adjust the settings at the top of `main.py`:

```python
WINDOW_W = 340          # Width of the popup
POS_X = 20              # Horizontal position
POS_Y = 80              # Vertical position
TIMEOUT_SECONDS = 4     # How long it stays visible
FADE_SPEED = 0.08       # Fade animation speed

```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

```
