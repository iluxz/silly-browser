"""
the silly browser
a little tool that makes any website a little sillier.
no terminals. no scary green-on-black. just vibes and mischief.
"""

import os
import sys
import json
import random
import threading
import webbrowser
import http.server
import socketserver

import tkinter as tk
from tkinter import messagebox

# ── paths ────────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
SCRIPTS_FOLDER = os.path.join(SCRIPT_DIR, "scripts")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")
PORT = 8742

os.makedirs(SCRIPTS_FOLDER, exist_ok=True)

# ── the palette (deliberately not scary) ─────────────────────────────────────

CREAM = "#fff8ee"
PANEL = "#ffffff"
INK = "#2f2a45"
MUTED = "#9a93b8"
LAVENDER = "#e8defd"
PINK = "#ff8fb1"
PINK_DARK = "#e46b92"
PURPLE = "#8b6cf0"
PURPLE_DARK = "#6f4fd0"
MINT = "#5fd4b0"
MINT_DARK = "#3fae8d"
SUN = "#ffc94d"
SUN_DARK = "#e0a52c"
SKY = "#5cb8f0"

H_FONT = "Comic Sans MS"
B_FONT = "Segoe UI"
C_FONT = "Consolas"

RAINBOW = ["#ff6b6b", "#ffa94d", "#ffd43b", "#69db7c", "#4dabf7", "#b197fc", "#f783ac"]

# the cube is blue by default, but it wears whatever colour its script wears
SCRIPT_COLORS = {
    "default.js": ("#5cb8f0", "#3484c4"),
    "confetti.js": ("#ff8fb1", "#e46b92"),
    "cursor-trail.js": ("#ffc94d", "#e0a52c"),
    "floating-elements.js": ("#5fd4b0", "#3fae8d"),
    "meme-text.js": ("#8b6cf0", "#6f4fd0"),
    "rainbow-mode.js": ("#ff6b6b", "#d64f4f"),
    "screen-shake.js": ("#b197fc", "#8f74e0"),
}


def script_colors(name):
    if name in SCRIPT_COLORS:
        return SCRIPT_COLORS[name]
    idx = abs(hash(name)) % len(RAINBOW)
    return RAINBOW[idx], RAINBOW[idx]

# ── tiny helpers ──────────────────────────────────────────────────────────────


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"current_script": "default.js"}


def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        pass


BUNDLED_SCRIPTS = os.path.join(getattr(sys, "_MEIPASS", SCRIPT_DIR), "scripts")


def ensure_default_script():
    # seed bundled scripts into the writable scripts folder (frozen app case)
    try:
        if os.path.isdir(BUNDLED_SCRIPTS) and os.path.abspath(BUNDLED_SCRIPTS) != os.path.abspath(SCRIPTS_FOLDER):
            for name in os.listdir(BUNDLED_SCRIPTS):
                src = os.path.join(BUNDLED_SCRIPTS, name)
                dst = os.path.join(SCRIPTS_FOLDER, name)
                if os.path.isfile(src) and not os.path.exists(dst):
                    with open(src, "rb") as a, open(dst, "wb") as b:
                        b.write(a.read())
    except Exception:
        pass

    p = os.path.join(SCRIPTS_FOLDER, "default.js")
    if not os.path.exists(p):
        with open(p, "w", encoding="utf-8") as f:
            f.write(
                "// the silliest script of them all\n"
                "console.log('[silly browser] you are now silly. congrats!');\n"
            )


def script_files():
    try:
        return sorted(f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".js"))
    except Exception:
        return []


# ── the injector server ──────────────────────────────────────────────────────


