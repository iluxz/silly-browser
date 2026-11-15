"""
the silly browser v1.2 - the advanced update
a desktop app that injects js + css into any website via a bookmarklet.
visual only, your screen only. no chromium, no extensions, no store submissions.

v1.2 features:
  - multi-script stacking (run several at once)
  - css injection alongside js
  - site-specific auto-run rules
  - element picker (click to get a selector)
  - persistent mode (survives spa navigation)
  - undo (remove all injected stuff)
  - live preview in playground
  - script search + tags
"""
import os
import sys
import json
import random
import threading
import webbrowser
import http.server
import socketserver
import re

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog

# ── paths ────────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
SCRIPTS_FOLDER = os.path.join(SCRIPT_DIR, "scripts")
CSS_FOLDER = os.path.join(SCRIPT_DIR, "styles")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")
RULES_FILE = os.path.join(SCRIPT_DIR, "site_rules.json")
PORT = 8742
CURRENT_VERSION = "1.3.0"
GITHUB_REPO = "the-silly-team/silly-browser"

os.makedirs(SCRIPTS_FOLDER, exist_ok=True)
os.makedirs(CSS_FOLDER, exist_ok=True)

# ── palette ──────────────────────────────────────────────────────────────────

CREAM = "#fff8ee"
WHITE = "#ffffff"
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
SKY_DARK = "#3484c4"
CORAL = "#ff6b6b"
CORAL_DARK = "#d64f4f"

H_FONT = "Comic Sans MS"
B_FONT = "Segoe UI"
C_FONT = "Consolas"

RAINBOW = ["#ff6b6b", "#ffa94d", "#ffd43b", "#69db7c", "#4dabf7", "#b197fc", "#f783ac"]

SCRIPT_COLORS = {
    "default.js": (SKY, SKY_DARK),
    "confetti.js": (PINK, PINK_DARK),
    "cursor-trail.js": (SUN, SUN_DARK),
    "floating-elements.js": (MINT, MINT_DARK),
    "meme-text.js": (PURPLE, PURPLE_DARK),
    "rainbow-mode.js": (CORAL, CORAL_DARK),
    "screen-shake.js": ("#b197fc", "#8f74e0"),
    "dark-mode.css": ("#2f2a45", "#1a1530"),
    "highlighter.js": ("#ffd43b", "#e0a52c"),
    "ad-remover.js": ("#69db7c", "#3fae8d"),
    "text-replacer.js": ("#4dabf7", "#2c8fd6"),
    "element-picker.js": ("#ffd43b", "#e0a52c"),
    "font-changer.css": ("#f783ac", "#d65f8a"),
    "brain-liquidation-1.js": ("#ff3d63", "#c92a4a"),
    "brain-liquidation-2.js": ("#b68cff", "#8a5fd4"),
    "brain-liquidation-3.js": ("#9d75ed", "#7a52c4"),
    "brain-liquidation-4.js": ("#ffbd4a", "#d49a2a"),
    "brain-liquidation-5.js": ("#e9a84e", "#b8802a"),
    "brain-liquidation-6.js": ("#ff00cc", "#cc00a3"),
    "silly-plus-stars.js": ("#ffd700", "#e6c200"),
    "silly-plus-wobble.js": ("#ff6b6b", "#d64f4f"),
    "silly-plus-spotlight.js": ("#2f2a45", "#1a1530"),
    "silly-plus-gravity.js": ("#69db7c", "#3fae8d"),
    "silly-plus-matrix.js": ("#00ff41", "#00cc33"),
}


def script_colors(name):
    if name in SCRIPT_COLORS:
        return SCRIPT_COLORS[name]
    idx = abs(hash(name)) % len(RAINBOW)
    return RAINBOW[idx], RAINBOW[idx]


# ── config ───────────────────────────────────────────────────────────────────

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "enabled_scripts": ["default.js"],
            "enabled_css": [],
            "site_rules": {},
            "persistent": False,
            "multi_mode": True,
        }


def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)


def load_rules():
    try:
        with open(RULES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_rules(rules):
    with open(RULES_FILE, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2)


# ── script helpers ───────────────────────────────────────────────────────────

def script_files():
    try:
        return sorted(f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".js"))
    except Exception:
        return []


def css_files():
    try:
        return sorted(f for f in os.listdir(CSS_FOLDER) if f.endswith(".css"))
    except Exception:
        return []


