# Merry_Lyrics

A fullscreen animated lyric overlay featuring a retro concert dot-matrix visualizer for the song "Merry Christmas, Please Don't Call" by Jack Antonoff & Bleachers.

The application renders lyrics with 8-row raster dot-matrix micro-glyphs, typewriter reveal animations, responsive anti-clipping scaling, and an integrated concert-style intro title sequence.

---

## Requirements

- **Python 3.8+**
- **Tkinter**: Pre-installed with standard Python distributions on Windows and macOS.
  - Linux (Ubuntu/Debian) users need to install it separately:
    ```bash
    sudo apt update
    sudo apt install python3-tk
    ```
- **Pillow**: Required for the dot-matrix font rasterization engine (`pip install -r requirements.txt`).
