"""
the silly browser v2.0 - the real browser
an actual browser with silly browser features built in.
uses pywebview (system webview, edge on windows).
"""
import os
import sys
import json
import base64
import webview

SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
SCRIPTS_FOLDER = os.path.join(SCRIPT_DIR, "scripts")
CSS_FOLDER = os.path.join(SCRIPT_DIR, "styles")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

os.makedirs(SCRIPTS_FOLDER, exist_ok=True)
os.makedirs(CSS_FOLDER, exist_ok=True)

# ── browser chrome (injected into every page via data URI) ────────────────────

CHROME_JS = r'''
(function() {
  if (window.__silly_chrome) return;
  window.__silly_chrome = true;

  // floating toolbar
  var bar = document.createElement('div');
  bar.id = '__silly_bar';
  bar.style.cssText = 'position:fixed;top:0;left:0;right:0;height:40px;background:linear-gradient(135deg,#fff8ee,#e8defd);border-bottom:3px solid #8b6cf0;display:flex;align-items:center;padding:0 8px;gap:6px;z-index:2147483647;font-family:Segoe UI,sans-serif;box-shadow:0 2px 10px rgba(139,108,240,0.3);';
  bar.innerHTML = '<button id="__silly_back" style="background:#8b6cf0;color:#fff;border:0;border-radius:6px;padding:4px 10px;cursor:pointer;font-weight:700;font-size:13px">&lt;</button><button id="__silly_fwd" style="background:#8b6cf0;color:#fff;border:0;border-radius:6px;padding:4px 10px;cursor:pointer;font-weight:700;font-size:13px">&gt;</button><button id="__silly_reload" style="background:#8b6cf0;color:#fff;border:0;border-radius:6px;padding:4px 10px;cursor:pointer;font-weight:700;font-size:13px">R</button><input id="__silly_url" type="text" style="flex:1;border:2px solid #e8defd;border-radius:16px;padding:4px 12px;font-size:13px;outline:none;background:#fff;color:#2f2a45;" placeholder="enter url..."><button id="__silly_go" style="background:#5fd4b0;color:#0a3a2a;border:0;border-radius:6px;padding:4px 12px;cursor:pointer;font-weight:700;font-size:13px">go</button><button id="__silly_dark" style="background:#2f2a45;color:#fff;border:0;border-radius:6px;padding:4px 10px;cursor:pointer;font-weight:700;font-size:13px">D</button><button id="__silly_silly" style="background:#ff8fb1;color:#fff;border:0;border-radius:6px;padding:4px 12px;cursor:pointer;font-weight:700;font-size:13px">inject</button><button id="__silly_toggle" style="background:#ffc94d;color:#5c4400;border:0;border-radius:6px;padding:4px 10px;cursor:pointer;font-weight:700;font-size:13px">L</button>';
  document.body.prepend(bar);
  document.body.style.paddingTop = '44px';

  // silly sidebar
  var sidebar = document.createElement('div');
  sidebar.id = '__silly_sidebar';
  sidebar.style.cssText = 'position:fixed;top:40px;right:0;width:300px;height:calc(100vh - 40px);background:#fff;border-left:3px solid #e8defd;z-index:2147483646;overflow-y:auto;font-family:Segoe UI,sans-serif;display:none;box-shadow:-2px 0 10px rgba(0,0,0,0.1);';
  sidebar.innerHTML = '<div style="padding:12px;border-bottom:2px solid #e8defd;display:flex;align-items:center;gap:8px"><span style="font-family:Comic Sans MS,cursive;font-size:16px;color:#2f2a45">the silly browser</span><span style="margin-left:auto;font-size:11px;color:#9a93b8">v2.0</span></div><div style="padding:8px;text-align:center" id="__silly_mascot"></div><div style="padding:8px;border-bottom:2px solid #e8defd"><div style="font-size:12px;font-weight:700;color:#2f2a45;margin-bottom:4px">scripts</div><div id="__silly_scripts" style="max-height:200px;overflow-y:auto"></div></div><div style="padding:8px"><textarea id="__silly_editor" style="width:100%;height:100px;border:2px solid #e8defd;border-radius:8px;padding:8px;font:12px Consolas;resize:none;outline:none" placeholder="write your script..."></textarea><div style="display:flex;gap:6px;margin-top:6px"><button id="__silly_save" style="flex:1;background:#8b6cf0;color:#fff;border:0;border-radius:8px;padding:6px;font:700 11px Segoe UI;cursor:pointer">save</button><button id="__silly_inject" style="flex:1;background:#5fd4b0;color:#0a3a2a;border:0;border-radius:8px;padding:6px;font:700 11px Segoe UI;cursor:pointer">inject</button></div></div><div style="padding:8px;border-top:2px solid #e8defd;font-size:11px;color:#9a93b8" id="__silly_status">ready</div>';
  document.body.appendChild(sidebar);

  // mascot
  var mc = document.createElement('canvas');
  mc.width = 80; mc.height = 70;
  mc.style.cssText = 'display:block;margin:0 auto;';
  document.getElementById('__silly_mascot').appendChild(mc);
  var mctx = mc.getContext('2d');
  var mt = 0;
  function mascotLoop() {
    mt += 0.05;
    mctx.clearRect(0, 0, 80, 70);
    var bob = Math.sin(mt) * 3;
    var cx = 40, cy = 32 + bob;
    mctx.fillStyle = '#e6ddf5';
    mctx.beginPath();
    mctx.ellipse(cx, 62 - Math.abs(bob)*0.3, 18, 4, 0, 0, Math.PI*2);
    mctx.fill();
    mctx.fillStyle = '#5cb8f0';
    mctx.strokeStyle = '#3484c4';
    mctx.lineWidth = 2;
    mctx.beginPath();
    mctx.roundRect(cx-16, cy-16, 32, 32, 6);
    mctx.fill();
    mctx.stroke();
    mctx.fillStyle = 'rgba(255,255,255,0.7)';
    mctx.beginPath();
    mctx.ellipse(cx-8, cy-10, 7, 4, 0, 0, Math.PI*2);
    mctx.fill();
    mctx.fillStyle = '#2f2a45';
    var blink = (mt % 4) > 3.4 ? 1.5 : 8;
    mctx.beginPath();
    mctx.ellipse(cx-6, cy-4, 3, blink/2, 0, 0, Math.PI*2);
    mctx.fill();
    mctx.beginPath();
    mctx.ellipse(cx+6, cy-4, 3, blink/2, 0, 0, Math.PI*2);
    mctx.fill();
    mctx.strokeStyle = '#2f2a45';
    mctx.lineWidth = 2;
    mctx.beginPath();
    mctx.arc(cx, cy+2, 6, 0.3, Math.PI-0.3);
    mctx.stroke();
    requestAnimationFrame(mascotLoop);
  }
  mascotLoop();

  // event handlers
  document.getElementById('__silly_back').onclick = function() { window.pywebview.api.go_back(); };
  document.getElementById('__silly_fwd').onclick = function() { window.pywebview.api.go_forward(); };
  document.getElementById('__silly_reload').onclick = function() { location.reload(); };
  document.getElementById('__silly_go').onclick = function() {
    var url = document.getElementById('__silly_url').value;
    if (!url.startsWith('http')) url = 'https://' + url;
    window.pywebview.api.navigate(url);
  };
  document.getElementById('__silly_url').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') document.getElementById('__silly_go').click();
  });
  document.getElementById('__silly_toggle').onclick = function() {
    sidebar.style.display = sidebar.style.display === 'none' ? 'block' : 'none';
  };
  document.getElementById('__silly_dark').onclick = function() {
    var s = document.getElementById('__silly_dark_style');
    if (s) { s.remove(); this.textContent = 'D'; }
    else {
      var st = document.createElement('style');
      st.id = '__silly_dark_style';
      st.textContent = 'html { filter: invert(1) hue-rotate(180deg) !important; } img, video, canvas { filter: invert(1) hue-rotate(180deg) !important; }';
      document.head.appendChild(st);
      this.textContent = 'S';
    }
  };
  document.getElementById('__silly_silly').onclick = function() {
    if (window.pywebview && window.pywebview.api) {
      window.pywebview.api.get_scripts().then(function(scripts) {
        scripts.forEach(function(name) {
          window.pywebview.api.read_file(window.pywebview.api.get_scripts_folder() + '/' + name).then(function(code) {
            var s = document.createElement('script');
            s.textContent = code;
            document.body.appendChild(s);
          });
        });
        document.getElementById('__silly_status').textContent = 'injected ' + scripts.length + ' scripts';
      });
    }
  };
  document.getElementById('__silly_save').onclick = function() {
    var code = document.getElementById('__silly_editor').value;
    var name = prompt('script name (without .js):');
    if (!name) return;
    name = name.trim().replace(/ /g, '-') + '.js';
    var folder = window.pywebview ? window.pywebview.api.get_scripts_folder() : '';
    if (folder) {
      window.pywebview.api.save_file(folder + '/' + name, code).then(function(r) {
        document.getElementById('__silly_status').textContent = 'saved ' + name;
        loadScriptList();
      });
    }
  };
  document.getElementById('__silly_inject').onclick = function() {
    var code = document.getElementById('__silly_editor').value;
    var s = document.createElement('script');
    s.textContent = code;
    document.body.appendChild(s);
    document.getElementById('__silly_status').textContent = 'injected!';
  };

  function loadScriptList() {
    if (window.pywebview && window.pywebview.api) {
      window.pywebview.api.get_scripts().then(function(scripts) {
        var list = document.getElementById('__silly_scripts');
        list.innerHTML = '';
        scripts.forEach(function(name) {
          var card = document.createElement('div');
          card.style.cssText = 'background:#fff8ee;border:2px solid #e8defd;border-radius:8px;padding:6px;margin-bottom:4px;cursor:pointer;';
          card.innerHTML = '<div style="font-weight:700;font-size:12px;color:#2f2a45">' + name.replace('.js','').replace(/-/g,' ') + '</div><div style="font-size:10px;color:#9a93b8">js script</div>';
          card.onclick = function() {
            window.pywebview.api.read_file(window.pywebview.api.get_scripts_folder() + '/' + name).then(function(code) {
              document.getElementById('__silly_editor').value = code;
            });
          };
          list.appendChild(card);
        });
      });
    }
  }

  window.addEventListener('pywebviewready', function() {
    loadScriptList();
    document.getElementById('__silly_url').value = window.location.href;
  });
  setTimeout(loadScriptList, 1000);
  document.getElementById('__silly_url').value = window.location.href;

  return 'chrome loaded';
})();
'''

