"""
164x314 left-panel image for inno setup classic wizard style
blue->black gradient + the cube mascot
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 164, 314
OUT = r"D:\OpenCode\silly-browser\setup_panel.bmp"
ICON = r"D:\OpenCode\silly-browser\silly.ico"

BLUE_TOP = (0, 0, 255)
BLUE_MID = (0, 0, 128)
BLACK = (0, 0, 0)

img = Image.new("RGB", (W, H), BLUE_TOP)
d = ImageDraw.Draw(img)
for y in range(H):
    t = y / max(1, H - 1)
    if t < 0.30:
        u = t / 0.30
        col = tuple(int(BLUE_TOP[c] + (BLUE_MID[c] - BLUE_TOP[c]) * u) for c in range(3))
    else:
        u = (t - 0.30) / 0.70
        col = tuple(int(BLUE_MID[c] + (BLACK[c] - BLUE_MID[c]) * u) for c in range(3))
    d.line([0, y, W, y], fill=col)

# cube
try:
    ico = Image.open(ICON)
    ico = ico.convert("RGBA")
    ico = ico.resize((96, 96), Image.LANCZOS)
    img.paste(ico, ((W - 96) // 2, 60), ico)
except Exception as e:
    print("icon failed:", e)

# title
try:
    f = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 13)
except Exception:
    f = ImageFont.load_default()
d.text((W // 2, 180), "Silly", font=f, fill=(255, 255, 255), anchor="mm")
d.text((W // 2, 198), "Browser", font=f, fill=(255, 255, 255), anchor="mm")

img.save(OUT)
print("wrote", OUT, img.size)
