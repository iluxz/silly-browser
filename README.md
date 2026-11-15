# 🧠 THE SILLY BROWSER 🧠

## MAKES ANY WEBSITE A LITTLE SILLIER. VISUAL ONLY. YOUR SCREEN ONLY. NOBODY ELSE SEES IT. THATS THE POINT.

a tiny desktop app that runs a local server on `localhost:8742`. you write a javascript snippet,
click a bookmark, and it gets injected into whatever page you're looking at.
works in any browser (edge, firefox, chrome, whatever) because it uses a
bookmarklet, not an extension. no chromium needed. no store submissions. no family safety drama.

## HOW TO USE (its not that hard)

1. open the silly browser
2. pick a script (or write your own in the editor)
3. hit **copy bookmarklet**
4. paste it as a bookmark in any browser
5. go to any website, click the bookmark
6. your script runs on that page. only on your screen. everyone else sees a normal website. you see chaos.

> **warning:** the built-in scripts are visual effects, but the editor accepts arbitrary javascript.
> custom scripts have full access to the page's environment (DOM, cookies, etc.) — use responsibly.
> only run scripts you wrote or trust.

there's a **playground** button that opens a local test page so you can check
your scripts work before unleashing them on the internet.

## FEATURES (there are a lot)

- local script server on `localhost:8742`
- script library with a built-in playground page
- 16+ starter scripts (confetti, cursor trail, floating elements, meme text,
  rainbow mode, screen shake, highlighter, ad-remover, text-replacer,
  element-picker, dark-mode, font-changer, rainbow-borders, tic-tac-toe,
  brain liquidation 1-6, silly+ premium scripts)
- write your own js/css in the built-in editor
- the little cube wears the colour of whichever script is loaded
- save/load your scripts in a plain `scripts/` folder next to the exe
- **silly+ supporter system** — star the repo + follow the org to unlock premium features
- key-based and github oauth verification
- auto-updating (checks github releases on startup)
- custom win3.1-style installer (no inno setup, pure python)
- dark mode (in settings)
- settings menu (mascot skins, auto-update, port, etc.)
- new script dialog
- delete button (protects presets)
- right-click to toggle scripts on/off
- horizontal scrolling bottom bar
- custom title bar (DWM styled)

## INSTALL

grab `silly-browser-setup.exe` from the releases page, run it, done.

or just run `silly-browser.exe` on its own. no install needed.

## BUILD IT YOURSELF (if you're into that)

```sh
pip install pyinstaller
pyinstaller --onefile --windowed --name "silly-browser" --icon silly.ico --add-data "scripts;scripts" --add-data "logo_small.png;." --add-data "silly.ico;." --add-data "styles;styles" silly_browser.py
```

## LICENSE

MIT

<div align="center">
  <p>built with <code>:3</code> and a concerning amount of coffee.....</p>
  <p>
    <a href="https://github.com/the-silly-team">github.com/the-silly-team</a>
  </p>
</div>