# ── js api ───────────────────────────────────────────────────────────────────

class JsApi:
    def __init__(self, window):
        self.window = window

    def get_scripts(self):
        try:
            return sorted(f for f in os.listdir(SCRIPTS_FOLDER) if f.endswith(".js"))
        except Exception:
            return []

    def get_styles(self):
        try:
            return sorted(f for f in os.listdir(CSS_FOLDER) if f.endswith(".css"))
        except Exception:
            return []

    def read_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return "ERROR: " + str(e)

    def save_file(self, path, content):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return "ok"
        except Exception as e:
            return "ERROR: " + str(e)

    def get_scripts_folder(self):
        return SCRIPTS_FOLDER

    def get_css_folder(self):
        return CSS_FOLDER

    def navigate(self, url):
        if self.window:
            try:
                self.window.load_url(url)
            except Exception as e:
                return "ERROR: " + str(e)
        return "ok"

    def go_back(self):
        if self.window:
            try:
                self.window.go_back()
            except Exception as e:
                return "ERROR: " + str(e)
        return "ok"

    def go_forward(self):
        if self.window:
            try:
                self.window.go_forward()
            except Exception as e:
                return "ERROR: " + str(e)
        return "ok"

    def inject_script(self, code):
        if self.window:
            try:
                self.window.evaluate_js(code)
                return "ok"
            except Exception as e:
                return "ERROR: " + str(e)
        return "no window"

    def get_page_url(self):
        if self.window:
            try:
                return self.window.get_current_url()
            except Exception:
                return ""
        return ""