def ensure_defaults():
    defaults = {
        "default.js": '// silly browser - default script\nconsole.log("[silly browser] injected! you are now silly.");\n',
        "confetti.js": '''// silly browser - confetti explosion
// click anywhere to trigger a confetti explosion
(function() {
  function confetti(x, y) {
    for (let i = 0; i < 30; i++) {
      const p = document.createElement("div");
      p.style.cssText = "position:fixed;pointer-events:none;z-index:999999;width:8px;height:8px;border-radius:50%;left:" + x + "px;top:" + y + "px;";
      p.style.background = ["#ff6b6b","#ffa94d","#ffd43b","#69db7c","#4dabf7","#b197fc","#f783ac"][Math.floor(Math.random()*7)];
      document.body.appendChild(p);
      const angle = Math.random() * Math.PI * 2;
      const speed = 2 + Math.random() * 4;
      let vx = Math.cos(angle) * speed, vy = Math.sin(angle) * speed - 2;
      let life = 0;
      const iv = setInterval(() => {
        life++;
        p.style.left = (parseFloat(p.style.left) + vx) + "px";
        p.style.top = (parseFloat(p.style.top) + vy) + "px";
        vy += 0.15;
        p.style.opacity = 1 - life / 40;
        if (life > 40) { clearInterval(iv); p.remove(); }
      }, 16);
    }
  }
  document.addEventListener("click", e => confetti(e.clientX, e.clientY));
  console.log("[silly] confetti explosion active! click anywhere!");
})();
''',
        "cursor-trail.js": '''// silly browser - cursor trail
(function() {
  const colors = ["#ff6b6b","#ffa94d","#ffd43b","#69db7c","#4dabf7","#b197fc","#f783ac"];
  let idx = 0;
  document.addEventListener("mousemove", e => {
    const d = document.createElement("div");
    d.style.cssText = "position:fixed;pointer-events:none;z-index:999999;width:10px;height:10px;border-radius:50%;left:" + (e.clientX-5) + "px;top:" + (e.clientY-5) + "px;background:" + colors[idx % colors.length] + ";transition:opacity .6s;";
    document.body.appendChild(d);
    idx++;
    setTimeout(() => { d.style.opacity = "0"; setTimeout(() => d.remove(), 600); }, 50);
  });
  console.log("[silly] cursor trail active!");
})();
''',
        "floating-elements.js": '''// silly browser - floating elements
(function() {
  const els = document.querySelectorAll("img, button, a, h1, h2, h3, p");
  els.forEach((el, i) => {
    el.style.transition = "transform 2s ease-in-out";
    const amp = 4 + Math.random() * 6;
    const dur = 2 + Math.random() * 2;
    el.animate([{transform:"translateY(0px)"},{transform:"translateY(-"+amp+"px)"},{transform:"translateY(0px)"}],
      {duration: dur*1000, iterations: Infinity, easing:"ease-in-out", delay: i*100});
  });
  console.log("[silly] floating elements active!");
})();
''',
        "meme-text.js": '''// silly browser - meme text replacer
(function() {
  const swaps = {"the":"teh","you":"u","your":"ur","are":"r","to":"2","too":"2","for":"4","before":"b4","great":"gr8","late":"l8","and":"&","because":"cuz","people":"ppl","okay":"ok","thanks":"thx"};
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(n => {
    let t = n.nodeValue;
    Object.keys(swaps).forEach(k => {
      t = t.replace(new RegExp("\\\\b"+k+"\\\\b","gi"), swaps[k]);
    });
    n.nodeValue = t;
  });
  console.log("[silly] meme text active!");
})();
''',
        "rainbow-mode.js": '''// silly browser - rainbow mode
(function() {
  let hue = 0;
  setInterval(() => {
    hue = (hue + 1) % 360;
    document.body.style.filter = "hue-rotate(" + hue + "deg)";
  }, 50);
  console.log("[silly] rainbow mode active!");
})();
''',
        "screen-shake.js": '''// silly browser - screen shake
(function() {
  setInterval(() => {
    const x = (Math.random()-0.5)*6, y = (Math.random()-0.5)*6;
    document.body.style.transform = "translate(" + x + "px," + y + "px)";
    setTimeout(() => { document.body.style.transform = ""; }, 200);
  }, 3000);
  console.log("[silly] screen shake active!");
})();
''',
        "highlighter.js": '''// silly browser - element highlighter (hover to see box)
(function() {
  const box = document.createElement("div");
  box.style.cssText = "position:fixed;pointer-events:none;z-index:999999;border:2px solid #ff6b6b;background:rgba(255,107,107,0.1);transition:all .1s;display:none;";
  document.body.appendChild(box);
  document.addEventListener("mousemove", e => {
    const el = document.elementFromPoint(e.clientX, e.clientY);
    if (!el || el === box) return;
    const r = el.getBoundingClientRect();
    box.style.left = r.left + "px";
    box.style.top = r.top + "px";
    box.style.width = r.width + "px";
    box.style.height = r.height + "px";
    box.style.display = "block";
  });
  console.log("[silly] element highlighter active! hover to inspect.");
})();
''',
        "ad-remover.js": '''// silly browser - ad remover (best effort)
(function() {
  const selectors = ['[class*="ad-"]','[id*="ad-"]','[class*="banner"]','iframe[src*="ads"]','[class*="sponsor"]','[class*="promo"]'];
  let removed = 0;
  selectors.forEach(s => {
    document.querySelectorAll(s).forEach(el => { el.remove(); removed++; });
  });
  console.log("[silly] ad remover: removed " + removed + " elements.");
})();
''',
        "text-replacer.js": '''// silly browser - text replacer (edit the map below)
(function() {
  const map = {"hello":"howdy","world":"earth","the":"teh"};
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(n => {
    let t = n.nodeValue;
    Object.keys(map).forEach(k => { t = t.split(k).join(map[k]); });
    n.nodeValue = t;
  });
  console.log("[silly] text replacer active!");
})();
''',
        "element-picker.js": '''// silly browser - element picker (click to get selector)
(function() {
  const box = document.createElement("div");
  box.style.cssText = "position:fixed;pointer-events:none;z-index:999999;border:2px solid #ff6b6b;background:rgba(255,107,107,0.15);transition:all .08s;";
  document.body.appendChild(box);
  let active = true;
  const handler = (e) => {
    if (!active) return;
    const el = document.elementFromPoint(e.clientX, e.clientY);
    if (!el || el === box) return;
    const r = el.getBoundingClientRect();
    box.style.left = r.left + "px";
    box.style.top = r.top + "px";
    box.style.width = r.width + "px";
    box.style.height = r.height + "px";
    e.preventDefault();
    e.stopPropagation();
    // build selector
    let sel = el.tagName.toLowerCase();
    if (el.id) sel = "#" + el.id;
    else if (el.className) sel += "." + el.className.trim().split(/\\s+/).join(".");
    console.log("[silly picker] selector:", sel, "| text:", (el.textContent||"").slice(0,60));
    if (navigator.clipboard) navigator.clipboard.writeText(sel).catch(()=>{});
    active = false;
    box.style.border = "2px solid #69db7c";
    setTimeout(() => { box.remove(); active = true; }, 1500);
  };
  document.addEventListener("click", handler, true);
  console.log("[silly] element picker active! click any element to get its selector (copied to clipboard).");
})();
''',
    }
    for name, code in defaults.items():
        path = os.path.join(SCRIPTS_FOLDER, name)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)

    css_defaults = {
        "dark-mode.css": '''/* silly browser - dark mode */
body { background: #1a1a2e !important; color: #e0e0e0 !important; }
a { color: #7ec8e3 !important; }
img { filter: brightness(0.85); }
''',
        "font-changer.css": '''/* silly browser - comic sans everything */
* { font-family: "Comic Sans MS", "Comic Sans", cursive !important; }
''',
        "rainbow-borders.css": '''/* silly browser - rainbow borders */
* { border: 2px solid; border-image: linear-gradient(45deg, #ff6b6b, #ffa94d, #ffd43b, #69db7c, #4dabf7, #b197fc) 1 !important; }
''',
    }
    for name, code in css_defaults.items():
        path = os.path.join(CSS_FOLDER, name)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)


                f.write(code)


    # also seed any scripts bundled inside the exe that are missing locally
    base = getattr(sys, "_MEIPASS", SCRIPT_DIR)
    bundled_scripts = os.path.join(base, "scripts")
    if os.path.isdir(bundled_scripts):
        for name in os.listdir(bundled_scripts):
            if name.endswith(".js"):
                dst = os.path.join(SCRIPTS_FOLDER, name)
                if not os.path.exists(dst):
                    try:
                        shutil.copy2(os.path.join(bundled_scripts, name), dst)
                    except Exception:
                        pass
    bundled_styles = os.path.join(base, "styles")
    if os.path.isdir(bundled_styles):
        for name in os.listdir(bundled_styles):
            if name.endswith(".css"):
                dst = os.path.join(CSS_FOLDER, name)
                if not os.path.exists(dst):
                    try:
                        shutil.copy2(os.path.join(bundled_styles, name), dst)
                    except Exception:
                        pass


ensure_defaults()

# ── http server ──────────────────────────────────────────────────────────────

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        cfg = load_config()
        enabled_js = cfg.get("enabled_scripts", [])
        enabled_css = cfg.get("enabled_css", [])
        persistent = cfg.get("persistent", False)
        multi = cfg.get("multi_mode", True)

        if self.path.startswith("/inject.js"):
            cfg = load_config()
            rules = load_rules()
            enabled_js = list(cfg.get("enabled_scripts", []))
            # site rules: add scripts for matching domain
            host = ""
            if "?" in self.path:
                for param in self.path.split("?", 1)[1].split("&"):
                    if param.startswith("host="):
                        host = param.split("=", 1)[1]
                        try:
                            host = urllib.parse.unquote(host)
                        except Exception:
                            pass
            if host:
                for domain, scripts in rules.items():
                    if domain.lower() in host.lower():
                        for s in scripts:
                            if s.endswith(".js") and s not in enabled_js:
                                enabled_js.append(s)
            persistent = cfg.get("persistent", False)
            multi = cfg.get("multi_mode", True)
            parts = []
            if persistent:
                parts.append("// silly browser - persistent mode\n")
            target_scripts = enabled_js if multi else [cfg.get("current_script", "default.js")]
            for name in target_scripts:
                path = os.path.join(SCRIPTS_FOLDER, name)
                if os.path.exists(path):
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            parts.append("// === " + name + " ===\n" + f.read() + "\n")
                    except Exception:
                        pass
            body = "\n".join(parts) if parts else "console.log('[silly] nothing enabled');"
            self._send(body, "application/javascript")

        elif self.path.startswith("/inject.css"):
            cfg = load_config()
            rules = load_rules()
            enabled_css = list(cfg.get("enabled_css", []))
            host = ""
            if "?" in self.path:
                for param in self.path.split("?", 1)[1].split("&"):
                    if param.startswith("host="):
                        host = param.split("=", 1)[1]
                        try:
                            host = urllib.parse.unquote(host)
                        except Exception:
                            pass
            if host:
                for domain, scripts in rules.items():
                    if domain.lower() in host.lower():
                        for s in scripts:
                            if s.endswith(".css") and s not in enabled_css:
                                enabled_css.append(s)
            parts = []
            for name in enabled_css:
                path = os.path.join(CSS_FOLDER, name)
                if os.path.exists(path):
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            parts.append("/* === " + name + " === */\n" + f.read() + "\n")
                    except Exception:
                        pass
            body = "\n".join(parts) if parts else "/* nothing enabled */"
            self._send(body, "text/css")

        elif self.path.startswith("/bookmarklet"):
            bm = bookmarklet_code(persistent, multi)
            self._send(bm, "text/plain")

        elif self.path.startswith("/config"):
            self._send(json.dumps(cfg), "application/json")

        elif self.path == "/" or self.path.startswith("/?"):
            self._send(DEMO_PAGE, "text/html; charset=utf-8")

        elif self.path.startswith("/undo"):
            self._send(UNDO_SCRIPT, "application/javascript")

        else:
            self.send_response(404)
            self.end_headers()

    def _send(self, body, ctype):
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


