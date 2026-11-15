"""
the silly browser - custom installer (windows 3.1 style)
self-contained: bundles the app exe + scripts + assets inside itself
"""
import os
import sys
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# ── paths (pyinstaller frozen or dev) ────────────────────────────────────────

BASE = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
APP_NAME = "the silly browser"
INSTALL_DIR_DEFAULT = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "Programs", "silly-browser")
START_MENU = os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs")

# ── palette (windows 3.1) ───────────────────────────────────────────────────

BEIGE_HI = "#f3eed8"
BEIGE_LO = "#b0a888"
BEIGE_MID = "#d4cdb2"
BLUE_TOP = "#0000ff"
BLUE_MID = "#000080"
BLACK = "#000000"
DIALOG_GRAY = "#c0c0c0"
WHITE = "#ffffff"

W, H = 520, 340
FRAME = 22


def shear_text(canvas, text, x, y, size=26, color=WHITE):
    """draw italic-ish bold title with shadow, win3.1 style"""
    # shadow
    canvas.create_text(x + 3, y + 3, text=text, fill="#000000",
                      font=("Arial", size, "bold italic"), anchor="nw")
    canvas.create_text(x, y, text=text, fill=color,
                      font=("Arial", size, "bold italic"), anchor="nw")


class Installer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Setup - the silly browser 0.1.0")
        self.geometry(f"{W}x{H}")
        self.resizable(False, False)
        self.configure(bg=BEIGE_MID)

        self.install_dir = INSTALL_DIR_DEFAULT
        self.desktop_shortcut = tk.BooleanVar(value=False)
        self.state = "welcome"  # welcome | installing | done
        self._build()

    # ── layout ───────────────────────────────────────────────────────────────

    def _build(self):
        self.canvas = tk.Canvas(self, width=W, height=H, highlightthickness=0, bd=0, bg=BEIGE_MID)
        self.canvas.pack(fill="both", expand=True)

        # outer beige bevel frame
        for i in range(3):
            self.canvas.create_line(i, i, W - 1 - i, i, fill=BEIGE_HI)
            self.canvas.create_line(i, i, i, H - 1 - i, fill=BEIGE_HI)
            self.canvas.create_line(i, H - 1 - i, W - 1 - i, H - 1 - i, fill=BEIGE_LO)
            self.canvas.create_line(W - 1 - i, i, W - 1 - i, H - 1 - i, fill=BEIGE_LO)

        # blue -> black gradient (inner area)
        grad = tk.Canvas(self.canvas, width=W - FRAME * 2, height=H - FRAME * 2,
                         highlightthickness=0, bd=0)
        self.canvas.create_window(FRAME, FRAME, window=grad, anchor="nw")
        for y in range(H - FRAME * 2):
            t = y / max(1, H - FRAME * 2 - 1)
            if t < 0.30:
                u = t / 0.30
                r = int(0 + (0 - 0) * u)
                g = int(0 + (0 - 0) * u)
                b = int(255 + (128 - 255) * u)
            else:
                u = (t - 0.30) / 0.70
                r = int(0 + (0 - 0) * u)
                g = int(0 + (0 - 0) * u)
                b = int(128 + (0 - 128) * u)
            grad.create_line(0, y, W - FRAME * 2, y, fill=f"#{r:02x}{g:02x}{b:02x}")

        # title
        shear_text(self.canvas, "Silly Browser Setup", FRAME + 12, FRAME + 8, size=22)

        # dialog box
        self.dlg_x = (W - 400) // 2
        self.dlg_y = 90
        self.dlg_w, self.dlg_h = 400, 200
        # shadow
        self.canvas.create_rectangle(self.dlg_x + 4, self.dlg_y + 4,
                                    self.dlg_x + self.dlg_w + 4, self.dlg_y + self.dlg_h + 4,
                                    fill="#000060", outline="")
        # title bar
        self.canvas.create_rectangle(self.dlg_x, self.dlg_y, self.dlg_x + self.dlg_w, self.dlg_y + 24,
                                    fill=BLUE_MID, outline="")
        self.canvas.create_text(self.dlg_x + self.dlg_w // 2, self.dlg_y + 12, text="Windows Setup",
                                fill=WHITE, font=("Arial", 11, "bold"), anchor="center")
        # body
        self.canvas.create_rectangle(self.dlg_x, self.dlg_y + 24, self.dlg_x + self.dlg_w,
                                    self.dlg_y + self.dlg_h, fill=DIALOG_GRAY, outline="")
        # raised border (body)
        for i in range(2):
            self.canvas.create_line(self.dlg_x + i, self.dlg_y + 24 + i,
                                    self.dlg_x + self.dlg_w - i, self.dlg_y + 24 + i, fill=WHITE)
            self.canvas.create_line(self.dlg_x + i, self.dlg_y + 24 + i,
                                    self.dlg_x + i, self.dlg_y + self.dlg_h - i, fill=WHITE)
            self.canvas.create_line(self.dlg_x + i, self.dlg_y + self.dlg_h - i,
                                    self.dlg_x + self.dlg_w - i, self.dlg_y + self.dlg_h - i, fill="#404040")
            self.canvas.create_line(self.dlg_x + self.dlg_w - i, self.dlg_y + 24 + i,
                                    self.dlg_x + self.dlg_w - i, self.dlg_y + self.dlg_h - i, fill="#404040")

        # cube mascot in dialog
        try:
            from PIL import Image, ImageTk
            ico = Image.open(os.path.join(BASE, "silly.ico")).convert("RGBA")
            ico = ico.resize((48, 48), Image.LANCZOS)
            self._cube_img = ImageTk.PhotoImage(ico)
            self.canvas.create_image(self.dlg_x + 26, self.dlg_y + 56, image=self._cube_img, anchor="nw")
        except Exception:
            pass

        self.content_frame = tk.Frame(self.canvas, bg=DIALOG_GRAY)
        self.canvas.create_window(self.dlg_x + 88, self.dlg_y + 40, window=self.content_frame,
                                 anchor="nw", width=self.dlg_w - 100, height=self.dlg_h - 90)

        self._show_welcome()

    # ── screens ──────────────────────────────────────────────────────────────

    def _clear_content(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

    def _show_welcome(self):
        self._clear_content()
        tk.Label(self.content_frame, text="Setup will install the silly browser\non this computer.",
                 bg=DIALOG_GRAY, fg=BLACK, font=("Arial", 10, "bold"), justify="left").pack(anchor="w", pady=(0, 8))
        tk.Label(self.content_frame, text="You will be able to run it from the\nStart Menu afterwards.",
                 bg=DIALOG_GRAY, fg=BLACK, font=("Arial", 9), justify="left").pack(anchor="w", pady=(0, 8))

        tk.Label(self.content_frame, text="Install to:", bg=DIALOG_GRAY, fg=BLACK,
                 font=("Arial", 9, "bold")).pack(anchor="w")
        dir_row = tk.Frame(self.content_frame, bg=DIALOG_GRAY)
        dir_row.pack(fill="x", pady=(2, 8))
        tk.Entry(dir_row, textvariable=tk.StringVar(value=self.install_dir), font=("Arial", 9),
                 state="readonly", width=28).pack(side="left", fill="x", expand=True)
        tk.Button(dir_row, text="...", font=("Arial", 9), width=3,
                  command=self._browse).pack(side="left", padx=(4, 0))

        tk.Checkbutton(self.content_frame, text="Create desktop shortcut", variable=self.desktop_shortcut,
                       bg=DIALOG_GRAY, fg=BLACK, font=("Arial", 9), activebackground=DIALOG_GRAY).pack(anchor="w")

        # buttons
        btn_row = tk.Frame(self.canvas, bg=DIALOG_GRAY)
        self.canvas.create_window(self.dlg_x + self.dlg_w - 10, self.dlg_y + self.dlg_h - 12,
                                 window=btn_row, anchor="se")
        tk.Button(btn_row, text="Cancel", font=("Arial", 9), width=9,
                  command=self.destroy).pack(side="left", padx=(0, 6))
        tk.Button(btn_row, text="Install", font=("Arial", 9, "bold"), width=9,
                  command=self._start_install).pack(side="left")

    def _browse(self):
        from tkinter import filedialog
        d = filedialog.askdirectory(initialdir=self.install_dir, title="Choose install folder")
        if d:
            self.install_dir = d
            self._show_welcome()

    def _start_install(self):
        self.state = "installing"
        self._clear_content()
        tk.Label(self.content_frame, text="Installing the silly browser...",
                 bg=DIALOG_GRAY, fg=BLACK, font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 8))
        self.progress = ttk.Progressbar(self.content_frame, length=260, mode="determinate")
        self.progress.pack(fill="x", pady=(4, 8))
        self.status_label = tk.Label(self.content_frame, text="Preparing...",
                                    bg=DIALOG_GRAY, fg=BLACK, font=("Arial", 9))
        self.status_label.pack(anchor="w")
        threading.Thread(target=self._do_install, daemon=True).start()

    def _do_install(self):
        try:
            os.makedirs(self.install_dir, exist_ok=True)
            files_to_copy = [
                ("silly-browser.exe", "silly-browser.exe"),
                ("logo.png", "logo.png"),
                ("README.md", "README.md"),
            ]
            # scripts folder
            src_scripts = os.path.join(BASE, "scripts")
            dst_scripts = os.path.join(self.install_dir, "scripts")
            os.makedirs(dst_scripts, exist_ok=True)

            total = len(files_to_copy) + len(os.listdir(src_scripts)) if os.path.isdir(src_scripts) else len(files_to_copy)
            done = 0

            for src_name, dst_name in files_to_copy:
                self._set_status(f"Copying {src_name}...")
                shutil.copy2(os.path.join(BASE, src_name), os.path.join(self.install_dir, dst_name))
                done += 1
                self._set_progress(done / total * 100)

            if os.path.isdir(src_scripts):
                for name in os.listdir(src_scripts):
                    self._set_status(f"Copying scripts/{name}...")
                    shutil.copy2(os.path.join(src_scripts, name), os.path.join(dst_scripts, name))
                    done += 1
                    self._set_progress(done / total * 100)

            self._set_status("Creating shortcuts...")
            self._create_shortcuts()
            self._register_uninstaller()

            self._set_progress(100)
            self._set_status("Done!")
            self.after(400, self._show_done)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Install failed", str(e)))
            self.after(0, self.destroy)

    def _set_status(self, text):
        self.after(0, lambda: self.status_label.configure(text=text))

    def _set_progress(self, val):
        self.after(0, lambda: self.progress.configure(value=val))

    def _create_shortcuts(self):
        exe = os.path.join(self.install_dir, "silly-browser.exe")
        # Start Menu
        os.makedirs(START_MENU, exist_ok=True)
        sm_link = os.path.join(START_MENU, "the silly browser.lnk")
        self._make_lnk(sm_link, exe, self.install_dir)
        # Desktop
        if self.desktop_shortcut.get():
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            desk_link = os.path.join(desktop, "the silly browser.lnk")
            self._make_lnk(desk_link, exe, self.install_dir)

    def _make_lnk(self, path, target, workdir):
        # use powershell to create .lnk
        ps = (
            f'$ws = New-Object -ComObject WScript.Shell; '
            f'$sc = $ws.CreateShortcut("{path}"); '
            f'$sc.TargetPath = "{target}"; '
            f'$sc.WorkingDirectory = "{workdir}"; '
            f'$sc.IconLocation = "{target},0"; '
            f'$sc.Save()'
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True)

    def _register_uninstaller(self):
        # create uninstall script
        uninst = os.path.join(self.install_dir, "uninstall.ps1")
        with open(uninst, "w") as f:
            f.write(f'''$dir = "{self.install_dir}"
Remove-Item -Recurse -Force $dir -ErrorAction SilentlyContinue
Remove-Item -Force "{os.path.join(START_MENU, "the silly browser.lnk")}" -ErrorAction SilentlyContinue
Remove-Item -Force "$env:USERPROFILE\\Desktop\\the silly browser.lnk" -ErrorAction SilentlyContinue
Remove-Item -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\silly-browser" -Recurse -ErrorAction SilentlyContinue
Write-Host "uninstalled"
''')
        # registry entry
        try:
            import winreg
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                  r"Software\Microsoft\Windows\CurrentVersion\Uninstall\silly-browser")
            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "the silly browser")
            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ,
                              f'powershell -NoProfile -ExecutionPolicy Bypass -File "{uninst}"')
            winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, self.install_dir)
            winreg.CloseKey(key)
        except Exception:
            pass

    def _show_done(self):
        self.state = "done"
        self._clear_content()
        tk.Label(self.content_frame, text="Setup complete!",
                 bg=DIALOG_GRAY, fg=BLACK, font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 8))
        tk.Label(self.content_frame, text="the silly browser has been installed.\nYou can run it from the Start Menu.",
                 bg=DIALOG_GRAY, fg=BLACK, font=("Arial", 9), justify="left").pack(anchor="w", pady=(0, 12))

        # replace buttons
        for w in self.canvas.find_withtag("btnrow"):
            self.canvas.delete(w)
        btn_row = tk.Frame(self.canvas, bg=DIALOG_GRAY)
        self.canvas.create_window(self.dlg_x + self.dlg_w - 10, self.dlg_y + self.dlg_h - 12,
                                 window=btn_row, anchor="se", tags="btnrow")
        tk.Button(btn_row, text="Finish", font=("Arial", 9, "bold"), width=9,
                  command=self.destroy).pack(side="left", padx=(0, 6))
        tk.Button(btn_row, text="Launch", font=("Arial", 9), width=9,
                  command=self._launch).pack(side="left")

    def _launch(self):
        exe = os.path.join(self.install_dir, "silly-browser.exe")
        if os.path.exists(exe):
            subprocess.Popen([exe], cwd=self.install_dir)
        self.destroy()


if __name__ == "__main__":
    app = Installer()
    app.mainloop()
