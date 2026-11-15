import webview

# test with template literal
test_code = """(function() {
  if (window.__silly_chrome) return;
  window.__silly_chrome = true;
  var bar = document.createElement('div');
  bar.innerHTML = `<button>test</button>`;
  document.body.prepend(bar);
  return 'ok';
})();"""

window = webview.create_window('test', 'https://example.com', width=800, height=600)

def on_loaded():
    global window
    log = open(r"D:\OpenCode\silly-browser\test_debug.log", "a")
    try:
        r = window.evaluate_js(test_code)
        log.write("result: %s\n" % r)
    except Exception as e:
        log.write("error: %s\n" % str(e))
    log.close()

window.events.loaded += on_loaded
webview.start(debug=False)
