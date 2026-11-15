import webview

data_uri = open(r"D:\OpenCode\temp\datauri.txt").read()

window = webview.create_window('test', 'https://example.com', width=800, height=600)

def on_loaded():
    global window
    log = open(r"D:\OpenCode\silly-browser\test_debug.log", "a")
    try:
        code = "var s = document.createElement('script'); s.src = '%s'; document.body.appendChild(s); 'ok'" % data_uri
        r = window.evaluate_js(code)
        log.write("script tag result: %s\n" % r)
    except Exception as e:
        log.write("script tag error: %s\n" % str(e))
    log.close()

window.events.loaded += on_loaded
webview.start(debug=False)
