import webview

# read the chrome js
chrome_js = open(r"D:\OpenCode\silly-browser\chrome_inject.js", encoding="utf-8").read()

window = webview.create_window('test', 'https://example.com', width=800, height=600)

def on_loaded():
    global window
    log = open(r"D:\OpenCode\silly-browser\test_debug.log", "a")
    
    # Try evaluating just the first 4 lines joined
    lines = chrome_js.split("\n")
    for i in [4, 5, 8, 10, 15]:
        chunk = "\n".join(lines[:i])
        try:
            r = window.evaluate_js(chunk)
            log.write("chunk %d: OK %s\n" % (i, r))
        except Exception as e:
            log.write("chunk %d: ERROR %s\n" % (i, str(e)))
            break
    
    log.close()

window.events.loaded += on_loaded
webview.start(debug=False)
