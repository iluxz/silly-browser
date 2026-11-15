# the silly browser

makes any website a little sillier. visual only, your screen only.

a little desktop app that runs a local server. you write a javascript snippet,
click a bookmark, and it gets injected into whatever page you're looking at.
works in any browser (edge, firefox, chrome, whatever) because it uses a
bookmarklet, not an extension.

## how to use

1. open the silly browser
2. pick a script (or write your own in the editor)
3. hit **copy bookmarklet**
4. paste it as a bookmark in any browser
5. go to any website, click the bookmark
6. your script runs on that page. only on your screen.

> **note:** the built-in scripts are visual effects, but the editor accepts arbitrary javascript.
> custom scripts have full access to the page's environment (DOM, cookies, etc.) — use responsibly.
> only run scripts you wrote or trust.

there's a **playground** button that opens a local test page so you can check
your scripts work before unleashing them on the internet.

## features

- local script server on `localhost:8742`
- script library with a built-in playground page
- 7 starter scripts (confetti, cursor trail, floating elements, meme text,
  rainbow mode, screen shake, default)
- write your own js in the built-in editor
- the little cube wears the colour of whichever script is loaded
- save/load your scripts in a plain `scripts/` folder next to the exe

## install

grab `silly-browser-setup.exe`, run it, done.

or just run `silly-browser.exe` on its own.

## build it yourself

```sh
pip install pyinstaller
pyinstaller --onefile --windowed --name "silly-browser" --icon silly.ico --add-data "scripts;scripts" --add-data "logo_small.png;." --add-data "silly.ico;." silly_browser.py
```

## license

MIT

<div align="center">
  <p>built with <code>:3</code> and a concerning amount of coffee..... and also a tiny bit of brain liquidation</p>
  <p>
    <a href="https://github.com/the-silly-team">github.com/the-silly-team</a>
  </p>
</div>
