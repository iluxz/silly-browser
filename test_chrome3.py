import webview

src = open(r"D:\OpenCode\silly-browser\silly_browser_v2.py", encoding="utf-8").read()
i = src.find("CHROME_JS = r")
j = src.find('"""', i + 20)
chrome_js = src[i+16:j]

window = webview.create_window('test', 'https://example.com', width=800, height=600)

def on_loaded():
    global window
    log = open(r"D:\OpenCode\silly-browser\test_debug.log", "a")
    # try wrapping in a function
    wrapped = "(function() { " + chrome_js.strip().lstrip("(function() {").rstrip("})();") + " })();"
    # actually just try the raw string
    try:
        r = window.evaluate_js(chrome_js.strip())
        log.write("raw result: %s\n" % r)
    except Exception as e:
        log.write("raw error: %s\n" % str(e))
    log.close()

window.events.loaded += on_loaded
webview.start(debug=False)
