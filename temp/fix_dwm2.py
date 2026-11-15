s = open(r"D:\OpenCode\silly-browser\silly_browser.py", encoding="utf-8").read()
# find the __init__ overrideredirect section
old = '''        self.root.minsize(800, 600)
        self.root.overrideredirect(True)
        self._setup_custom_titlebar()
        # try to restore taskbar visibility
        try:
            self.root.wm_attributes("-toolwindow", False)
        except Exception:
            pass
        self.config = load_config()'''
new = '''        self.root.minsize(800, 600)
        self.config = load_config()
        # style the OS title bar using DWM (keeps taskbar visibility)
        self.root.after(100, self._style_os_titlebar)'''
assert old in s, "old not found"
s = s.replace(old, new, 1)

# remove _setup_custom_titlebar and _fix_taskbar, _create_taskbar_proxy methods
# find from _create_taskbar_proxy or _fix_taskbar or _setup_custom_titlebar
for method_name in ["_create_taskbar_proxy", "_fix_taskbar", "_setup_custom_titlebar"]:
    while True:
        i = s.find("    def %s(self):" % method_name)
        if i == -1:
            break
        j = s.find("    def ", i + 10)
        if j == -1:
            j = s.find("    # --", i + 10)
        if j == -1:
            j = len(s)
        s = s[:i] + s[j:]
        print("removed", method_name)

# add _style_os_titlebar method before set_window_icon
old2 = "    def set_window_icon(self):"
new2 = '''    def _style_os_titlebar(self):
        # use DWM to color the OS title bar (keeps taskbar + alt-tab)
        try:
            import ctypes
            hwnd = self.root.winfo_id()

            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            DWMWA_CAPTION_COLOR = 35
            DWMWA_TEXT_COLOR = 36

            dark = 1 if self.config.get("dark_mode") else 0
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(ctypes.c_int(dark)), ctypes.sizeof(ctypes.c_int)
            )

            # purple caption color
            caption_color = 0x00F0B88B  # #8b6cf0 in BGR
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_CAPTION_COLOR,
                ctypes.byref(ctypes.c_int(caption_color)), ctypes.sizeof(ctypes.c_int)
            )

            # white text
            text_color = 0x00FFFFFF
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_TEXT_COLOR,
                ctypes.byref(ctypes.c_int(text_color)), ctypes.sizeof(ctypes.c_int)
            )
        except Exception as e:
            print("dwm style failed:", e)

    def set_window_icon(self):'''
assert old2 in s
s = s.replace(old2, new2, 1)

open(r"D:\OpenCode\silly-browser\silly_browser.py", "w", encoding="utf-8").write(s)
print("done")
