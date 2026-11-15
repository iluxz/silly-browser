(() => {
  window.stopBrainLiquidation4?.();

  const S = {
    running: true,
    revenue: 999999,
    bread: 0,
    braincells: 0.5,
    debt: 9000000000,
    timers: [],
    nodes: [],
    root: null
  };

  const random = (a, b) => Math.floor(Math.random() * (b - a + 1)) + a;
  const pick = arr => arr[random(0, arr.length - 1)];

  const announcements = [
    "BREAKING: BAGUETTE ACQUIRES WINDOWS 95",
    "THE BREAD FOUNDATION HAS DECLARED INDEPENDENCE",
    "NOBRO TECHNOLOGIES IS NOW 87% CROISSANT",
    "CEO UPDATE: THE CEO IS A LOAF OF BREAD",
    "URGENT: TOAST PRICES HAVE COLLAPSED",
    "ROOF GATOR INDUSTRIES HAS BOUGHT A BAKERY",
    "WINDOWS 95 HAS BEEN PROMOTED TO CFO",
    "THE STOCK MARKET IS NOW MADE OF CRUMBS",
    "SPOON INDUSTRIES HAS DECLARED WAR ON FORKS",
    "BREAD INFLATION HAS REACHED 9000%",
    "THE BOARD HAS BEEN REPLACED BY 14 BAGELS",
    "LIZARD CAPITAL HAS INVESTED IN YEAST",
    "ALL EMPLOYEES MUST NOW BE AT LEAST 40% BREAD",
    "THE COMPANY HAS ACQUIRED THE CONCEPT OF BUTTER",
    "THE CEO HAS ASCENDED INTO THE BREAD DIMENSION",
    "WARNING: UNAUTHORIZED CROISSANT DETECTED",
    "BRAIN LIQUIDATION INC. HAS RUN OUT OF BRAIN",
    "THE BREADENING IS NOW INEVITABLE"
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
    @keyframes bl4-float {
      0% { transform: translateY(110vh) rotate(0deg); }
      100% { transform: translateY(-150px) rotate(900deg); }
    }
    @keyframes bl4-shake {
      0%,100% { transform: translateX(0) rotate(0deg); }
      20% { transform: translateX(-5px) rotate(-1deg); }
      40% { transform: translateX(5px) rotate(1deg); }
      60% { transform: translateX(-4px) rotate(-1deg); }
      80% { transform: translateX(4px) rotate(1deg); }
    }
    @keyframes bl4-flash {
      0%,100% { filter: hue-rotate(0deg); }
      50% { filter: hue-rotate(180deg); }
    }
    @keyframes bl4-scroll {
      from { transform: translateX(100vw); }
      to { transform: translateX(-150%); }
    }
    .bl4-card {
      font-family: monospace;
      color: #fff4c9;
      background: rgba(35, 19, 5, .94);
      border: 2px solid #ffbd4a;
      box-shadow: 0 0 25px #ff9c0088;
      border-radius: 12px;
    }
  `;
  document.head.appendChild(style);

  S.root = document.createElement("div");
  S.root.id = "brain-liquidation-4";
  S.root.style.cssText =
    "position:fixed;inset:0;z-index:2147483647;pointer-events:none;overflow:hidden;";
  document.documentElement.appendChild(S.root);

  const banner = make("div",
    "position:absolute;top:12px;left:50%;transform:translateX(-50%);" +
    "width:min(90vw,650px);padding:14px;text-align:center;" +
    "font:bold 20px monospace;color:#fff;background:#7d2600;" +
    "border:3px dashed #ffd36b;border-radius:12px;" +
    "box-shadow:0 0 30px #ff9c00;animation:bl4-shake .3s infinite;"
  );
  banner.textContent = "🥖 BRAIN LIQUIDATION INC. — THE BREADENING 🥖";

  const panel = make("div",
    "position:absolute;top:100px;right:18px;width:260px;" +
    "padding:15px;box-sizing:border-box;animation:bl4-shake .7s infinite;",
  );
  panel.className = "bl4-card";

  const heading = make("div", "font-size:19px;font-weight:bold;margin-bottom:12px;", panel);
  heading.textContent = "🥖 BREAD HQ";

  const stats = make("div", "font-size:13px;line-height:2;", panel);

  const ticker = make("div",
    "position:absolute;bottom:15px;left:0;width:100%;height:36px;" +
    "background:#542000;color:#ffe4a3;border-top:2px solid orange;" +
    "border-bottom:2px solid orange;overflow:hidden;font:bold 17px monospace;"
  );

  const tickerText = make("div",
    "position:absolute;white-space:nowrap;top:8px;animation:bl4-scroll 13s linear infinite;",
    ticker
  );
  tickerText.textContent =
    " BRAIN LIQUIDATION INC. $$$  BREAD STOCK: TO THE MOON  $$$  BUY YEAST  $$$ ";

  const toast = make("div",
    "position:absolute;bottom:65px;left:50%;transform:translateX(-50%);" +
    "max-width:85vw;padding:12px 18px;text-align:center;" +
    "background:#311500;color:#ffe7a8;border:2px solid orange;" +
    "border-radius:10px;font:bold 14px monospace;opacity:0;"
  );

  function announce() {
    toast.textContent = pick(announcements);
    toast.style.opacity = "1";
    toast.style.animation = "bl4-shake .2s 3";

    const old = toast.textContent;
    const t = setTimeout(() => {
      if (S.running && toast.textContent === old) toast.style.opacity = "0";
    }, 2400);
    S.timers.push(t);
  }

  function spawnBread() {
    const breads = ["🥖", "🍞", "🥐", "🥯", "🧈", "🍞", "🥖"];
    const el = make("div",
      `position:absolute;left:${random(0, 95)}vw;bottom:-100px;` +
      `font-size:${random(25, 65)}px;` +
      `animation:bl4-float ${random(5, 11)}s linear forwards;`
    );
    el.textContent = pick(breads);

    setTimeout(() => {
      if (el.isConnected) el.remove();
    }, 11500);

    const breadNodes = S.root.querySelectorAll("div");
    if (breadNodes.length > 80) {
      const first = breadNodes[0];
      if (first !== banner && first !== panel && first !== ticker) first.remove();
    }
  }

  function update() {
    S.revenue += random(1000, 999999);
    S.bread += random(1, 900);
    S.braincells = Math.max(0, S.braincells - 0.01);
    S.debt += random(100000, 99999999);

    stats.innerHTML = `
      revenue: $${S.revenue.toLocaleString()}<br>
      bread produced: ${S.bread.toLocaleString()}<br>
      braincells remaining: ${S.braincells.toFixed(2)}<br>
      corporate debt: $${S.debt.toLocaleString()}<br>
      ceo: 🥖 baguette<br>
      cfo: 🪟 windows 95<br>
      company status: ${pick(["thriving", "legally questionable", "bread", "under investigation", "yeasting"])}
    `;
  }

  function timer(fn, ms) {
    S.timers.push(setInterval(() => {
      if (S.running) fn();
    }, ms));
  }

  update();
  announce();

  timer(update, 1000);
  timer(spawnBread, 350);
  timer(announce, 3200);

  window.stopBrainLiquidation4 = () => {
    S.running = false;
    S.timers.forEach(t => {
      clearInterval(t);
      clearTimeout(t);
    });
    S.root?.remove();
    style.remove();
    delete window.stopBrainLiquidation4;
    console.log("🥖 brain liquidation 4 has been liquidated.");
  };

  console.log("🥖 THE BREADENING HAS BEGUN.");
})();