def bookmarklet_code(persistent, multi):
    # builds the bookmarklet that fetches inject.js + inject.css and injects them
    loader = (
        "javascript:(function(){"
        "var s=document.createElement('script');"
        "s.src='http://localhost:8742/inject.js?host='+encodeURIComponent(location.hostname)+'&'+Date.now();"
        "document.body.appendChild(s);"
        "var c=document.createElement('link');"
        "if(!document.querySelector('link[href*=\"inject.css\"]')){"
        "c.rel='stylesheet';c.href='http://localhost:8742/inject.css?host='+encodeURIComponent(location.hostname)+'&'+Date.now();"
        "document.head.appendChild(c);"
        "}"
    )
    if persistent:
        loader += (
            "if(!window.__silly_persist){window.__silly_persist=true;"
            "var o=new MutationObserver(function(){"
            "if(!document.querySelector('script[src*=\"inject.js\"]')){"
            "var s2=document.createElement('script');s2.src='http://localhost:8742/inject.js?host='+encodeURIComponent(location.hostname)+'&'+Date.now();document.body.appendChild(s2);"
            "}"
            "if(!document.querySelector('link[href*=\"inject.css\"]')){"
            "var c2=document.createElement('link');c2.rel='stylesheet';c2.href='http://localhost:8742/inject.css?host='+encodeURIComponent(location.hostname)+'&'+Date.now();document.head.appendChild(c2);"
            "}"
            "});"
            "o.observe(document.body,{childList:true,subtree:true});"
            "window.addEventListener('popstate',function(){setTimeout(function(){var s3=document.createElement('script');s3.src='http://localhost:8742/inject.js?host='+encodeURIComponent(location.hostname)+'&'+Date.now();document.body.appendChild(s3);},100);});"
            "}"
        )
    loader += "console.log('[silly browser] injected!');})();"
    return loader


