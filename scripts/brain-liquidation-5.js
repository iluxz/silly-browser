(() => {
  window.stopBrainLiquidation5?.();

  const S = {
    running: true,
    chaos: 1,
    revenue: 900000,
    braincells: 0.5,
    bread: 0,
    debt: 9000000000,
    timers: [],
    nodes: [],
    root: null
  };

  const pick = a => a[Math.floor(Math.random() * a.length)];
  const rand = (a, b) => Math.floor(Math.random() * (b - a + 1)) + a;
  const money = n => "$" + Math.round(n).toLocaleString();

  const announcements = [
    "the baguette ceo has entered the building.",
    "windows 95 has successfully opened the calculator.",
    "nobro technologies has acquired 3 crumbs.",
    "the bread foundation demands more yeast.",
    "shareholders are now being paid in toast.",
    "lizard capital has invested in a suspicious sandwich.",
    "applesoft legal has requested another meeting.",
    "the company has liquidated its liquidator.",
    "urgent: the bakery is experiencing turbulence.",
    "the board has unanimously approved more bread.",
    "braincells are now a premium subscription.",
    "the company has discovered a new tax called bread tax.",
    "roof gator industries has purchased the parking lot.",
    "spoon industries reports record spoon production.",
    "the ceo has been replaced by a slightly larger baguette."
  ];

  const make = (tag, css, parent = S.root) => {
    const el = document.createElement(tag);
    el.style.cssText = css;
    parent.appendChild(el);
    S.nodes.push(el);
    return el;
  };

  const style = document.createElement("style");
  style.textContent = `
    @keyframes bl5-shake {
      0%,100% { transform: translate(0,0) rotate(0); }
      25% { transform: translate(-2px,1px) rotate(-.4deg); }
      75% { transform: translate(2px,-1px) rotate(.4deg); }
    }
    @keyframes bl5-float {
      from { transform: translateY(110vh) rotate(0deg); }
      to { transform: translateY(-130px) rotate(720deg); }
    }
    @keyframes bl5-scroll {
      from { transform: translateX(100%); }
      to { transform: translateX(-110%); }
    }
    #bl5-root * { box-sizing: border-box; }
    #bl5-root button {
      cursor: pointer;
      border: 1px solid #dca34c;
      border-radius: 7px;
      padding: 7px 10px;
      color: #ffe5b0;
      background: #42260f;
      font: bold 12px monospace;
    }
    #bl5-root button:hover { background: #70421b; }
    #bl5-root .bl5-muted { color: #c5a77d; }
    #bl5-root .bl5-card {
      background: #24180f;
      color: #ffe8bd;
      border: 2px solid #d99a42;
      border-radius: 10px;
      padding: 11px;
      margin-top: 9px;
    }
  `;

  S.root = document.createElement("div");
  S.root.id = "bl5-root";
  S.root.style.cssText =
    "position:fixed;inset:0;z-index:2147483647;pointer-events:none;" +
    "overflow:hidden;font-family:monospace;";
  document.documentElement.appendChild(S.root);
  document.head.appendChild(style);

  const panel = make("div",
    "position:fixed;top:15px;right:15px;width:min(340px,92vw);" +
    "max-height:85vh;overflow:auto;pointer-events:auto;" +
    "background:#24180f;color:#ffe8bd;border:2px solid #e9a84e;" +
    "border-radius:13px;padding:13px;box-shadow:0 0 30px #a85b1c88;" +
    "animation:bl5-shake 1.4s infinite;"
  );

  const header = make("div",
    "display:flex;justify-content:space-between;align-items:center;gap:8px;",
    panel
  );

  const title = make("div", "font-size:17px;font-weight:bold;", header);
  title.textContent = "🥖 brain liquidation 5";

  const close = make("button", "", header);
  close.textContent = "×";
  close.title = "close liquiditor";

  const subtitle = make("div",
    "font-size:10px;color:#c5a77d;margin-top:5px;", panel
  );
  subtitle.textContent = "the most useful financial disaster in history";

  const stats = make("div", "line-height:1.8;font-size:12px;", panel);
  stats.className = "bl5-card";

  const controls = make("div",
    "display:flex;flex-wrap:wrap;gap:6px;margin-top:10px;", panel
  );

  const inspectButton = make("button", "", controls);
  inspectButton.textContent = "inspect page";

  const announceButton = make("button", "", controls);
  announceButton.textContent = "corporate announcement";

  const chaosButton = make("button", "", controls);
  chaosButton.textContent = "chaos: level 1";

  const inspector = make("div", "font-size:12px;line-height:1.8;", panel);
  inspector.className = "bl5-card";

  const inspectorTitle = make("div", "font-weight:bold;margin-bottom:5px;", inspector);
  inspectorTitle.textContent = "🔎 webpage inspection";

  const inspectorOutput = make("div", "color:#e8d1ad;", inspector);
  inspectorOutput.textContent = "press inspect page to analyze this webpage.";

  const announcement = make("div",
    "position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);" +
    "max-width:85vw;padding:13px 18px;background:#3d210e;" +
    "border:2px dashed #f5bd64;border-radius:10px;color:#ffe8bd;" +
    "font:bold 13px monospace;text-align:center;opacity:0;" +
    "transition:opacity .2s;pointer-events:none;"
  );

  const ticker = make("div",
    "position:fixed;bottom:0;left:0;width:100%;height:31px;" +
    "background:#3d210e;border-top:2px solid #d99a42;" +
    "color:#ffe8bd;overflow:hidden;"
  );

  const tickerText = make("div",
    "white-space:nowrap;position:absolute;top:7px;" +
    "animation:bl5-scroll 18s linear infinite;",
    ticker
  );
  tickerText.textContent =
    " BRAIN LIQUIDATION INC. $$$ BREAD STOCK $$$ " +
    "APPLesoft LEGAL DEPARTMENT $$$ BUY CRUMBS $$$ ";

  function update() {
    S.revenue += rand(100, 900000);
    S.bread += rand(1, 50);
    S.braincells = Math.max(0, S.braincells - 0.001 * S.chaos);
    S.debt += rand(1000, 900000) * S.chaos;

    stats.innerHTML = `
      <div>💰 revenue: ${money(S.revenue)}</div>
      <div>🥖 bread produced: ${S.bread.toLocaleString()}</div>
      <div>🧠 braincells: ${S.braincells.toFixed(3)}</div>
      <div>📉 corporate debt: ${money(S.debt)}</div>
      <div>📊 chaos multiplier: x${S.chaos}</div>
      <div>👔 ceo: baguette</div>
      <div>🪟 cfo: windows 95</div>
      <div>📡 status: ${pick([
        "thriving",
        "under investigation",
        "legally questionable",
        "yeasting",
        "absolutely cooked"
      ])}</div>
    `;
  }

  function notify(message = pick(announcements)) {
    announcement.textContent = message;
    announcement.style.opacity = "1";

    const timer = setTimeout(() => {
      if (S.running) announcement.style.opacity = "0";
    }, 2400);

    S.timers.push(timer);
  }

  function inspect() {
    const text = document.body?.innerText || "";
    const headings = document.querySelectorAll("h1,h2,h3").length;
    const links = document.links.length;
    const images = document.images.length;
    const forms = document.forms.length;
    const scripts = document.scripts.length;
    const bytes = new Blob([text]).size;
    const words = text.trim().split(/\s+/).filter(Boolean).length;

    inspectorOutput.textContent = "";

    const rows = [
      ["page title", document.title || "(untitled)"],
      ["domain", location.hostname],
      ["headings", headings],
      ["links", links],
      ["images", images],
      ["forms", forms],
      ["scripts", scripts],
      ["visible text", words.toLocaleString() + " words"],
      ["text size", (bytes / 1024).toFixed(1) + " kb"],
      ["viewport", innerWidth + " × " + innerHeight]
    ];

    for (const [label, value] of rows) {
      const row = document.createElement("div");
      row.textContent = label + ": " + value;
      inspectorOutput.appendChild(row);
    }

    notify("page inspection completed. the shareholders are impressed.");
  }

  function spawnBread() {
    const el = make("div",
      `position:absolute;left:${rand(0,95)}vw;top:105vh;` +
      `font-size:${rand(24,55)}px;` +
      `animation:bl5-float ${rand(5,12)}s linear forwards;`
    );
    el.textContent = pick(["🥖", "🍞", "🥐", "🥯", "🧈"]);

    const timer = setTimeout(() => el.remove(), 13000);
    S.timers.push(timer);
  }

  inspectButton.onclick = inspect;
  announceButton.onclick = () => notify();

  chaosButton.onclick = () => {
    S.chaos = S.chaos >= 5 ? 1 : S.chaos + 1;
    chaosButton.textContent = "chaos: level " + S.chaos;
    notify("chaos level increased to " + S.chaos + ". the board is concerned.");
  };

  close.onclick = () => window.stopBrainLiquidation5();

  const interval = (fn, ms) => {
    S.timers.push(setInterval(() => {
      if (S.running) fn();
    }, ms));
  };

  update();
  interval(update, 1000);
  interval(spawnBread, 700);
  interval(() => notify(), 7500);

  window.stopBrainLiquidation5 = () => {
    if (!S.running) return;
    S.running = false;

    S.timers.forEach(t => {
      clearInterval(t);
      clearTimeout(t);
    });

    S.root.remove();
    style.remove();
    delete window.stopBrainLiquidation5;

    console.log("brain liquidation 5 has been liquidated.");
  };

  console.log("🥖 brain liquidation 5 initialized.");
})();
