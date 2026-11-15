import webview

src = open(r"D:\OpenCode\silly-browser\silly_browser_v2.py", encoding="utf-8").read()
i = src.find("CHROME_JS = r")
j = src.find('"""', i + 20)
chrome_js = src[i+16:j].strip()

window = webview.create_window('test', 'https://example.com', width=800, height=600)

def on_loaded():
    global window
    log = open(r"D:\OpenCode\silly-browser\test_debug.log", "a")
    lines = chrome_js.split("\n")
    # binary search for the problematic line
    # test increasing chunks
    for end in range(1, min(30, len(lines)+1)):
        chunk = "\n".join(lines[:end])
        try:
            r = window.evaluate_js(chunk)
            log.write("lines 1-%d: OK\n" % end)
        except Exception as e:
            log.write("lines 1-%d: ERROR %s\n" % (end, str(e)))
            # print the last line
            log.write("  last line: %s\n" % lines[end-1][:80])
            break
    log.close()

window.events.loaded += on_loaded
webview.start(debug=False)
