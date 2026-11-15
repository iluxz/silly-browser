(() => {
  if (window.brainLiquidationTres) return;

  const S = window.brainLiquidationTres = {
    timers: [],
    nodes: [],
    originalTitle: document.title,
    revenue: 4200000000,
    braincells: 0,
    running: true
  };

  const random = a => a[Math.floor(Math.random() * a.length)];

  const companies = [
    "NOBRO TECHNOLOGIES",
    "POTATO COMPUTING",
    "SILLY SYSTEMS",
    "NEURON DESTRUCTION LLC",
    "THE BREAD FOUNDATION",
    "ROOF GATOR INDUSTRIES",
    "WINDOWS 95 HOLDINGS",
    "LIZARD CAPITAL"
  ];

  const announcements = [
    "BRAIN LIQUIDATION ACQUIRES THE MOON",
    "NOBRO TECHNOLOGIES HAS DECLARED WAR ON CSS",
    "POTATO COMPUTING STOCK UP 9000%",
    "THE BREAD FOUNDATION REPORTS RECORD CRUMBS",
    "CEO HAS FORGOTTEN WHAT A COMPANY IS",
    "NEW SUBSIDIARY: SPOON INDUSTRIES",
    "INTEL REQUESTS A POTATO",
    "NVIDIA HAS BEEN OUTBID BY A SANDWICH",
    "THE BREAD INDEX IS UNSTABLE",
    "SHAREHOLDERS ARE CONFUSED",
    "THE HALF-BRAINCELL HAS APPROVED THE BUDGET"
  ];

  const emojis = [
    "💀","📈","💸","🍞","🥔","🦎","🧠",
    "🏢","📉","🗿","🚨","🧾","🪑","💼"
  ];

  const add = (tag, css, content) => {
    const e = document.createElement(tag);
    e.style.cssText = css;
    e.textContent = content;
    document.body.appendChild(e);
    S.nodes.push(e);
    return e;
  };

  const style = document.createElement("style");
  style.textContent = `
    @keyframes blSpin {
      to { transform:rotate(360deg); }
    }
    @keyframes blBounce {
      0%,100% { transform:translateY(0); }
      50% { transform:translateY(-35px); }
    }
    @keyframes blPulse {
      0%,100% { scale:1; }
      50% { scale:1.08; }
    }
    @keyframes blTicker {
      from { transform:translateX(100vw); }
      to { transform:translateX(-100%); }
    }
  `;
  document.head.appendChild(style);

  const later = (fn, ms) => {
    const id = setTimeout(fn, ms);
    S.timers.push({id, repeat:false});
  };

  const repeat = (fn, ms) => {
    const id = setInterval(fn, ms);
    S.timers.push({id, repeat:true});
  };

  const remove = e => {
    e.remove();
    S.nodes = S.nodes.filter(n => n !== e);
  };

  // CORPORATE STOCK TICKER
  const ticker = add("div", `
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:35px;
    overflow:hidden;
    background:#080808;
    color:#00ff41;
    border-bottom:2px solid #00ff41;
    z-index:2147483647;
    font:bold 14px Consolas;
    pointer-events:none;
  `, "");

  const tickerText = document.createElement("div");
  tickerText.textContent =
    " BRAIN LIQUIDATION INC.  |  BRAIN: 📈 999999%  | " +
    "BREAD INDEX: RISING  |  POTATO COMPUTING: ACQUIRED THE SUN  | ";
  tickerText.style.cssText =
    "white-space:nowrap;padding:9px;animation:blTicker 18s linear infinite";
  ticker.appendChild(tickerText);

  // THE FINANCIAL DASHBOARD
  const dashboard = add("div", `
    position:fixed;
    right:12px;
    bottom:12px;
    width:245px;
    background:#080808;
    color:#00ff41;
    border:2px solid #00ff41;
    padding:13px;
    font:12px Consolas;
    line-height:1.7;
    z-index:2147483647;
    pointer-events:none;
    box-shadow:0 0 20px #00ff4166;
    white-space:pre-line;
  `, "BRAIN LIQUIDATION INC.\nINITIALIZING...");

  // FLOATING CORPORATE ASSETS
  function asset() {
    const e = add("div", `
      position:fixed;
      left:${Math.random()*95}vw;
      top:${Math.random()*85}vh;
      font-size:${20+Math.random()*45}px;
      z-index:2147483646;
      pointer-events:none;
      animation:blBounce ${0.5+Math.random()*1.5}s infinite;
    `, random(emojis));

    later(() => remove(e), 6500);
  }

  // ACQUISITION NOTICES
  function acquisition() {
    const e = add("div", `
      position:fixed;
      left:${Math.random()*55}vw;
      top:${Math.random()*70}vh;
      background:#101010;
      color:#00ff41;
      border:2px solid #00ff41;
      padding:13px;
      max-width:300px;
      font:bold 13px Consolas;
      z-index:2147483647;
      pointer-events:none;
      box-shadow:0 0 15px #00ff4166;
      animation:blPulse .5s infinite;
    `, "🏢 CORPORATE ANNOUNCEMENT\n" + random(announcements));

    later(() => remove(e), 4000);
  }

  // THE CEO SPEAKS
  function ceo() {
    const e = add("div", `
      position:fixed;
      left:50%;
      top:45%;
      transform:translate(-50%,-50%);
      background:#111;
      color:#ffff00;
      border:3px double #ffff00;
      padding:20px;
      font:bold 19px Consolas;
      text-align:center;
      z-index:2147483647;
      pointer-events:none;
      max-width:80vw;
    `, "👔 CEO UPDATE:\n" + random([
      "i forgot the quarterly report",
      "buy more bread",
      "what is a stock",
      "we are now a potato company",
      "approved. no idea what it is.",
      "i have discovered a new number"
    ]));

    later(() => remove(e), 3000);
  }

  // CORPORATE DIAGNOSTICS
  repeat(() => {
    S.revenue += Math.floor(Math.random() * 99999999);
    S.braincells -= Math.floor(Math.random() * 3);

    dashboard.textContent =
      "BRAIN LIQUIDATION INC.\n" +
      "========================\n" +
      "NASDAQ: BRAIN\n" +
      "REVENUE: $" + S.revenue.toLocaleString() + "\n" +
      "BRAIN CELLS: " + S.braincells + "\n" +
      "CEO: HALF A BRAINCELL\n" +
      "STOCK: 📈 YES\n" +
      "BREAD INDEX: " + random(["RISING","MISSING","CRUNCHY","BANKRUPT"]) + "\n" +
      "SUBSIDIARIES: " + companies.length + "\n" +
      "CORPORATE STABILITY: NONE";
  }, 500);

  repeat(asset, 250);
  repeat(acquisition, 2200);
  repeat(ceo, 750);

  repeat(() => {
    document.title = random([
      "BRAIN LIQUIDATION INC.",
      "📈 BRAIN: BUY",
      "NOBRO TECHNOLOGIES",
      "THE BREAD INDEX",
      "CEO HAS LEFT",
      "CORPORATE GOOFYNESS"
    ]);
  }, 1500);

  // CLEANUP
  window.stopBrainLiquidationTres = () => {
    S.timers.forEach(t =>
      t.repeat ? clearInterval(t.id) : clearTimeout(t.id)
    );

    S.nodes.forEach(n => n.remove());
    style.remove();
    document.title = S.originalTitle;

    delete window.brainLiquidationTres;
    delete window.stopBrainLiquidationTres;

    console.log("BRAIN LIQUIDATION TRES: COMPANY DISSOLVED.");
  };

  console.log("BRAIN LIQUIDATION TRES: HOSTILE TAKEOVER COMPLETE.");
})();
