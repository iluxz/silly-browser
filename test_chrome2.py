src = open(r"D:\OpenCode\silly-browser\silly_browser_v2.py", encoding="utf-8").read()
i = src.find("CHROME_JS = r")
j = src.find('"""', i + 20)
chrome_js = src[i+15:j]
lines = chrome_js.split("\n")

# test each line individually
import webview
window = webview.create_window('test', 'https://example.com', width=800, height=600)

def on_loaded():
    global window
    log = open(r"D:\OpenCode\silly-browser\test_debug.log", "a")
    # try evaluating the whole thing
    try:
        r = window.evaluate_js(chrome_js)
        log.write("FULL OK: %s\n" % r)
    except Exception as e:
        log.write("FULL ERROR: %s\n" % str(e))
    # try evaluating line by line
    for k, line in enumerate(lines[:10]):
        try:
            r = window.evaluate_js(line)
            log.write("line %d OK: %s\n" % (k+1, r))
        except Exception as e:
            log.write("line %d ERROR: %s | %s\n" % (k+1, str(e), line[:60]))
    log.close()

window.events.loaded += on_loaded
webview.start(debug=False)
