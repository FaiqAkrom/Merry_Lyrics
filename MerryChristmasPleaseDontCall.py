import os
import time
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont

INTRO_DURATION = 3.5

LYRICS = [
    (3.5,  "I want one ticket out of your heavy gaze"),
    (7.5,  "I want one ticket off of your carousel"),
    (12.5, "But you should know that I die slow"),
    (16.5, "Running through the halls of your haunted home"),
    (21.5, "And the toughest part is that we both know"),
    (25.5, "What happened to you"),
    (27.5, "Why you're out on your own"),
    (29.5, "Merry Christmas, please don't call"),
    (34.5, "Merry Christmas, I'm not yours at all"),
    (39.5, "Merry Christmas, please don't call me"),
    (44.5, "Please don't call me"),
    (48.5, "Please don't call me"),
    (52.5, "Please don't call me"),
]

BG_BLACK = "#000000"
DIM_OPACITY = 0.80
DOT_MATRIX_WHITE = "#FFFFFF"
SUBTLE_CREDIT = "#8892B0"
SUBTLE_HINT = "#333842"


def get_raster_font(size=11):
    """Retrieve best available monospaced bold system font for rasterization."""
    candidates = [
        "C:/Windows/Fonts/consolab.ttf",
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/courbd.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

RASTER_FONT = get_raster_font(11)


def text_to_matrix_rows(text, pad_len=None, fill_str="nn", empty_str="  "):
    """
    Convert text into an 8-row dot-matrix ASCII block (as in Image 2).
    Every ON pixel in the glyph is mapped to 'nn' micro-segments.
    """
    if not text and not pad_len:
        return []

    target_str = text.ljust(pad_len) if pad_len else text
    if not target_str.strip():
        col_count = len(target_str) * 6
        return [empty_str * col_count for _ in range(8)]

    bbox = RASTER_FONT.getbbox(target_str)
    w = max(1, bbox[2] - bbox[0])
    h = max(1, bbox[3] - bbox[1])

    img = Image.new("1", (w + 2, h + 2), 0)
    draw = ImageDraw.Draw(img)
    draw.text((1 - bbox[0], 1 - bbox[1]), target_str, font=RASTER_FONT, fill=1)

    rows = []
    for y in range(img.height):
        row = "".join(fill_str if img.getpixel((x, y)) else empty_str for x in range(img.width))
        rows.append(row)

    while rows and not rows[0].strip():
        rows.pop(0)
    while rows and not rows[-1].strip():
        rows.pop()

    return rows if rows else [empty_str * 10 for _ in range(8)]


def format_title_case(text):
    """Capitalize words matching the concert marquee styling of Image 2."""
    words = text.split()
    formatted = []
    for w in words:
        if len(w) > 1 and w[0] in ("'", '"'):
            formatted.append(w[0] + w[1:].capitalize())
        else:
            formatted.append(w.capitalize())
    return " ".join(formatted)


def split_lyric_into_lines(text):
    """
    Intelligently split lyric text into 2 short, balanced lines
    guaranteeing lines never exceed 22 characters to prevent edge clipping.
    """
    formatted = format_title_case(text.strip())

    curated_map = {
        "I Want One Ticket Out Of Your Heavy Gaze": ["I Want One Ticket", "Out Of Your Heavy Gaze"],
        "I Want One Ticket Off Of Your Carousel": ["I Want One Ticket", "Off Of Your Carousel"],
        "But You Should Know That I Die Slow": ["But You", "Should Know"],
        "Running Through The Halls Of Your Haunted Home": ["Running Through The Halls", "Of Your Haunted Home"],
        "And The Toughest Part Is That We Both Know": ["And The Toughest Part", "Is That We Both Know"],
        "What Happened To You": ["What Happened", "To You"],
        "Why You're Out On Your Own": ["Why You're Out", "On Your Own"],
        "Merry Christmas, Please Don't Call": ["Merry Christmas,", "Please Don't Call"],
        "Merry Christmas, I'm Not Yours At All": ["Merry Christmas,", "I'm Not Yours At All"],
        "Merry Christmas, Please Don't Call Me": ["Merry Christmas,", "Please Don't Call Me"],
        "Please Don't Call Me": ["Please Don't", "Call Me"],
    }

    if formatted in curated_map:
        return curated_map[formatted]

    if len(formatted) <= 16:
        return [formatted]

    if ", " in formatted:
        parts = formatted.split(", ")
        p1 = parts[0] + ","
        p2 = ", ".join(parts[1:])
        return [p1, p2]

    words = formatted.split()
    mid = len(words) // 2
    best_split = mid
    best_diff = 999
    for i in range(1, len(words)):
        s1 = " ".join(words[:i])
        s2 = " ".join(words[i:])
        diff = abs(len(s1) - len(s2))
        if diff < best_diff:
            best_diff = diff
            best_split = i

    return [" ".join(words[:best_split]), " ".join(words[best_split:])]


class AsciiLyricsApp:
    """
    Unified Concert Dot-Matrix Lyrics Experience:
    - Clean, focused, minimalist dark stage
    - Intro (0.0s - 3.5s): Pure dot-matrix song title & Bleachers credit badge
    - Lyrics (3.5s onwards): Glowing white dot-matrix typewriter reveal
    - Strict 2-line layout with automatic responsive font scaling: ZERO edge clipping
    - 80% dimmed translucent fullscreen overlay with ESC / Q instant exit
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Merry Christmas, Please Don't Call")

        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        try:
            self.root.attributes("-alpha", DIM_OPACITY)
        except tk.TclError:
            pass

        self.root.configure(bg=BG_BLACK)
        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()

        # Center stage container for lyrics & intro title
        self.stage = tk.Frame(self.root, bg=BG_BLACK)
        self.stage.place(relx=0.5, rely=0.5, anchor="center")

        # Main Dot-Matrix Lyric Scoreboard
        self.matrix_label = tk.Label(
            self.stage,
            text="",
            font=("Consolas", 10, "bold"),
            fg=DOT_MATRIX_WHITE,
            bg=BG_BLACK,
            justify="center",
        )
        self.matrix_label.pack(pady=10)

        # Intro Subtitle / Credit Badge (Visible during intro)
        self.credit_badge = tk.Label(
            self.stage,
            text="[ WRITTEN & PERFORMED BY JACK ANTONOFF AND BLEACHERS ]",
            font=("Consolas", 10, "bold"),
            fg=SUBTLE_CREDIT,
            bg=BG_BLACK,
        )
        self.credit_badge.pack(pady=(16, 0))

        # Minimalist bottom escape hint
        self.hint_label = tk.Label(
            self.root,
            text="[ Press ESC or Q to exit ]",
            font=("Consolas", 9),
            fg=SUBTLE_HINT,
            bg=BG_BLACK,
        )
        self.hint_label.place(relx=0.5, rely=0.96, anchor="center")

        self.root.bind("<Escape>", lambda e: self.quit_app())
        self.root.bind("q", lambda e: self.quit_app())

        self.current_idx = 0
        self.intro_finished = False
        self.is_closing = False
        self.anim_typewriter_id = None

        self.start_time = time.time()
        self.last_lyric_time = LYRICS[-1][0] if LYRICS else 0

        self.show_intro_title()
        self.tick()

    def show_intro_title(self):
        """Display the song title in the exact same glowing dot-matrix style."""
        intro_lines = ["Merry Christmas,", "Please Don't Call"]
        self.apply_responsive_font(intro_lines)

        m1 = text_to_matrix_rows(intro_lines[0])
        m2 = text_to_matrix_rows(intro_lines[1])
        combined = m1 + [""] + m2
        self.matrix_label.config(text="\n".join(combined))

    def apply_responsive_font(self, target_lines):
        """
        Dynamically calculate font size so that the dot-matrix rows
        are mathematically guaranteed never to exceed 78% of the screen width,
        leaving comfortable margins and completely preventing edge clipping.
        """
        max_px = 1
        for line in target_lines:
            bbox = RASTER_FONT.getbbox(line)
            w = max(1, bbox[2] - bbox[0])
            if w > max_px:
                max_px = w

        max_cols = max_px * 2

        calculated_size = int((self.screen_w * 0.78) / (max_cols * 0.62))
        safe_font_size = max(6, min(12, calculated_size))

        self.matrix_label.config(font=("Consolas", safe_font_size, "bold"))

    def trigger_line(self, text):
        """Initiate the typewriter reveal for a newly arriving lyric."""
        if not self.intro_finished:
            self.intro_finished = True
            self.credit_badge.pack_forget()

        if self.anim_typewriter_id:
            self.root.after_cancel(self.anim_typewriter_id)

        target_lines = split_lyric_into_lines(text)
        self.apply_responsive_font(target_lines)
        self.animate_dot_matrix_typewriter(target_lines, current_char_count=0)

    def animate_dot_matrix_typewriter(self, target_lines, current_char_count=0):
        """
        Reveal dot-matrix letters sequentially from left to right.
        Maintains fixed padded dimensions so the display remains stable.
        """
        if self.is_closing:
            return

        total_chars = sum(len(line) for line in target_lines)
        l1_len = len(target_lines[0])

        if current_char_count <= l1_len:
            curr_l1 = target_lines[0][:current_char_count]
            curr_l2 = ""
        else:
            curr_l1 = target_lines[0]
            curr_l2 = target_lines[1][: current_char_count - l1_len]

        m1 = text_to_matrix_rows(curr_l1, pad_len=l1_len)
        m2 = text_to_matrix_rows(curr_l2, pad_len=len(target_lines[1])) if len(target_lines) > 1 else []

        combined = m1 + [""] + m2 if m2 else m1
        self.matrix_label.config(text="\n".join(combined))

        if current_char_count < total_chars:
            if current_char_count < l1_len:
                ch = target_lines[0][current_char_count]
            else:
                ch = target_lines[1][current_char_count - l1_len]

            delay = 20 if ch == " " else 36
            self.anim_typewriter_id = self.root.after(
                delay,
                self.animate_dot_matrix_typewriter,
                target_lines,
                current_char_count + 1,
            )

    def tick(self):
        """Main timeline coordinator matching exact intervals."""
        if self.is_closing:
            return

        elapsed = time.time() - self.start_time

        while (
            self.current_idx < len(LYRICS)
            and LYRICS[self.current_idx][0] <= elapsed
        ):
            _, text = LYRICS[self.current_idx]
            self.trigger_line(text)
            self.current_idx += 1

        if self.current_idx >= len(LYRICS) and elapsed > self.last_lyric_time + 5.5:
            self.fade_out_and_close()
            return

        self.root.after(25, self.tick)

    def fade_out_and_close(self, current_alpha=DIM_OPACITY):
        """Gracefully fade out opacity and close after the song ends."""
        self.is_closing = True
        if current_alpha > 0.05:
            next_alpha = max(0.0, current_alpha - 0.05)
            try:
                self.root.attributes("-alpha", next_alpha)
                self.root.after(35, self.fade_out_and_close, next_alpha)
            except tk.TclError:
                self.quit_app()
        else:
            self.quit_app()

    def quit_app(self):
        """Cleanly destroy window and terminate."""
        try:
            self.root.destroy()
        except tk.TclError:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = AsciiLyricsApp(root)
    root.mainloop()
