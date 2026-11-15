import webview

src = open(r"D:\OpenCode\silly-browser\silly_browser_v2.py", encoding="utf-8").read()
i = src.find("CHROME_JS = r")
j = src.find('"""', i + 20)
chrome_js = src[i+16:j]

window = webview.create_window('test', 'https://example.com', width=800, height=600)

def on_loaded():
    global window
    log = open(r"D:\OpenCode\silly-browser\test_debug.log", "a")
    try:
        r = window.evaluate_js(chrome_js)
        log.write("result: %s\n" % r)
    except Exception as e:
        log.write("error: %s\n" % str(e))
        # try to find the problematic line by testing chunks
        lines = chrome_js.split("\n")
        # test first 15 lines
        for end in range(2, 16):
            chunk = "\n".join(lines[:end])
            try:
                window.evaluate_js(chunk)
                log.write("lines 1-%d: OK\n" % end)
            except Exception as e2:
                log.write("lines 1-%d: ERROR %s\n" % (end, str(e2)))
                break
    log.close()

window.events.loaded += on_loaded
webview.start(debug=False)
