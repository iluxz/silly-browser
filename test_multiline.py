import webview

# Test with a multi-line script that has semicolons
test_code = """(function() {
  var x = 1;
  var y = 2;
  var z = x + y;
  console.log('result:', z);
  return z;
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
