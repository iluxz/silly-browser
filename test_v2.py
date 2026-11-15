import webview

window = webview.create_window('test', 'https://example.com', width=800, height=600)

def on_loaded():
    global window
    log = open(r"D:\OpenCode\silly-browser\test_debug.log", "a")
    try:
        r = window.evaluate_js("document.body.style.background = 'red'; 'ok'")
        log.write("bg result: %s\n" % r)
    except Exception as e:
        log.write("bg error: %s\n" % str(e))
    try:
        code = "var d = document.createElement('div'); d.textContent = 'HELLO FROM SILLY'; d.style.cssText = 'position:fixed;top:10px;left:10px;z-index:999999;background:red;color:white;padding:10px;font-size:20px;'; document.body.appendChild(d); 'injected'"
        r = window.evaluate_js(code)
        log.write("inject result: %s\n" % r)
    except Exception as e:
        log.write("inject error: %s\n" % str(e))
    log.close()

window.events.loaded += on_loaded
webview.start(debug=False)