DEMO_PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>silly browser - playground</title>
<style>
body{background:#fff8ee;font-family:'Segoe UI',sans-serif;color:#2f2a45;margin:0;padding:40px}
h1{font-size:34px;margin:0 0 6px}
p{color:#6f6885;margin:0 0 24px}
.card{background:#fff;border:3px solid #e8defd;border-radius:16px;padding:24px;max-width:640px}
button{font:700 14px 'Segoe UI';background:#8b6cf0;color:#fff;border:0;border-radius:20px;padding:12px 22px;cursor:pointer;margin-right:10px}
button.hot{background:#ff8fb1}
h2{margin:0 0 10px;font-size:18px}
</style></head><body>
<h1>silly browser playground</h1>
<p>this page is served by your own silly browser. pick a script, hit MAKE IT SILLY, then come back here.</p>
<div class="card">
<h2>try it</h2>
<button onclick="alert('the cube says hello')">click me</button>
<button class="hot" onclick="document.body.style.background='#ffe6ef'">recolour the page</button>
<p style="margin-top:20px">if your script injected, whatever it does will already be happening on this page.</p>
</div>
</body></html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/inject.js"):
            name = self.server.current_script
            path = os.path.join(SCRIPTS_FOLDER, name)
            body = "console.log('[silly browser] no script loaded');"
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        body = f.read()
                except Exception:
                    pass
            data = body.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        elif self.path.startswith("/bookmarklet"):
            bm = bookmarklet()
            data = bm.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        elif self.path.startswith("/") and self.path not in ("/favicon.ico",):
            data = DEMO_PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass


class Server(socketserver.TCPServer):
    allow_reuse_address = True
    current_script = "default.js"


def bookmarklet():
    return (
        "javascript:(function(){var s=document.createElement('script');"
        "s.src='http://localhost:%d/inject.js';document.body.appendChild(s);})();" % PORT
    )


# ── chunky rounded widgets ───────────────────────────────────────────────────


class Pill(tk.Canvas):
    """A fat rounded button that squishes when you press it."""

    def __init__(self, master, text, command=None, fill=PURPLE, dark=PURPLE_DARK,
                 fg="#ffffff", width=140, height=44, font=None, radius=None, **kw):
        super().__init__(master, width=width, height=height, highlightthickness=0,
                         bd=0, bg=master.cget("bg"), cursor="hand2", **kw)
        self._text = text
        self._cmd = command
        self.fill = fill
        self.dark = dark
        self.fg = fg
        self.font = font or (B_FONT, 11, "bold")
        self.radius = radius if radius is not None else height // 2
        self.pressed = False
        self.enabled = True
        self.bind("<Button-1>", self._down)
        self.bind("<ButtonRelease-1>", self._up)
        self.bind("<Leave>", self._leave)
        self._draw()

    def set_text(self, t):
        self._text = t
        self._draw()

    def set_fill(self, fill, dark):
        self.fill = fill
        self.dark = dark
        self._draw()

    def _rr(self, x, y, w, h, r, **kw):
        pts = []
        steps = 8
        for cx, cy, a0 in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0),
                           (x + r, y + h - r, 90), (x + r, y + r, 180)):
            for i in range(steps + 1):
                a = (a0 + i * (90 / steps)) * 3.14159265 / 180
                pts.append((cx + r * __import__("math").cos(a),
                            cy + r * __import__("math").sin(a)))
        return self.create_polygon(pts, smooth=True, **kw)

    def _draw(self):
        self.delete("all")
        w = int(self.cget("width"))
        h = int(self.cget("height"))
        d = 4 if self.pressed else 0
        r = self.radius
        self._rr(0, 4, w, h - 4, r, fill=self.dark, outline="")
        self._rr(0, d, w, h - 4, r, fill=self.fill, outline="")
        if not self.enabled:
            self._rr(0, d, w, h - 4, r, fill="#cfc9e0", outline="")
        self.create_text(w / 2, (h - 4) / 2 + d - (2 if self.pressed else 0),
                         text=self._text, fill=self.fg if self.enabled else "#ffffff",
                         font=self.font)

    def _down(self, _e):
        if self.enabled:
            self.pressed = True
            self._draw()

    def _up(self, e):
        was = self.pressed
        self.pressed = False
        self._draw()
        if was and self.enabled and self._cmd:
            if 0 <= e.x <= int(self.cget("width")) and 0 <= e.y <= int(self.cget("height")):
                self._cmd()

    def _leave(self, _e):
        self.pressed = False
        self._draw()


class Card(tk.Canvas):
    """A little rounded script card."""

    def __init__(self, master, on_click, **kw):
        super().__init__(master, height=64, highlightthickness=0, bd=0,
                         bg=master.cget("bg"), cursor="hand2", **kw)
        self.on_click = on_click
        self.title = ""
        self.sub = ""
        self.tint = PINK
        self.selected = False
        self.hover = False
        self.bind("<Button-1>", lambda e: self.on_click(self))
        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)
        self.bind("<Configure>", lambda e: self._draw())

    def set(self, title, sub, tint, selected, fname=None):
        self.title = title
        self.sub = sub
        self.tint = tint
        self.selected = selected
        self.fname = fname or title
        self._draw()

    def _enter(self, _e):
        self.hover = True
        self._draw()

    def _leave(self, _e):
        self.hover = False
        self._draw()

    def _draw(self):
        self.delete("all")
        w = int(self.cget("width")) or 220
        h = 64
        import math
        r = 14
        bg = "#ffffff" if self.selected else ("#fbf7ff" if self.hover else "#f4f0fb")
        outline = self.tint if self.selected else "#e4dcf5"
        pts = []
        for cx, cy, a0 in ((w - r, r, -90), (w - r, h - r, 0), (r, h - r, 90), (r, r, 180)):
            for i in range(9):
                a = (a0 + i * 11.25) * math.pi / 180
                pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        self.create_polygon(pts, smooth=True, fill=bg, outline=outline,
                            width=3 if self.selected else 1)
        self.create_oval(14, 20, 38, 44, fill=self.tint, outline="")
        self.create_text(50, 24, anchor="w", text=self.title, fill=INK,
                         font=(B_FONT, 11, "bold"))
        self.create_text(50, 43, anchor="w", text=self.sub, fill=MUTED,
                         font=(B_FONT, 9))


class Mascot(tk.Canvas):
    """A bouncing little cube with eyes. it wears its script's colour."""

    def __init__(self, master, **kw):
        super().__init__(master, width=120, height=110, highlightthickness=0, bd=0,
                         bg=master.cget("bg"), **kw)
        self.t = 0.0
        self.blink = 0.0
        self.spin = 0.0
        self.happy = 1.0
        self.fill = SKY
        self.edge = "#3484c4"
        self._loop()

    def set_color(self, fill, edge):
        self.fill = fill
        self.edge = edge

    def cheer(self):
        self.happy = 1.0

    def _loop(self):
        self.t += 0.05
        self.spin += 0.04
        self.blink += 0.03
        if self.blink > 4.0:
            self.blink = 0.0
        self.happy = max(0.0, self.happy - 0.02)
        self.delete("all")
        import math
        bob = math.sin(self.t) * 6
        cx, cy = 60, 52 + bob
        squash = 1 + math.sin(self.t * 2) * 0.05
        w = 46 * squash
        h = 46 / squash
        # shadow
        self.create_oval(cx - 26, 92 - abs(bob) * 0.6, cx + 26, 100 - abs(bob) * 0.6,
                         fill="#e6ddf5", outline="")
        # cube body
        self.create_rectangle(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2,
                              fill=self.fill, outline=self.edge, width=3)
        # gloss
        self.create_oval(cx - w / 2 + 6, cy - h / 2 + 4, cx - w / 2 + 20, cy - h / 2 + 16,
                         fill="#ffffff", outline="")
        # eyes
        eye_h = 11 if (self.blink < 3.4) else 1.5
        self.create_oval(cx - 13, cy - 12, cx - 3, cy - 12 + eye_h, fill=INK, outline="")
        self.create_oval(cx + 3, cy - 12, cx + 13, cy - 12 + eye_h, fill=INK, outline="")
        # mouth
        if self.happy > 0.3:
            self.create_arc(cx - 10, cy - 2, cx + 10, cy + 16, start=20, extent=140,
                            style="arc", outline=INK, width=3)
        else:
            self.create_line(cx - 8, cy + 10, cx + 8, cy + 10, fill=INK, width=3)
        # little floating hearts when cheering
        if self.happy > 0.55:
            import math as _m
            for i in range(3):
                ph = self.t * 2 + i * 2.1
                hx = cx + _m.cos(ph) * 34
                hy = cy - 26 + _m.sin(ph * 1.3) * 8
                self.create_text(hx, hy, text="❤", fill=self.fill, font=(B_FONT, 11))
        self.after(33, self._loop)


# ── the app ──────────────────────────────────────────────────────────────────


class SillyBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("the silly browser")
        self.root.geometry("960x640")
        self.root.configure(bg=CREAM)
        self.root.minsize(840, 560)
        self.config = load_config()
        ensure_default_script()
        self.set_window_icon()

        self.server = None
        try:
            self.server = Server(("127.0.0.1", PORT), Handler)
            self.server.current_script = self.config.get("current_script", "default.js")
            threading.Thread(target=self.server.serve_forever, daemon=True).start()
        except OSError as e:
            messagebox.showwarning(
                "port is busy",
                "something else is already using port %d (%s).\n\n"
                "close it and restart the silly browser, or nothing will inject." % (PORT, e))

        self.cards = []
        self.current = self.server.current_script

        self._build()
        self.refresh_cards()
        self.load_script(self.current)

    # -- layout ---------------------------------------------------------------

    def set_window_icon(self):
        """put the cube in the title bar + taskbar (pyinstaller exes need this)"""
        base = getattr(sys, "_MEIPASS", SCRIPT_DIR)
        for candidate in (os.path.join(base, "silly.ico"),
                          os.path.join(SCRIPT_DIR, "silly.ico")):
            if os.path.exists(candidate):
                try:
                    self.root.iconbitmap(candidate)
                    return
                except Exception:
                    pass

    def _build(self):
        top = tk.Frame(self.root, bg=CREAM)
        top.pack(fill="x", side="top")

        self.logo_img = None
        base = getattr(sys, "_MEIPASS", SCRIPT_DIR)
        for candidate in (os.path.join(base, "logo_small.png"),
                          os.path.join(SCRIPT_DIR, "logo_small.png")):
            if os.path.exists(candidate):
                try:
                    self.logo_img = tk.PhotoImage(file=candidate)
                    break
                except Exception:
                    self.logo_img = None

        banner = tk.Canvas(top, height=96, highlightthickness=0, bd=0, bg=CREAM)
        banner.pack(fill="x")
        banner.bind("<Configure>", lambda e: self._draw_banner(banner, e.width))

        self.mascot = Mascot(top)
        self.mascot.place(relx=1.0, x=-140, y=6)

        # bottom bar (packed BEFORE body so expand doesn't eat it)
        bottom = tk.Frame(self.root, bg=CREAM)
        bottom.pack(fill="x", side="bottom", padx=18, pady=(10, 16))

        body = tk.Frame(self.root, bg=CREAM)
        body.pack(fill="both", expand=True, padx=18, pady=(4, 0))

        # left: script cards
        left = tk.Frame(body, bg=CREAM)
        left.pack(side="left", fill="y")

        tk.Label(left, text="the silly scripts", bg=CREAM, fg=INK,
                 font=(H_FONT, 14, "bold")).pack(anchor="w", pady=(6, 2))
        tk.Label(left, text="pick one and we'll make it happen", bg=CREAM, fg=MUTED,
                 font=(B_FONT, 9)).pack(anchor="w", pady=(0, 8))

        # scrollable card list
        self.card_host = tk.Frame(left, bg=CREAM)
        self.card_host.pack(fill="both", expand=True)

        self.card_canvas = tk.Canvas(self.card_host, bg=CREAM, highlightthickness=0, bd=0)
        self.card_scroll = tk.Scrollbar(self.card_host, orient="vertical",
                                        command=self.card_canvas.yview)
        self.card_canvas.configure(yscrollcommand=self.card_scroll.set)
        self.card_scroll.pack(side="right", fill="y")
        self.card_canvas.pack(side="left", fill="both", expand=True)
        self.card_inner = tk.Frame(self.card_canvas, bg=CREAM)
        self.card_win = self.card_canvas.create_window((0, 0), window=self.card_inner,
                                                       anchor="nw")
        self.card_inner.bind("<Configure>",
                              lambda e: self.card_canvas.configure(scrollregion=self.card_canvas.bbox("all")))
        self.card_canvas.bind("<Configure>",
                               lambda e: self.card_canvas.itemconfigure(self.card_win, width=e.width))
        for w in (self.card_canvas, self.card_inner):
            w.bind("<MouseWheel>", self._scroll_cards)

        self.list_btns = tk.Frame(left, bg=CREAM)
        self.list_btns.pack(fill="x", pady=(8, 0))
        Pill(self.list_btns, "+ new", self.new_script, fill=MINT, dark=MINT_DARK,
             width=88, height=36, font=(B_FONT, 10, "bold")).pack(side="left")
        Pill(self.list_btns, "delete", self.delete_script, fill="#f0e8ff", dark="#d8c9f7",
             fg=PURPLE_DARK, width=88, height=36, font=(B_FONT, 10, "bold")).pack(side="right")

        # right: editor
        right = tk.Frame(body, bg=CREAM)
        right.pack(side="right", fill="both", expand=True, padx=(18, 0))

        editor_head = tk.Frame(right, bg=CREAM)
        editor_head.pack(fill="x", pady=(6, 4))
        tk.Label(editor_head, text="your evil little code", bg=CREAM, fg=INK,
                 font=(H_FONT, 14, "bold")).pack(side="left")
        self.editor_name = tk.Label(editor_head, text="", bg=CREAM, fg=PURPLE,
                                    font=(C_FONT, 11, "bold"))
        self.editor_name.pack(side="left", padx=(10, 0))

        edit_wrap = tk.Frame(right, bg=PANEL, highlightbackground="#e7dff7",
                             highlightthickness=2)
        edit_wrap.pack(fill="both", expand=True)
        self.editor = tk.Text(edit_wrap, bg="#fffdf8", fg=INK, insertbackground=PURPLE,
                               font=(C_FONT, 12), wrap="none", undo=True, bd=0,
                               highlightthickness=0, padx=12, pady=10,
                               selectbackground="#e8defd", selectforeground=INK)
        # scrollbars packed BEFORE the text so expand doesn't squeeze them out
        hbar = tk.Scrollbar(edit_wrap, orient="horizontal", command=self.editor.xview)
        hbar.pack(side="bottom", fill="x")
        vbar = tk.Scrollbar(edit_wrap, orient="vertical", command=self.editor.yview)
        vbar.pack(side="right", fill="y")
        self.editor.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.editor.pack(fill="both", expand=True)
        self.editor.bind("<Control-s>", lambda e: self.save_script())

        self.inject_btn = Pill(bottom, "🎉  MAKE IT SILLY", self.inject_now,
                                fill=PINK, dark=PINK_DARK, width=220, height=52,
                                font=(H_FONT, 15, "bold"))
        self.inject_btn.pack(side="left")

        Pill(bottom, "📋  copy bookmarklet", self.copy_bookmarklet,
             fill=PURPLE, dark=PURPLE_DARK, width=200, height=52,
             font=(B_FONT, 12, "bold")).pack(side="left", padx=(10, 0))

        Pill(bottom, "🎲  surprise me", self.surprise_me,
             fill=SUN, dark=SUN_DARK, fg="#5c4400", width=170, height=52,
             font=(B_FONT, 12, "bold")).pack(side="left", padx=(10, 0))

        Pill(bottom, "🧪  playground", self.open_playground,
             fill=MINT, dark=MINT_DARK, width=170, height=52,
             font=(B_FONT, 12, "bold")).pack(side="left", padx=(10, 0))

        Pill(bottom, "💾  save", self.save_script, fill="#e9e3f7", dark="#d5cbec",
             fg=PURPLE_DARK, width=110, height=52, font=(B_FONT, 12, "bold")).pack(
            side="left", padx=(10, 0))

        self.status = tk.Label(bottom, text="", bg=CREAM, fg=MUTED, font=(B_FONT, 10))
        self.status.pack(side="right")

    def _scroll_cards(self, e):
        self.card_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

    def _draw_banner(self, canvas, width):
        canvas.delete("all")
        h = 96
        for i in range(h):
            t = i / h
            r = int(0xFF * (1 - t) + 0xF0 * t)
            g = int(0xF8 * (1 - t) + 0xE6 * t)
            b = int(0xFF * (1 - t) + 0xFB * t)
            canvas.create_line(0, i, width, i, fill="#%02x%02x%02x" % (r, g, b))
        # soft blobs for depth (kept close to the gradient so they read as glow)
        for cx, col, rx in ((0.16, "#ffe6ef", 56), (0.52, "#efe6ff", 70), (0.86, "#e2f8f1", 52)):
            canvas.create_oval(width * cx - rx, -44, width * cx + rx, 42,
                               fill=col, outline="")
        # the official logo, drawn straight onto the canvas
        if self.logo_img is not None:
            canvas.create_image(26, 22, anchor="nw", image=self.logo_img)
            canvas.create_text(28, 72, anchor="w",
                               text="makes any website a little sillier  ✦  visual only, your screen only",
                               fill=MUTED, font=(B_FONT, 10))
        else:
            canvas.create_text(26, 34, anchor="w", text="the silly browser",
                               fill=INK, font=(H_FONT, 26, "bold"))
            canvas.create_text(28, 66, anchor="w",
                               text="makes any website a little sillier  ✦  visual only, your screen only",
                               fill=MUTED, font=(B_FONT, 10))

    # -- script list ----------------------------------------------------------

    def refresh_cards(self):
        for c in self.cards:
            c.destroy()
        self.cards = []
        files = script_files()
        if not files:
            return
        for i, name in enumerate(files):
            tint, _ = script_colors(name)
            card = Card(self.card_inner, self.on_card_click)
            card.pack(fill="x", pady=3)
            card.set(name.replace(".js", "").replace("-", " ").replace("_", " "),
                     "a little mischief",
                     tint, name == self.current, fname=name)
            self.cards.append(card)

    def on_card_click(self, card):
        self.load_script(card.fname)

    def load_script(self, name):
        path = os.path.join(SCRIPTS_FOLDER, name)
        if not os.path.exists(path):
            path = os.path.join(SCRIPTS_FOLDER, "default.js")
            name = "default.js"
        self.current = name
        if self.server is not None:
            self.server.current_script = name
        self.config["current_script"] = name
        save_config(self.config)
        with open(path, "r", encoding="utf-8") as f:
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", f.read())
        self.editor_name.configure(text=name)
        fill, edge = script_colors(name)
        self.mascot.set_color(fill, edge)
        self.refresh_cards()

    # -- actions --------------------------------------------------------------

    def save_script(self):
        name = self.current
        with open(os.path.join(SCRIPTS_FOLDER, name), "w", encoding="utf-8") as f:
            f.write(self.editor.get("1.0", tk.END))
        self.status.configure(text="saved ✓  " + name)
        self.root.after(2200, lambda: self.status.configure(text=""))

    def new_script(self):
        name = "silly_idea.js"
        i = 1
        while os.path.exists(os.path.join(SCRIPTS_FOLDER, name)):
            name = "silly_idea_%d.js" % i
            i += 1
        with open(os.path.join(SCRIPTS_FOLDER, name), "w", encoding="utf-8") as f:
            f.write("// new mischief goes here\n")
        self.refresh_cards()
        self.load_script(name)

    def delete_script(self):
        if self.current == "default.js":
            self.status.configure(text="nope, that one's sacred")
            self.root.after(2200, lambda: self.status.configure(text=""))
            return
        if messagebox.askyesno("delete it?", "throw away %s?" % self.current):
            try:
                os.remove(os.path.join(SCRIPTS_FOLDER, self.current))
            except Exception:
                pass
            self.current = "default.js"
            self.refresh_cards()
            self.load_script("default.js")

    def copy_bookmarklet(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(bookmarklet())
        self.mascot.cheer()
        self.status.configure(text="bookmarklet copied!  paste it as a bookmark ✦")
        self.root.after(3200, lambda: self.status.configure(text=""))

    def inject_now(self):
        self.save_script()
        self.copy_bookmarklet()
        self.status.configure(
            text="now click your bookmark on any website  ✦")

    def surprise_me(self):
        files = script_files()
        if not files:
            return
        pick = random.choice(files)
        self.load_script(pick)
        self.mascot.cheer()
        self.status.configure(text="feeling lucky: %s  ✦" % pick)
        self.root.after(2600, lambda: self.status.configure(text=""))

    def open_playground(self):
        if self.server is None:
            self.status.configure(text="server is not running  ✦")
            return
        webbrowser.open("http://localhost:%d/" % PORT)
        self.status.configure(text="playground opened  ✦  hit MAKE IT SILLY then refresh")
        self.root.after(3200, lambda: self.status.configure(text=""))


def main():
    root = tk.Tk()
    app = SillyBrowser(root)
    root.mainloop()
    try:
        app.server.shutdown()
    except Exception:
        pass


if __name__ == "__main__":
    main()