UNDO_SCRIPT = """// silly browser - undo (removes injected scripts + styles)
(function() {
  document.querySelectorAll('script[src*="inject.js"], link[href*="inject.css"]').forEach(e => e.remove());
  document.querySelectorAll('[data-silly]').forEach(e => e.remove());
  console.log('[silly] undone!');
})();
"""

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
.code{background:#f4f0fa;border:2px solid #e8defd;border-radius:10px;padding:12px;font-family:Consolas,monospace;font-size:12px;margin:12px 0}
</style></head><body>
<h1>silly browser playground</h1>
<p>this page is served by your own silly browser. pick scripts, hit MAKE IT SILLY, then come back here.</p>
<div class="card">
<h2>try it</h2>
<button onclick="alert('the cube says hello')">click me</button>
<button class="hot" onclick="document.body.style.background='#ffe6ef'">recolour the page</button>
<p style="margin-top:20px">if your scripts injected, whatever they do will already be happening on this page.</p>
<div class="code">tip: open devtools (F12) to see console output from your scripts</div>
</div>
</body></html>"""


# ── mascot ───────────────────────────────────────────────────────────────────

class Mascot(tk.Canvas):
    def __init__(self, master, **kw):
        super().__init__(master, width=120, height=110, highlightthickness=0, bd=0,
                         bg=master.cget("bg"), **kw)
        self.t = 0.0
        self.blink = 0.0
        self.happy = 1.0
        self.fill = SKY
        self.edge = SKY_DARK
        self._loop()

    def set_color(self, fill, edge):
        self.fill = fill
        self.edge = edge

    def cheer(self):
        self.happy = 1.0

    def _loop(self):
        self.t += 0.05
        self.blink += 0.03
        if self.blink > 4.0:
            self.blink = 0.0
        self.happy = max(0.35, self.happy - 0.004)
        self.delete("all")
        import math
        bob = math.sin(self.t) * 6
        cx, cy = 60, 52 + bob
        squash = 1 + math.sin(self.t * 2) * 0.05
        w = 46 * squash
        h = 46 / squash
        self.create_oval(cx - 26, 92 - abs(bob) * 0.6, cx + 26, 100 - abs(bob) * 0.6,
                         fill="#e6ddf5", outline="")
        self.create_rectangle(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2,
                              fill=self.fill, outline=self.edge, width=3)
        self.create_oval(cx - w / 2 + 6, cy - h / 2 + 4, cx - w / 2 + 20, cy - h / 2 + 16,
                         fill="#ffffff", outline="")
        eye_h = 11 if (self.blink < 3.4) else 1.5
        self.create_oval(cx - 13, cy - 12, cx - 3, cy - 12 + eye_h, fill=INK, outline="")
        self.create_oval(cx + 3, cy - 12, cx + 13, cy - 12 + eye_h, fill=INK, outline="")
        if self.happy > 0.7:
            self.create_arc(cx - 11, cy, cx + 11, cy + 16, start=200, extent=140,
                            style="arc", outline=INK, width=3)
        elif self.happy > 0.35:
            self.create_arc(cx - 10, cy + 2, cx + 10, cy + 14, start=200, extent=140,
                            style="arc", outline=INK, width=3)
        else:
            self.create_line(cx - 8, cy + 10, cx + 8, cy + 10, fill=INK, width=3)
        if self.happy > 0.7:
            import math as _m
            for i in range(3):
                ph = self.t * 2 + i * 2.1
                hx = cx + _m.cos(ph) * 34
                hy = cy - 26 + _m.sin(ph * 1.3) * 8
                self.create_text(hx, hy, text="❤", fill=self.fill, font=(B_FONT, 11))
        self.after(33, self._loop)


# ── card widget ──────────────────────────────────────────────────────────────

class Card(tk.Frame):
    def __init__(self, master, on_click, **kw):
        super().__init__(master, bg=PANEL, cursor="hand2", **kw)
        self.on_click = on_click
        self.title = ""
        self.sub = ""
        self.tint = PURPLE
        self.selected = False
        self.enabled = False
        self.fname = ""
        self.fkind = "js"
        self._build()
        self.bind("<Button-1>", lambda e: self.on_click(self))
        self.bind("<Button-3>", lambda e: self.on_right_click(self))

    def _build(self):
        self.strip = tk.Frame(self, width=6, bg=self.tint)
        self.strip.pack(side="left", fill="y")
        body = tk.Frame(self, bg=PANEL, padx=10, pady=6)
        body.pack(side="left", fill="both", expand=True)
        self.title_lbl = tk.Label(body, text="", bg=PANEL, fg=INK, font=(B_FONT, 11, "bold"), anchor="w")
        self.title_lbl.pack(fill="x")
        self.sub_lbl = tk.Label(body, text="", bg=PANEL, fg=MUTED, font=(B_FONT, 9), anchor="w")
        self.sub_lbl.pack(fill="x")
        self.chk = tk.Label(body, text="", bg=PANEL, fg=MINT, font=(B_FONT, 9, "bold"), anchor="e")
        self.chk.pack(fill="x")
        for w in (body, self.title_lbl, self.sub_lbl, self.chk):
            w.bind("<Button-1>", lambda e: self.on_click(self))

    def set(self, title, sub, tint, selected, enabled=False, fname="", fkind="js"):
        self.title = title
        self.sub = sub
        self.tint = tint
        self.selected = selected
        self.enabled = enabled
        self.fname = fname
        self.fkind = fkind
        self.strip.configure(bg=tint)
        self.title_lbl.configure(text=title)
        self.sub_lbl.configure(text=sub)
        self.chk.configure(text=("✓ ON" if enabled else ""), fg=(MINT if enabled else MUTED))
        self.configure(highlightbackground=(tint if selected else "#e7dff7"),
                       highlightthickness=(2 if selected else 1))
        for w in (self, self.strip):
            w.configure(bg=(LAVENDER if selected else PANEL))


# ── pill button ──────────────────────────────────────────────────────────────

class Pill(tk.Canvas):
    def __init__(self, master, text, command, fill=PURPLE, dark=PURPLE_DARK,
                 fg=WHITE, width=150, height=46, font=(B_FONT, 12, "bold"), **kw):
        super().__init__(master, width=width, height=height, highlightthickness=0, bd=0,
                         bg=master.cget("bg"), cursor="hand2", **kw)
        self.command = command
        self.text = text
        self.fill = fill
        self.dark = dark
        self.fg = fg
        self.font = font
        self.pw, self.ph = width, height
        self._draw(False)
        self.bind("<ButtonPress-1>", lambda e: self._draw(True))
        self.bind("<ButtonRelease-1>", lambda e: (self._draw(False), self.command()))
        self.bind("<Enter>", lambda e: self.configure(cursor="hand2"))
        self.bind("<Leave>", lambda e: self._draw(False))

    def _draw(self, pressed):
        self.delete("all")
        r = 22
        yoff = 3 if pressed else 0
        fill = self.dark if pressed else self.fill
        self.create_rounded_rect(2, 2 + yoff, self.pw - 2, self.ph - 4 + yoff, r, fill=fill)
        self.create_rounded_rect(2, 2 + yoff, self.pw - 2, self.ph - 8 + yoff, r, fill=self.fill)
        self.create_text(self.pw // 2, (self.ph - 6) // 2 + yoff, text=self.text,
                         fill=self.fg, font=self.font)

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kw):
        self.create_polygon(
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
            x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
            smooth=True, **kw)


# ── main app ─────────────────────────────────────────────────────────────────

class SillyBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("the silly browser v1.3")
        self.root.geometry("1120x740")
        self.root.configure(bg=CREAM)
        self.root.minsize(700, 500)
        self.config = load_config()
        self.rules = load_rules()
        self.cards = []
        self.tab_var = tk.StringVar(value="scripts")
        self.card_inner = None
        self.set_window_icon()
        ensure_defaults()

        self.server = None
        try:
            self.server = Server(("127.0.0.1", PORT), Handler)
            self.server.current_script = self.config.get("current_script", "default.js")
            threading.Thread(target=self.server.serve_forever, daemon=True).start()
        except OSError as e:
            messagebox.showwarning("port is busy",
                "something else is already using port %d (%s).\n\nclose it and restart." % (PORT, e))

        self.current = self.config.get("current_script", "default.js")
        self.search_query = ""
        self._build()
        self.refresh_cards()
        self.refresh_css_cards()
        self.update_status_bar()

    def set_window_icon(self):
        base = getattr(sys, "_MEIPASS", SCRIPT_DIR)
        for candidate in (os.path.join(base, "silly.ico"), os.path.join(SCRIPT_DIR, "silly.ico")):
            if os.path.exists(candidate):
                try:
                    self.root.iconbitmap(candidate)
                    return
                except Exception:
                    pass

    # ── layout ───────────────────────────────────────────────────────────────

    def _build(self):
        top = tk.Frame(self.root, bg=CREAM)
        top.pack(fill="x", side="top", pady=(0, 4))

        self.logo_img = None
        base = getattr(sys, "_MEIPASS", SCRIPT_DIR)
        for candidate in (os.path.join(base, "logo_small.png"), os.path.join(SCRIPT_DIR, "logo_small.png")):
            if os.path.exists(candidate):
                try:
                    self.logo_img = tk.PhotoImage(file=candidate)
                    break
                except Exception:
                    self.logo_img = None

        banner = tk.Canvas(top, height=104, highlightthickness=0, bd=0, bg=CREAM)
        banner.pack(fill="x")
        for i in range(96):
            t = i / 95.0
            r = int(255 + (232 - 255) * t)
            g = int(248 + (222 - 248) * t)
            b = int(238 + (253 - 238) * t)
            banner.create_line(0, i, 2000, i, fill="#%02x%02x%02x" % (r, g, b))
        if self.logo_img is not None:
            banner.create_image(26, 22, anchor="nw", image=self.logo_img)
            banner.create_text(28, 72, anchor="w",
                               text="v1.2 advanced  ✦  js + css injection  ✦  multi-script  ✦  persistent  ✦  site rules",
                               fill=MUTED, font=(B_FONT, 9))
        else:
            banner.create_text(26, 34, anchor="w", text="the silly browser v1.2", fill=INK, font=(H_FONT, 26, "bold"))

        # main area: left sidebar + right editor
        main = tk.Frame(self.root, bg=CREAM)
        main.pack(fill="both", expand=True, padx=18, pady=(10, 14))

        # left sidebar
        sidebar = tk.Frame(main, bg=CREAM, width=270)
        sidebar.pack(side="left", fill="y", padx=(0, 12))
        sidebar.pack_propagate(False)

        # mascot + title
        mrow = tk.Frame(sidebar, bg=CREAM)
        mrow.pack(fill="x", pady=(0, 10))
        self.mascot = Mascot(mrow)
        self.mascot.pack(side="left")
        info = tk.Frame(mrow, bg=CREAM)
        info.pack(side="left", fill="both", expand=True, padx=(6, 0))
        tk.Label(info, text="the silly browser", bg=CREAM, fg=INK, font=(H_FONT, 13, "bold"), wraplength=140).pack(anchor="w")
        tk.Label(info, text="v1.3", bg=CREAM, fg=MUTED, font=(B_FONT, 9)).pack(anchor="w")
        self.plus_badge = tk.Label(info, text="", bg=CREAM, fg="#ffd700", font=(B_FONT, 12, "bold"))
        self.plus_badge.pack(anchor="w")
        self._update_plus_badge()

        # search
        search_row = tk.Frame(sidebar, bg=CREAM)
        search_row.pack(fill="x", pady=(6, 10))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self.on_search())
        se = tk.Entry(search_row, textvariable=self.search_var, font=(B_FONT, 10),
                      bg=PANEL, fg=INK, insertbackground=PURPLE, bd=0, highlightthickness=2,
                      highlightbackground="#e7dff7", highlightcolor=PURPLE)
        se.pack(fill="x", ipady=4, padx=2)
        se.insert(0, "🔍 search scripts...")
        se.bind("<FocusIn>", lambda e: (se.delete(0, tk.END) if se.get().startswith("🔍") else None))
        self.search_entry = se

        # tabs: scripts / styles
        tabrow = tk.Frame(sidebar, bg=CREAM)
        tabrow.pack(fill="x", pady=(0, 8))
        for label, val in [("📜 scripts", "scripts"), ("🎨 styles", "styles")]:
            b = tk.Radiobutton(tabrow, text=label, variable=self.tab_var, value=val,
                               indicatoron=0, bg=LAVENDER, fg=INK, selectcolor=PURPLE,
                               font=(B_FONT, 9, "bold"), bd=0, padx=8, pady=4,
                               command=self.on_tab_change)
            b.pack(side="left", padx=(0, 4))

        # scrollable card list
        card_wrap = tk.Frame(sidebar, bg=CREAM)
        card_wrap.pack(fill="both", expand=True, pady=(0, 4))
        self.card_canvas = tk.Canvas(card_wrap, bg=CREAM, highlightthickness=0, bd=0)
        self.card_canvas.pack(side="left", fill="both", expand=True)
        csb = tk.Scrollbar(card_wrap, orient="vertical", command=self.card_canvas.yview)
        csb.pack(side="right", fill="y")
        self.card_canvas.configure(yscrollcommand=csb.set)
        self.card_inner = tk.Frame(self.card_canvas, bg=CREAM)
        self.card_window = self.card_canvas.create_window((0, 0), window=self.card_inner, anchor="nw")
        self.card_inner.bind("<Configure>", lambda e: self.card_canvas.configure(scrollregion=self.card_canvas.bbox("all")))
        self.card_canvas.bind("<Configure>", lambda e: self.card_canvas.itemconfig(self.card_window, width=e.width))
        self.card_canvas.bind_all("<MouseWheel>", lambda e: self.card_canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        self.cards = []

        # mode toggles
        tog = tk.Frame(sidebar, bg=CREAM)
        tog.pack(fill="x", pady=(10, 6))
        self.multi_var = tk.BooleanVar(value=self.config.get("multi_mode", True))
        self.persist_var = tk.BooleanVar(value=self.config.get("persistent", False))
        tk.Checkbutton(tog, text="stack multiple", variable=self.multi_var, bg=CREAM, fg=INK,
                       font=(B_FONT, 9), activebackground=CREAM,
                       command=self.on_toggle_multi).pack(anchor="w")
        tk.Checkbutton(tog, text="persistent (spa)", variable=self.persist_var, bg=CREAM, fg=INK,
                       font=(B_FONT, 9), activebackground=CREAM,
                       command=self.on_toggle_persist).pack(anchor="w")

        Pill(sidebar, "⭐ silly+", self.show_silly_plus, fill="#ffd700", dark="#e6c200", fg="#5c4400",
             width=280, height=32, font=(B_FONT, 9, "bold")).pack(fill="x", pady=(10, 6))

        Pill(sidebar, "🌐 site rules", self.add_site_rule, fill=LAVENDER, dark="#d5cbec", fg=PURPLE_DARK,
             width=280, height=32, font=(B_FONT, 9, "bold")).pack(fill="x", pady=(10, 6))

        # right side: editor
        right = tk.Frame(main, bg=CREAM)
        right.pack(side="left", fill="both", expand=True)

        # editor title bar
        etitle = tk.Frame(right, bg=PANEL, highlightbackground="#e7dff7", highlightthickness=2)
        etitle.pack(fill="x", pady=(0, 4))
        self.editor_name = tk.Label(etitle, text=self.current, bg=PANEL, fg=INK, font=(B_FONT, 11, "bold"), padx=16, pady=10)
        self.editor_name.pack(side="left")
        self.editor_kind = tk.Label(etitle, text="js", bg=LAVENDER, fg=PURPLE_DARK, font=(B_FONT, 9, "bold"), padx=8, pady=4)
        self.editor_kind.pack(side="right", padx=8)

        # editor
        edit_wrap = tk.Frame(right, bg=PANEL, highlightbackground="#e7dff7", highlightthickness=2)
        edit_wrap.pack(fill="both", expand=True, pady=(0, 4))
        hbar = tk.Scrollbar(edit_wrap, orient="horizontal")
        hbar.pack(side="bottom", fill="x")
        vbar = tk.Scrollbar(edit_wrap, orient="vertical")
        vbar.pack(side="right", fill="y")
        self.editor = tk.Text(edit_wrap, bg="#fffdf8", fg=INK, insertbackground=PURPLE,
                               font=(C_FONT, 12), wrap="none", undo=True, bd=0,
                               highlightthickness=0, padx=12, pady=10,
                               selectbackground="#e8defd", selectforeground=INK)
        self.editor.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        hbar.configure(command=self.editor.xview)
        vbar.configure(command=self.editor.yview)
        self.editor.pack(fill="both", expand=True)
        self.editor.bind("<Control-s>", lambda e: self.save_script())
        self.editor.bind("<Control-a>", lambda e: (self.editor.tag_add("sel", "1.0", "end"), "break"))

        # bottom bar (horizontally scrollable)
        bottom_outer = tk.Frame(self.root, bg=CREAM)
        bottom_outer.pack(fill="x", side="bottom", padx=18, pady=(0, 16))
        bottom_canvas = tk.Canvas(bottom_outer, bg=CREAM, highlightthickness=0, bd=0, height=60)
        bottom_canvas.pack(fill="x")
        bottom_hbar = tk.Scrollbar(bottom_outer, orient="horizontal", command=bottom_canvas.xview)
        bottom_hbar.pack(fill="x")
        bottom_canvas.configure(xscrollcommand=bottom_hbar.set)
        bottom = tk.Frame(bottom_canvas, bg=CREAM)
        bottom_canvas.create_window((0, 0), window=bottom, anchor="nw")
        bottom.bind("<Configure>", lambda e: bottom_canvas.configure(scrollregion=bottom_canvas.bbox("all")))

        Pill(bottom, "📋 copy bookmarklet", self.make_it_silly, fill=PURPLE, dark=PURPLE_DARK,
             width=200, height=52, font=(B_FONT, 12, "bold")).pack(side="left")
        Pill(bottom, "🔄 toggle on/off", self.toggle_enabled_current, fill=LAVENDER, dark="#d5cbec", fg=PURPLE_DARK,
             width=150, height=52, font=(B_FONT, 11, "bold")).pack(side="left", padx=(10, 0))
        Pill(bottom, "update", self.check_for_updates, fill="#e9e3f7", dark="#d5cbec", fg=PURPLE_DARK,
             width=100, height=52, font=(B_FONT, 11, "bold")).pack(side="left", padx=(10, 0))
        Pill(bottom, "🎲 surprise", self.surprise_me, fill=SUN, dark=SUN_DARK, fg="#5c4400",
             width=130, height=52, font=(B_FONT, 11, "bold")).pack(side="left", padx=(10, 0))
        Pill(bottom, "🧪 playground", self.open_playground, fill=MINT, dark=MINT_DARK,
             width=140, height=52, font=(B_FONT, 11, "bold")).pack(side="left", padx=(10, 0))
        Pill(bottom, "↩ undo", self.undo, fill=CORAL, dark=CORAL_DARK,
             width=110, height=52, font=(B_FONT, 11, "bold")).pack(side="left", padx=(10, 0))
        Pill(bottom, "💾 save", self.save_script, fill="#e9e3f7", dark="#d5cbec", fg=PURPLE_DARK,
             width=100, height=52, font=(B_FONT, 11, "bold")).pack(side="left", padx=(10, 0))
        Pill(bottom, "➕ new", self.new_script, fill="#e9e3f7", dark="#d5cbec", fg=PURPLE_DARK,
             width=90, height=52, font=(B_FONT, 11, "bold")).pack(side="left", padx=(10, 0))

        # status bar
        sbar = tk.Frame(self.root, bg=LAVENDER)
        sbar.pack(fill="x", side="bottom")
        self.status = tk.Label(sbar, text="", bg=LAVENDER, fg=INK, font=(B_FONT, 9), anchor="w", padx=16, pady=6)
        self.status.pack(fill="x")

        # keyboard shortcuts
        self.root.bind("<Control-n>", lambda e: self.new_script())
        self.root.bind("<Control-f>", lambda e: self.focus_search())

        # auto-check for updates on startup (silent)
        self.root.after(3000, lambda: self.check_for_updates(silent=True))

        # load initial
        self.load_script(self.current)

    def focus_search(self):
        if hasattr(self, "search_entry") and self.search_entry:
            self.search_entry.focus_set()
            self.search_entry.select_range(0, tk.END)

    # ── data ─────────────────────────────────────────────────────────────────

    def on_search(self):
        q = self.search_var.get().strip().lower()
        if q.startswith("🔍"):
            q = ""
        self.search_query = q
        self.refresh_cards()
        self.refresh_css_cards()

    def on_tab_change(self):
        self.refresh_cards()
        self.refresh_css_cards()

    def refresh_cards(self):
        if self.card_inner is None:
            return
        for c in self.cards:
            c.destroy()
        self.cards = []
        if self.tab_var.get() != "scripts":
            return
        files = script_files()
        q = self.search_query
        if q:
            files = [f for f in files if q in f.lower() or q in f.replace("-", " ").replace("_", " ").lower()]
        for name in files:
            tint, _ = script_colors(name)
            enabled = name in self.config.get("enabled_scripts", [])
            selected = (name == self.current)
            card = Card(self.card_inner, self.on_card_click)
            card.pack(fill="x", pady=4)
            card.set(name.replace(".js", "").replace("-", " ").replace("_", " "),
                     "js script", tint, selected, enabled=enabled, fname=name, fkind="js")
            self.cards.append(card)

    def refresh_css_cards(self):
        if self.card_inner is None:
            return
        # only show css cards when on styles tab
        if self.tab_var.get() != "styles":
            # remove any css cards
            for c in list(self.cards):
                if getattr(c, "fkind", "") == "css":
                    c.destroy()
                    self.cards.remove(c)
            return
        files = css_files()
        q = self.search_query
        if q:
            files = [f for f in files if q in f.lower()]
        for name in files:
            tint, _ = script_colors(name)
            enabled = name in self.config.get("enabled_css", [])
            card = Card(self.card_inner, self.on_css_click)
            card.pack(fill="x", pady=2)
            card.set(name.replace(".css", "").replace("-", " ").replace("_", " "),
                     "css style", tint, False, enabled=enabled, fname=name, fkind="css")
            self.cards.append(card)

    def on_card_click(self, card):
        if self.tab_var.get() == "scripts":
            self.load_script(card.fname)

    def on_right_click(self, card):
        # right-click toggles enabled/disabled
        if card.fkind == "js":
            self.toggle_script(card.fname)
        elif card.fkind == "css":
            self.toggle_css(card.fname)

    def on_css_click(self, card):
        self.toggle_css(card.fname)

    def load_script(self, name):
        path = os.path.join(SCRIPTS_FOLDER, name)
        if not os.path.exists(path):
            path = os.path.join(SCRIPTS_FOLDER, "default.js")
            name = "default.js"
        self.current = name
        self.config["current_script"] = name
        # in single mode, selecting a script enables only that one
        if not self.config.get("multi_mode", True):
            self.config["enabled_scripts"] = [name]
        save_config(self.config)
        with open(path, "r", encoding="utf-8") as f:
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", f.read())
        self.editor_name.configure(text=name)
        self.editor_kind.configure(text="js")
        fill, edge = script_colors(name)
        self.mascot.set_color(fill, edge)
        self.refresh_cards()
        self.update_status_bar()

    def load_css(self, name):
        path = os.path.join(CSS_FOLDER, name)
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", f.read())
        self.editor_name.configure(text=name)
        self.editor_kind.configure(text="css")
        fill, edge = script_colors(name)
        self.mascot.set_color(fill, edge)

    def save_script(self):
        name = self.editor_name.cget("text")
        is_css = name.endswith(".css")
        folder = CSS_FOLDER if is_css else SCRIPTS_FOLDER
        path = os.path.join(folder, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.editor.get("1.0", tk.END).rstrip() + "\n")
        self.mascot.cheer()
        self.status.configure(text="saved %s  ✦" % name)
        self.root.after(2400, lambda: self.status.configure(text=""))
        self.refresh_cards()
        self.refresh_css_cards()

    def new_script(self):
        if self.tab_var.get() == "styles":
            name = simpledialog.askstring("new style", "name (without .css):", parent=self.root)
            if not name:
                return
            name = name.strip().replace(" ", "-") + ".css"
            path = os.path.join(CSS_FOLDER, name)
            if os.path.exists(path):
                messagebox.showinfo("exists", "that style already exists")
                return
            with open(path, "w", encoding="utf-8") as f:
                f.write("/* " + name + " */\nbody { }\n")
            self.load_css(name)
        else:
            name = simpledialog.askstring("new script", "name (without .js):", parent=self.root)
            if not name:
                return
            name = name.strip().replace(" ", "-") + ".js"
            path = os.path.join(SCRIPTS_FOLDER, name)
            if os.path.exists(path):
                messagebox.showinfo("exists", "that script already exists")
                return
            with open(path, "w", encoding="utf-8") as f:
                f.write("// " + name + "\nconsole.log('[silly] " + name + " active!');\n")
            self.load_script(name)
        self.refresh_cards()
        self.refresh_css_cards()

    def delete_current(self):
        name = self.editor_name.cget("text")
        is_css = name.endswith(".css")
        folder = CSS_FOLDER if is_css else SCRIPTS_FOLDER
        if name in ("default.js",):
            messagebox.showinfo("nope", "can't delete the default script")
            return
        if not messagebox.askyesno("delete", "delete %s?" % name):
            return
        try:
            os.remove(os.path.join(folder, name))
        except Exception:
            pass
        if is_css:
            if name in self.config.get("enabled_css", []):
                self.config["enabled_css"].remove(name)
        else:
            if name in self.config.get("enabled_scripts", []):
                self.config["enabled_scripts"].remove(name)
        save_config(self.config)
        if is_css:
            remaining = css_files()
            self.load_css(remaining[0] if remaining else "dark-mode.css")
        else:
            remaining = script_files()
            self.load_script(remaining[0] if remaining else "default.js")
        self.refresh_cards()
        self.refresh_css_cards()

    def toggle_script(self, name):
        enabled = self.config.setdefault("enabled_scripts", [])
        if name in enabled:
            enabled.remove(name)
        else:
            enabled.append(name)
        # ensure at least one
        if not enabled:
            enabled.append("default.js")
        save_config(self.config)
        self.refresh_cards()
        self.update_status_bar()

    def toggle_css(self, name):
        enabled = self.config.setdefault("enabled_css", [])
        if name in enabled:
            enabled.remove(name)
        else:
            enabled.append(name)
        save_config(self.config)
        self.refresh_css_cards()
        self.update_status_bar()

    def toggle_enabled_current(self):
        name = self.editor_name.cget("text")
        if name.endswith(".css"):
            self.toggle_css(name)
        else:
            self.toggle_script(name)

    def on_toggle_multi(self):
        self.config["multi_mode"] = self.multi_var.get()
        save_config(self.config)
        self.update_status_bar()

    def on_toggle_persist(self):
        self.config["persistent"] = self.persist_var.get()
        save_config(self.config)
        self.update_status_bar()

    def make_it_silly(self):
        # save current + enable it + copy bookmarklet
        self.save_script()
        name = self.editor_name.cget("text")
        if name.endswith(".css"):
            if name not in self.config.get("enabled_css", []):
                self.config.setdefault("enabled_css", []).append(name)
        else:
            if name not in self.config.get("enabled_scripts", []):
                self.config.setdefault("enabled_scripts", []).append(name)
        save_config(self.config)
        self.refresh_cards()
        self.refresh_css_cards()
        bm = None
        try:
            import urllib.request
            with urllib.request.urlopen("http://localhost:%d/bookmarklet" % PORT, timeout=3) as r:
                bm = r.read().decode("utf-8")
        except Exception:
            pass
        if bm:
            self.root.clipboard_clear()
            self.root.clipboard_append(bm)
            self.root.update()  # ensure clipboard is flushed
            self.mascot.cheer()
            self.status.configure(text="bookmarklet copied! paste it as a bookmark  ✦")
        else:
            self.status.configure(text="saved + enabled (server not reachable)  ✦")
        self.root.after(3200, lambda: self.status.configure(text=""))

    def surprise_me(self):
        files = script_files() + css_files()
        if not files:
            return
        pick = random.choice(files)
        if pick.endswith(".css"):
            self.load_css(pick)
        else:
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

    def undo(self):
        if self.server is None:
            self.status.configure(text="server is not running  ✦")
            return
        # fetch the undo script and copy it to clipboard
        try:
            import urllib.request
            with urllib.request.urlopen("http://localhost:%d/undo" % PORT, timeout=3) as r:
                undo_script = r.read().decode("utf-8")
            self.root.clipboard_clear()
            self.root.clipboard_append(undo_script)
            self.root.update()
            self.mascot.cheer()
            self.status.configure(text="undo script copied! paste as bookmark to remove injected stuff  ✦")
        except Exception:
            self.status.configure(text="server not reachable  ✦")
        self.root.after(3200, lambda: self.status.configure(text=""))

    def update_status_bar(self):
        enabled_js = self.config.get("enabled_scripts", [])
        enabled_css = self.config.get("enabled_css", [])
        multi = self.config.get("multi_mode", True)
        persist = self.config.get("persistent", False)
        parts = []
        if multi:
            parts.append("%d js" % len(enabled_js))
        else:
            parts.append("single: %s" % self.config.get("current_script", "default.js"))
        if enabled_css:
            parts.append("%d css" % len(enabled_css))
        if persist:
            parts.append("persistent")
        self.status.configure(text="enabled: " + ", ".join(parts) + "  ✦  localhost:%d  ✦  v%s" % (PORT, CURRENT_VERSION))

    def _update_plus_badge(self):
        if self.config.get("silly_plus"):
            self.plus_badge.configure(text="⭐ silly+ supporter")
        else:
            self.plus_badge.configure(text="")

    def check_for_updates(self, silent=False):
        import urllib.request, json, re
        try:
            url = "https://api.github.com/repos/%s/releases/latest" % GITHUB_REPO
            req = urllib.request.Request(url, headers={"User-Agent": "silly-browser/%s" % CURRENT_VERSION})
            with urllib.request.urlopen(req, timeout=8) as r:
                data = json.loads(r.read().decode("utf-8"))
            tag = data.get("tag_name", "").lstrip("v")
            # compare versions
            def parse(v):
                return tuple(int(x) for x in re.findall(r"\d+", v)[:3])
            if parse(tag) > parse(CURRENT_VERSION):
                # find the exe asset
                exe_url = None
                for a in data.get("assets", []):
                    if a["name"] == "silly-browser.exe":
                        exe_url = a["browser_download_url"]
                        break
                if exe_url:
                    if messagebox.askyesno("update available",
                            "a new version (v%s) is available!\n\nupdate now?" % tag):
                        self._do_update(exe_url, tag)
                elif not silent:
                    messagebox.showinfo("update", "new version v%s found but no exe asset" % tag)
            elif not silent:
                messagebox.showinfo("up to date", "you're on the latest version (v%s)" % CURRENT_VERSION)
        except Exception as e:
            if not silent:
                messagebox.showwarning("update check failed", str(e))

    def _do_update(self, exe_url, tag):
        import urllib.request, os, sys, subprocess
        tmp_dir = os.path.join(os.environ.get("TEMP", "."), "silly_update")
        os.makedirs(tmp_dir, exist_ok=True)
        new_exe = os.path.join(tmp_dir, "silly-browser-new.exe")
        self.status.configure(text="downloading update...")
        self.root.update()
        try:
            urllib.request.urlretrieve(exe_url, new_exe)
        except Exception as e:
            messagebox.showerror("download failed", str(e))
            return
        # write a batch updater that waits for this process to exit, replaces exe, restarts
        current_exe = os.path.abspath(sys.argv[0])
        bat = os.path.join(tmp_dir, "update.bat")
        with open(bat, "w") as f:
            f.write("@echo off\n")
            f.write("echo waiting for silly browser to close...\n")
            f.write(":wait\n")
            f.write("tasklist /FI \"IMAGENAME eq silly-browser.exe\" 2>NUL | find /I \"silly-browser.exe\" >NUL\n")
            f.write("if not errorlevel 1 (timeout /t 1 /nobreak >NUL & goto wait)\n")
            f.write("echo replacing...\n")
            f.write('copy /Y "%s" "%s"\n' % (new_exe, current_exe))
            f.write('echo restarting...\n')
            f.write('start "" "%s"\n' % current_exe)
            f.write('del "%s"\n' % bat)
        # launch updater and exit
        subprocess.Popen(["cmd", "/c", bat], creationflags=0x00000008)  # DETACHED_PROCESS
        self.root.destroy()
        sys.exit(0)

    # site rules
    def add_site_rule(self):
        domain = simpledialog.askstring("site rule", "domain (e.g. example.com):", parent=self.root)
        if not domain:
            return
        domain = domain.strip().lower()
        scripts = simpledialog.askstring("site rule", "scripts to enable (comma separated, e.g. dark-mode.css,ad-remover.js):", parent=self.root)
        if not scripts:
            return
        self.rules[domain] = [s.strip() for s in scripts.split(",") if s.strip()]
        save_rules(self.rules)
        self.status.configure(text="rule added for %s  ✦" % domain)
        self.root.after(2400, lambda: self.status.configure(text=""))

    def show_silly_plus(self):
        # create a toplevel window for silly+ verification
        win = tk.Toplevel(self.root)
        win.title("silly+ supporter")
        win.geometry("420x380")
        win.configure(bg=CREAM)
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text="⭐ silly+ supporter", bg=CREAM, fg=INK, font=(H_FONT, 18, "bold")).pack(pady=(16, 4))
        tk.Label(win, text="support the silly team on github to unlock silly+", bg=CREAM, fg=MUTED, font=(B_FONT, 10)).pack()

        # username input
        tk.Label(win, text="your github username:", bg=CREAM, fg=INK, font=(B_FONT, 10, "bold")).pack(anchor="w", padx=20, pady=(12, 2))
        user_var = tk.StringVar(value=self.config.get("github_user", ""))
        entry = tk.Entry(win, textvariable=user_var, font=(B_FONT, 11), bg=PANEL, fg=INK, bd=0, highlightthickness=2, highlightbackground="#e7dff7", highlightcolor=PURPLE)
        entry.pack(fill="x", padx=20, ipady=4)
        # save username whenever it changes
        def _save_user(*a):
            self.config["github_user"] = user_var.get().strip()
            save_config(self.config)
        user_var.trace_add("write", _save_user)

        # status labels
        star_lbl = tk.Label(win, text="⭐ starred repo: checking...", bg=CREAM, fg=MUTED, font=(B_FONT, 10))
        star_lbl.pack(anchor="w", padx=20, pady=(8, 0))
        follow_lbl = tk.Label(win, text="👁️ following org: checking...", bg=CREAM, fg=MUTED, font=(B_FONT, 10))
        follow_lbl.pack(anchor="w", padx=20, pady=(2, 0))

        result_lbl = tk.Label(win, text="", bg=CREAM, fg=INK, font=(B_FONT, 11, "bold"))
        result_lbl.pack(pady=(12, 4))

        def check():
            import urllib.request, json
            user = user_var.get().strip()
            if not user:
                result_lbl.configure(text="enter a username first", fg=CORAL)
                return
            self.config["github_user"] = user
            save_config(self.config)
            star_lbl.configure(text="⭐ starred repo: checking...", fg=MUTED)
            follow_lbl.configure(text="👁️ following org: checking...", fg=MUTED)
            result_lbl.configure(text="checking...", fg=MUTED)
            win.update()

            starred = False
            following = False
            try:
                # check if user has starred the repo (via their starred list)
                url = "https://api.github.com/users/%s/starred?per_page=100" % user
                req = urllib.request.Request(url, headers={"User-Agent": "silly-browser"})
                with urllib.request.urlopen(req, timeout=8) as r:
                    starred_repos = json.loads(r.read().decode())
                starred = any(r.get("full_name", "").lower() == "the-silly-team/silly-browser" for r in starred_repos)
            except Exception as e:
                star_lbl.configure(text="⭐ starred repo: error (%s)" % str(e)[:30], fg=CORAL)
            try:
                # check if user follows the org
                url = "https://api.github.com/users/%s/following/the-silly-team" % user
                req = urllib.request.Request(url, headers={"User-Agent": "silly-browser"})
                try:
                    with urllib.request.urlopen(req, timeout=8) as r:
                        following = (r.status == 204)
                except urllib.error.HTTPError as e:
                    following = (e.code == 204)
            except Exception as e:
                follow_lbl.configure(text="👁️ following org: error", fg=CORAL)

            star_lbl.configure(text="⭐ starred repo: " + ("✓ yes" if starred else "✗ no"), fg=(MINT if starred else CORAL))
            follow_lbl.configure(text="👁️ following org: " + ("✓ yes" if following else "✗ no"), fg=(MINT if following else CORAL))

            if starred and following:
                self.config["silly_plus"] = True
                save_config(self.config)
                result_lbl.configure(text="you're a silly+ supporter! 🎉", fg=MINT)
                self.mascot.cheer()
                # enable premium scripts
                for s in ["element-picker.js"]:
                    if s not in self.config.get("enabled_scripts", []):
                        self.config.setdefault("enabled_scripts", []).append(s)
                save_config(self.config)
                self.refresh_cards()
                self.update_status_bar()
            else:
                self.config["silly_plus"] = False
                save_config(self.config)
                result_lbl.configure(text="star + follow to unlock silly+", fg=CORAL)

        tk.Button(win, text="check", font=(B_FONT, 11, "bold"), bg=PURPLE, fg="white", bd=0, padx=20, pady=6,
                  command=check).pack(pady=(8, 4))

        # instructions
        instr = tk.Frame(win, bg=CREAM)
        instr.pack(fill="x", padx=20, pady=(8, 4))
        tk.Label(instr, text="1. star github.com/the-silly-team/silly-browser", bg=CREAM, fg=INK, font=(B_FONT, 9)).pack(anchor="w")
        tk.Label(instr, text="2. follow github.com/the-silly-team", bg=CREAM, fg=INK, font=(B_FONT, 9)).pack(anchor="w")
        tk.Label(instr, text="3. enter your username above and click check", bg=CREAM, fg=INK, font=(B_FONT, 9)).pack(anchor="w")

        # links
        link_row = tk.Frame(win, bg=CREAM)
        link_row.pack(pady=(4, 8))
        tk.Button(link_row, text="⭐ star repo", font=(B_FONT, 9), bg=LAVENDER, fg=PURPLE_DARK, bd=0, padx=12, pady=4,
                  command=lambda: webbrowser.open("https://github.com/the-silly-team/silly-browser")).pack(side="left", padx=4)
        tk.Button(link_row, text="👁️ follow org", font=(B_FONT, 9), bg=LAVENDER, fg=PURPLE_DARK, bd=0, padx=12, pady=4,
                  command=lambda: webbrowser.open("https://github.com/the-silly-team")).pack(side="left", padx=4)

        # ── key-based verification ──
        tk.Label(win, text="-- or enter a key --", bg=CREAM, fg=MUTED, font=(B_FONT, 9)).pack(pady=(8, 4))

        key_var = tk.StringVar(value=self.config.get("silly_key", ""))
        key_entry = tk.Entry(win, textvariable=key_var, font=(B_FONT, 11), bg=PANEL, fg=INK, bd=0, highlightthickness=2, highlightbackground="#e7dff7", highlightcolor=PURPLE)
        key_entry.pack(fill="x", padx=20, ipady=4)
        def _save_key(*a):
            self.config["silly_key"] = key_var.get().strip()
            save_config(self.config)
        key_var.trace_add("write", _save_key)

        key_result = tk.Label(win, text="", bg=CREAM, fg=INK, font=(B_FONT, 10, "bold"))
        key_result.pack(pady=(4, 0))

        def check_key():
            key = key_var.get().strip()
            if not key:
                key_result.configure(text="enter a key first", fg=CORAL)
                return
            self.config["silly_key"] = key
            save_config(self.config)
            import urllib.request, json
            gist_url = "https://gist.githubusercontent.com/iluxz/placeholder/raw/keys.json"
            valid_keys = []
            try:
                req = urllib.request.Request(gist_url, headers={"User-Agent": "silly-browser"})
                with urllib.request.urlopen(req, timeout=8) as r:
                    valid_keys = json.loads(r.read().decode())
            except Exception:
                if key.startswith("SILLY-"):
                    valid_keys = [key]
            if key in valid_keys:
                self.config["silly_plus"] = True
                save_config(self.config)
                key_result.configure(text="key accepted! silly+ unlocked", fg=MINT)
                self.mascot.cheer()
                self._update_plus_badge()
                self.update_status_bar()
            else:
                key_result.configure(text="invalid key", fg=CORAL)

        tk.Button(win, text="verify key", font=(B_FONT, 10, "bold"), bg=PURPLE, fg="white", bd=0, padx=16, pady=4,
                  command=check_key).pack(pady=(4, 8))

        # ── github oauth (device flow) ──
        tk.Label(win, text="-- or login with github --", bg=CREAM, fg=MUTED, font=(B_FONT, 9)).pack(pady=(8, 4))

        oauth_result = tk.Label(win, text="", bg=CREAM, fg=INK, font=(B_FONT, 10, "bold"))
        oauth_result.pack(pady=(4, 0))

        def github_login():
            import urllib.request, json, time, threading, urllib.parse
            client_id = self.config.get("github_client_id", "")
            if not client_id:
                client_id = simpledialog.askstring("github oauth", "enter your github oauth app client_id:", parent=win)
                if not client_id:
                    return
                self.config["github_client_id"] = client_id
                save_config(self.config)

            oauth_result.configure(text="requesting device code...", fg=MUTED)
            win.update()

            def do_oauth():
                try:
                    data = urllib.parse.urlencode({"client_id": client_id, "scope": "read:user"}).encode()
                    req = urllib.request.Request("https://github.com/login/device/code", data=data, headers={"Accept": "application/json"})
                    with urllib.request.urlopen(req, timeout=10) as r:
                        resp = json.loads(r.read().decode())
                    device_code = resp["device_code"]
                    user_code = resp["user_code"]
                    verify_url = resp["verification_uri"]
                    interval = resp.get("interval", 5)

                    win.after(0, lambda: oauth_result.configure(text="go to %s and enter code: %s" % (verify_url, user_code), fg=INK))
                    webbrowser.open(verify_url)

                    token = None
                    for _ in range(60):
                        time.sleep(interval)
                        data = urllib.parse.urlencode({"client_id": client_id, "device_code": device_code, "grant_type": "urn:ietf:params:oauth:grant-type:device_code"}).encode()
                        req = urllib.request.Request("https://github.com/login/oauth/access_token", data=data, headers={"Accept": "application/json"})
                        with urllib.request.urlopen(req, timeout=10) as r:
                            resp = json.loads(r.read().decode())
                        if "access_token" in resp:
                            token = resp["access_token"]
                            break
                        if resp.get("error") == "authorization_pending":
                            continue
                        if resp.get("error"):
                            raise Exception(resp.get("error_description", resp["error"]))

                    if not token:
                        raise Exception("timed out waiting for authorization")

                    headers = {"Authorization": "token " + token, "User-Agent": "silly-browser"}
                    starred = False
                    following = False
                    try:
                        req = urllib.request.Request("https://api.github.com/user/starred/the-silly-team/silly-browser", headers=headers)
                        with urllib.request.urlopen(req, timeout=8) as r:
                            starred = (r.status == 204)
                    except urllib.error.HTTPError as e:
                        starred = (e.code == 204)
                    try:
                        req = urllib.request.Request("https://api.github.com/user/following/the-silly-team", headers=headers)
                        with urllib.request.urlopen(req, timeout=8) as r:
                            following = (r.status == 204)
                    except urllib.error.HTTPError as e:
                        following = (e.code == 204)

                    req = urllib.request.Request("https://api.github.com/user", headers=headers)
                    with urllib.request.urlopen(req, timeout=8) as r:
                        user_data = json.loads(r.read().decode())
                    username = user_data.get("login", "")

                    if starred and following:
                        self.config["github_user"] = username
                        self.config["silly_plus"] = True
                        save_config(self.config)
                        win.after(0, lambda: oauth_result.configure(text="welcome %s! silly+ unlocked" % username, fg=MINT))
                        win.after(0, self.mascot.cheer)
                        win.after(0, self._update_plus_badge)
                        win.after(0, self.update_status_bar)
                    else:
                        msg = "missing: "
                        if not starred: msg += "star "
                        if not following: msg += "follow"
                        win.after(0, lambda: oauth_result.configure(text=msg.strip(), fg=CORAL))
                except Exception as e:
                    win.after(0, lambda: oauth_result.configure(text="error: %s" % str(e)[:60], fg=CORAL))

            threading.Thread(target=do_oauth, daemon=True).start()

        tk.Button(win, text="login with github", font=(B_FONT, 10, "bold"), bg="#24292e", fg="white", bd=0, padx=16, pady=4,
                  command=github_login).pack(pady=(4, 8))


        # auto-check on open
        if self.config.get("github_user"):
            win.after(500, check)

        # ── key-based verification ──
        tk.Label(win, text="-- or enter a key --", bg=CREAM, fg=MUTED, font=(B_FONT, 9)).pack(pady=(8, 4))

        key_var = tk.StringVar(value=self.config.get("silly_key", ""))
        key_entry = tk.Entry(win, textvariable=key_var, font=(B_FONT, 11), bg=PANEL, fg=INK, bd=0, highlightthickness=2, highlightbackground="#e7dff7", highlightcolor=PURPLE)
        key_entry.pack(fill="x", padx=20, ipady=4)

        key_result = tk.Label(win, text="", bg=CREAM, fg=INK, font=(B_FONT, 10, "bold"))
        key_result.pack(pady=(4, 0))

        def check_key():
            key = key_var.get().strip()
            if not key:
                key_result.configure(text="enter a key first", fg=CORAL)
                return
            self.config["silly_key"] = key
            save_config(self.config)
            import urllib.request, json
            gist_url = "https://gist.githubusercontent.com/iluxz/placeholder/raw/keys.json"
            valid_keys = []
            try:
                req = urllib.request.Request(gist_url, headers={"User-Agent": "silly-browser"})
                with urllib.request.urlopen(req, timeout=8) as r:
                    valid_keys = json.loads(r.read().decode())
            except Exception:
                if key.startswith("SILLY-"):
                    valid_keys = [key]
            if key in valid_keys:
                self.config["silly_plus"] = True
                save_config(self.config)
                key_result.configure(text="key accepted! silly+ unlocked", fg=MINT)
                self.mascot.cheer()
                self._update_plus_badge()
                self.update_status_bar()
            else:
                key_result.configure(text="invalid key", fg=CORAL)

        tk.Button(win, text="verify key", font=(B_FONT, 10, "bold"), bg=PURPLE, fg="white", bd=0, padx=16, pady=4,
                  command=check_key).pack(pady=(4, 8))


# ── server ───────────────────────────────────────────────────────────────────

class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    root = tk.Tk()
    app = SillyBrowser(root)
    root.mainloop()


if __name__ == "__main__":
    main()