# ── main ─────────────────────────────────────────────────────────────────────

_window = None

def on_loaded():
    global _window
    try:
        url = _window.get_current_url()
        import base64
        b64 = base64.b64encode(CHROME_JS.encode("utf-8")).decode("ascii")
        data_uri = "data:text/javascript;base64," + b64
        _window.evaluate_js("var s = document.createElement('script'); s.src = '%s'; document.body.appendChild(s); 'ok'" % data_uri)
        import time
        # wait for script to execute then set URL
        import threading
        def set_url():
            import time
            time.sleep(1)
            try:
                url = _window.get_current_url()
                _window.evaluate_js("if(document.getElementById('__silly_url')) document.getElementById('__silly_url').value = '%s';" % url.replace("'", "\\'"))
            except Exception as e:
                print("set_url error:", e)
        threading.Thread(target=set_url, daemon=True).start()
    except Exception as e:
        print("inject failed:", e)


def main():
    global _window
    _window = webview.create_window(
        "the silly browser v2",
        "https://example.com",
        width=1280,
        height=800,
        min_size=(900, 600),
    )
    api = JsApi(_window)
    _window.expose(api.get_scripts)
    _window.expose(api.get_styles)
    _window.expose(api.read_file)
    _window.expose(api.save_file)
    _window.expose(api.get_scripts_folder)
    _window.expose(api.get_css_folder)
    _window.expose(api.navigate)
    _window.expose(api.go_back)
    _window.expose(api.go_forward)
    _window.expose(api.inject_script)
    _window.expose(api.get_page_url)

    _window.events.loaded += on_loaded

    webview.start(debug=False)


if __name__ == "__main__":
    main()
