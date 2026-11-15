import webview
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROME_JS = open(os.path.join(SCRIPT_DIR, "chrome_js.txt"), "w")  # placeholder

# read the CHROME_JS from silly_browser_v2.py
src = open(os.path.join(SCRIPT_DIR, "silly_browser_v2.py"), encoding="utf-8").read()
i = src.find('CHROME_JS = r"""')
j = src.find('"""', i + 20)
chrome_js = src[i+15:j]

window = webview.create_window('test', 'https://example.com', width=800, height=600)

def on_loaded():
    global window
    log = open(os.path.join(SCRIPT_DIR, "test_debug.log"), "a")
    try:
        r = window.evaluate_js(chrome_js)
        log.write("chrome result: %s\n" % r)
    except Exception as e:
        log.write("chrome error: %s\n" % str(e))
    log.close()

window.events.loaded += on_loaded
webview.start(debug=False)
