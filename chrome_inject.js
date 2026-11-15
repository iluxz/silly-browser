
(function() {
  if (window.__silly_chrome) return;
  window.__silly_chrome = true;

  // ----
  const bar = document.createElement('div');
  bar.id = '__silly_bar';
  bar.style.cssText = 'position:fixed;top:0;left:0;right:0;height:40px;background:linear-gradient(135deg,#fff8ee,#e8defd);border-bottom:3px solid #8b6cf0;display:flex;align-items:center;padding:0 8px;gap:6px;z-index:2147483647;font-family:Segoe UI,sans-serif;box-shadow:0 2px 10px rgba(139,108,240,0.3);';
  bar.innerHTML = `
    <button id="__silly_back" style="background:#8b6cf0;color:#fff;border:0;border-radius:6px;padding:4px 10px;cursor:pointer;font-weight:700;font-size:13px"><</button>
    <button id="__silly_fwd" style="background:#8b6cf0;color:#fff;border:0;border-radius:6px;padding:4px 10px;cursor:pointer;font-weight:700;font-size:13px">></button>
    <button id="__silly_reload" style="background:#8b6cf0;color:#fff;border:0;border-radius:6px;padding:4px 10px;cursor:pointer;font-weight:700;font-size:13px">R</button>
    <input id="__silly_url" type="text" style="flex:1;border:2px solid #e8defd;border-radius:16px;padding:4px 12px;font-size:13px;outline:none;background:#fff;" placeholder="enter url...">
    <button id="__silly_go" style="background:#5fd4b0;color:#0a3a2a;border:0;border-radius:6px;padding:4px 12px;cursor:pointer;font-weight:700;font-size:13px">go</button>
    <button id="__silly_dark" style="background:#2f2a45;color:#fff;border:0;border-radius:6px;padding:4px 10px;cursor:pointer;font-weight:700;font-size:13px">D</button>
    <button id="__silly_silly" style="background:#ff8fb1;color:#fff;border:0;border-radius:6px;padding:4px 12px;cursor:pointer;font-weight:700;font-size:13px">* inject</button>
    <button id="__silly_toggle" style="background:#ffc94d;color:#5c4400;border:0;border-radius:6px;padding:4px 10px;cursor:pointer;font-weight:700;font-size:13px">L</button>
  `;
  document.body.prepend(bar);
  document.body.style.paddingTop = '44px';

  // ----
  const sidebar = document.createElement('div');
  sidebar.id = '__silly_sidebar';
  sidebar.style.cssText = 'position:fixed;top:40px;right:0;width:300px;height:calc(100vh - 40px);background:#fff;border-left:3px solid #e8defd;z-index:2147483646;overflow-y:auto;font-family:Segoe UI,sans-serif;display:none;box-shadow:-2px 0 10px rgba(0,0,0,0.1);';
  sidebar.innerHTML = `
    <div style="padding:12px;border-bottom:2px solid #e8defd;display:flex;align-items:center;gap:8px">
      <span style="font-family:Comic Sans MS,cursive;font-size:16px;color:#2f2a45">the silly browser</span>
      <span style="margin-left:auto;font-size:11px;color:#9a93b8">v2.0</span>
    </div>
    <div style="padding:8px;text-align:center" id="__silly_mascot"></div>
    <div style="padding:8px;border-bottom:2px solid #e8defd">
      <div style="font-size:12px;font-weight:700;color:#2f2a45;margin-bottom:4px">scripts</div>
      <div id="__silly_scripts" style="max-height:200px;overflow-y:auto"></div>
    </div>
    <div style="padding:8px">
      <textarea id="__silly_editor" style="width:100%;height:100px;border:2px solid #e8defd;border-radius:8px;padding:8px;font:12px Consolas;resize:none;outline:none" placeholder="write your script..."></textarea>
      <div style="display:flex;gap:6px;margin-top:6px">
        <button id="__silly_save" style="flex:1;background:#8b6cf0;color:#fff;border:0;border-radius:8px;padding:6px;font:700 11px Segoe UI;cursor:pointer">save</button>
        <button id="__silly_inject" style="flex:1;background:#5fd4b0;color:#0a3a2a;border:0;border-radius:8px;padding:6px;font:700 11px Segoe UI;cursor:pointer">inject</button>
      </div>
    </div>
    <div style="padding:8px;border-top:2px solid #e8defd;font-size:11px;color:#9a93b8" id="__silly_status">ready *</div>
  `;
  document.body.appendChild(sidebar);

  // ----
  const mascotCanvas = document.createElement('canvas');
  mascotCanvas.width = 80;
  mascotCanvas.height = 70;
  mascotCanvas.style.cssText = 'display:block;margin:0 auto;';
  document.getElementById('__silly_mascot').appendChild(mascotCanvas);
  const mctx = mascotCanvas.getContext('2d');
  let mt = 0;
  function mascotLoop() {
    mt += 0.05;
    mctx.clearRect(0, 0, 80, 70);
    const bob = Math.sin(mt) * 3;
    const cx = 40, cy = 32 + bob;
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
    const blink = (mt % 4) > 3.4 ? 1.5 : 8;
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

  // ----
  document.getElementById('__silly_back').onclick = function() { window.pywebview.api.go_back(); };
  document.getElementById('__silly_fwd').onclick = function() { window.pywebview.api.go_forward(); };
  document.getElementById('__silly_reload').onclick = function() { location.reload(); };
  document.getElementById('__silly_go').onclick = function() {
    var url = document.getElementById('__silly_url').value;
    if (!url.startsWith('http')) url = 'https://' + url;
    window.location.href = url;
  };
  document.getElementById('__silly_url').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') document.getElementById('__silly_go').click();
  });
  document.getElementById('__silly_url').value = window.location.href;
  document.getElementById('__silly_toggle').onclick = function() {
    sidebar.style.display = sidebar.style.display === 'none' ? 'block' : 'none';
  };
  document.getElementById('__silly_dark').onclick = function() {
    var dark = document.body.classList.toggle('__silly_dark');
    if (dark) {
      var style = document.createElement('style');
      style.id = '__silly_dark_style';
      style.textContent = 'html { filter: invert(1) hue-rotate(180deg) !important; } img, video, canvas { filter: invert(1) hue-rotate(180deg) !important; }';
      document.head.appendChild(style);
      this.textContent = 'S';
      this.style.background = '#fff';
      this.style.color = '#2f2a45';
    } else {
      var s = document.getElementById('__silly_dark_style');
      if (s) s.remove();
      this.textContent = 'D';
      this.style.background = '#2f2a45';
      this.style.color = '#fff';
    }
  };
    // fetch scripts from pywebview API and inject
    if (window.pywebview && window.pywebview.api) {
      window.pywebview.api.get_scripts().then(function(scripts) {
        scripts.forEach(function(name) {
          window.pywebview.api.read_file(window.pywebview.api.get_scripts_folder() + '/' + name).then(function(code) {
            var s = document.createElement('script');
            s.textContent = code;
            document.body.appendChild(s);
          });
        });
        document.getElementById('__silly_status').textContent = 'injected ' + scripts.length + ' scripts *';
      });
    } else {
      document.getElementById('__silly_status').textContent = 'pywebview not available';
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
        document.getElementById('__silly_status').textContent = 'saved ' + name + ' *';
        loadScriptList();
      });
    }
  };
  document.getElementById('__silly_inject').onclick = function() {
    var code = document.getElementById('__silly_editor').value;
    var s = document.createElement('script');
    s.textContent = code;
    document.body.appendChild(s);
    document.getElementById('__silly_status').textContent = 'injected! *';
  };

  // ----
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

  // load scripts after pywebview is ready
  window.addEventListener('pywebviewready', function() {
    loadScriptList();
  });
  // fallback
  setTimeout(loadScriptList, 1000);

})();
