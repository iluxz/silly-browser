(() => {
  "use strict";

  // BRAIN LIQUIDATION INC. PRESENTS:
  // BRAIN LIQUIDATION 6: THE BREADENING
  // maximum chaos. minimum shareholder satisfaction.

  // remove an older instance first
  if (window.stopBrainLiquidation6) {
    window.stopBrainLiquidation6();
  }

  const BL6 = {
    running: true,
    timers: [],
    nodes: new Set(),
    audio: null
  };

  const rand = (min, max) =>
    Math.floor(Math.random() * (max - min + 1)) + min;

  const pick = arr => arr[rand(0, arr.length - 1)];

  const colors = [
    "#ff003c", "#ff8c00", "#ffee00", "#00ff88",
    "#00cfff", "#a000ff", "#ff00cc", "#ffffff",
    "#7cff00", "#ff5500", "#000000"
  ];

  const garbage = [
    "🥖", "🍞", "🥐", "🧠", "🪑", "🐊", "🧀", "🍅",
    "🗿", "🪿", "🪣", "📉", "💼", "🥔", "💀", "🦎",
    "🚨", "💰", "📺", "❗", "🛒", "🧦", "🪨",
    "BRAIN LIQUIDATION", "APPLESOFT", "NOBRO",
    "BUY BREAD", "SELL BREAD", "CEO MISSING",
    "STOCK CRASH", "BREAD STOCK +900%",
    "OBJECTION!", "LEGAL DEPARTMENT",
    "POTATO CAPITAL", "WINDOWS 95",
    "THE BREADENING", "CRUMB ECONOMY",
    "YOUR BRAIN IS NOW A SUBSCRIPTION",
    "MARKET CLOSED (IT IS NOT)",
    "URGENT CORPORATE NONSENSE",
    "BAGUETTE ACQUISITION",
    "SHAREHOLDERS ARE CONFUSED",
    "PLEASE PANIC", "NOBRO MOMENT",
    "THE TOASTER HAS VOTING RIGHTS",
    "DIVIDENDS PAID IN CRUMBS",
    "ERROR: CEO NOT FOUND",
    "THE BREAD IS WATCHING"
  ];

  const headlines = [
    "BREAKING: BREAD STOCK RISES 9000%",
    "APPLESOFT FILES ANOTHER OBJECTION",
    "NOBRO TECHNOLOGIES DECLARES BANKRUPTCY",
    "POTATO COMPUTING ACQUIRES THE MOON",
    "CEO HAS BEEN REPLACED BY A BAGUETTE",
    "BRAIN LIQUIDATION DENIES EVERYTHING",
    "THE CRUMB ECONOMY IS IN SHAMBLES",
    "SHAREHOLDERS DEMAND MORE POTATOES",
    "MARKET ANALYSTS HAVE GIVEN UP",
    "BRAIN LIQUIDATION BUYS ITS OWN STOCK",
    "THE STOCK MARKET IS NOW A TOASTER",
    "APPLESOFT OBJECTS TO THE COLOR PURPLE",
    "NOBRO STOCKS ENTER THE FOURTH DIMENSION",
    "URGENT: THE CEO HAS LEFT THE BUILDING",
    "BREAD FOUNDATION REPORTS RECORD PROFITS",
    "NEURON DESTRUCTION LLC LOSES ITS BRAINCELL",
    "SILLY SYSTEMS ACCIDENTALLY BUYS A PLANET",
    "LEGAL DEPARTMENT HAS EATEN THE CONTRACT"
  ];

  const announcements = [
    "PLEASE REMAIN CALM",
    "THIS IS A FINANCIAL EMERGENCY",
    "BREAD IS THE FUTURE",
    "THE CEO IS A HALF-BRAIN CELL",
    "WE HAVE NO COMMENT",
    "BUY BUY BUY BUY BUY",
    "SELL EVERYTHING EXCEPT THE BREAD",
    "THE MARKET IS EXPERIENCING A MOMENT",
    "YOUR INVESTMENT HAS BECOME A SANDWICH",
    "CORPORATE CONFUSION DETECTED",
    "THIS MEETING COULD HAVE BEEN AN EMAIL",
    "THE SHAREHOLDERS ARE IN THE PARKING LOT",
    "WE HAVE LIQUIDATED THE LIQUIDATOR",
    "THE BREADENING IS UPON US"
  ];

  const objections = [
    {
      name: "APPLESOFT",
      lines: [
        "OBJECTION! THE BREAD IS TOO LIQUID!",
        "APPLESOFT OBJECTS TO THIS ENTIRE WEBSITE!",
        "THIS IS NOT HOW BRAINS WORK!",
        "WE OWN THE CONCEPT OF ROUNDED CORNERS!"
      ]
    },
    {
      name: "BRAIN LIQUIDATION INC.",
      lines: [
        "OBJECTION! WE OBJECT TO OUR OWN OBJECTION!",
        "THE CEO HAS NO COMMENT!",
        "LEGAL DEPARTMENT HAS BEEN LIQUIDATED!",
        "WE ARE NOT RESPONSIBLE FOR THE POTATO!"
      ]
    },
    {
      name: "NOBRO TECHNOLOGIES",
      lines: [
        "OBJECTION! NOBRO HAS NO BRO!",
        "OUR STOCK IS NOW A VEGETABLE!",
        "WE HAVE LOST THE FINANCIAL DOCUMENT!",
        "PLEASE STOP ASKING ABOUT THE BREAD!"
      ]
    }
  ];

  const stocks = [
    { name: "BREAD", price: 420 },
    { name: "NOBRO", price: 69 },
    { name: "POTATO", price: 120 },
    { name: "CRUMB", price: 12 },
    { name: "APPLESOFT", price: 900 },
    { name: "BRAIN", price: 100 },
    { name: "TOASTER", price: 55 },
    { name: "CEO", price: 0 }
  ];

  // create the overlay
  const root = document.createElement("div");
  root.id = "brain-liquidation-6-root";

  Object.assign(root.style, {
    position: "fixed",
    inset: "0",
    zIndex: "2147483647",
    pointerEvents: "none",
    overflow: "hidden",
    fontFamily: "Arial, sans-serif",
    color: "white"
  });

  document.documentElement.appendChild(root);

  const style = document.createElement("style");
  style.textContent = `
    @keyframes bl6-wobble {
      0% { transform: rotate(-8deg) scale(1); }
      50% { transform: rotate(8deg) scale(1.2); }
      100% { transform: rotate(-8deg) scale(1); }
    }

    @keyframes bl6-pop {
      0% { transform: scale(0) rotate(-20deg); }
      70% { transform: scale(1.2) rotate(8deg); }
      100% { transform: scale(1) rotate(0); }
    }

    @keyframes bl6-marquee {
      from { transform: translateX(100vw); }
      to { transform: translateX(-150%); }
    }

    @keyframes bl6-flash {
      0%, 100% { opacity: 1; }
      50% { opacity: .35; }
    }

    @keyframes bl6-spin {
      to { transform: rotate(360deg); }
    }

    #brain-liquidation-6-root * {
      box-sizing: border-box;
    }

    .bl6-ticker {
      position: absolute;
      left: 0;
      width: 100%;
      overflow: hidden;
      white-space: nowrap;
      font-weight: 1000;
      text-shadow: 2px 2px black;
      padding: 7px;
      animation: bl6-flash .4s infinite;
    }

    .bl6-ticker span {
      display: inline-block;
      animation: bl6-marquee 7s linear infinite;
    }

    .bl6-panel {
      position: absolute;
      top: 65px;
      right: 12px;
      width: 230px;
      padding: 12px;
      background: #10001f;
      border: 4px solid #ff00cc;
      box-shadow: 0 0 20px #ff00cc;
      font-size: 13px;
      font-weight: 1000;
      line-height: 1.6;
    }

    .bl6-button {
      pointer-events: auto;
      cursor: pointer;
      border: 3px solid white;
      background: #ff00cc;
      color: white;
      font-weight: 1000;
      padding: 7px;
      margin-top: 6px;
      width: 100%;
    }

    .bl6-breaking {
      position: absolute;
      top: 45%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 95vw;
      text-align: center;
      font-size: clamp(25px, 5vw, 75px);
      font-weight: 1000;
      text-shadow: 5px 5px black;
      -webkit-text-stroke: 1px black;
      animation: bl6-pop .25s;
    }
  `;

  root.appendChild(style);

  function track(el) {
    BL6.nodes.add(el);
    return el;
  }

  function remove(el) {
    if (!el) return;
    el.remove();
    BL6.nodes.delete(el);
  }

  function make(text, css) {
    const el = document.createElement("div");
    el.textContent = text;
    el.style.cssText = css;
    root.appendChild(el);
    return track(el);
  }

  function every(fn, delay) {
    const timer = setInterval(() => {
      if (BL6.running) fn();
    }, delay);

    BL6.timers.push(timer);
  }

  function later(fn, delay) {
    const timer = setTimeout(() => {
      if (BL6.running) fn();
    }, delay);

    BL6.timers.push(timer);
  }

  function ticker(text, color, top, speed) {
    const bar = document.createElement("div");
    bar.className = "bl6-ticker";
    bar.style.top = `${top}px`;
    bar.style.background = color;

    const span = document.createElement("span");
    span.textContent = text;
    span.style.animationDuration = `${speed / 10}s`;

    bar.appendChild(span);
    root.appendChild(bar);
    track(bar);
  }

  // stock exchange
  const market = document.createElement("div");
  market.className = "bl6-panel";
  market.innerHTML = "";
  market.textContent = "BRAIN LIQUIDATION STOCK EXCHANGE";
  root.appendChild(market);
  track(market);

  const marketData = document.createElement("div");
  marketData.style.cssText = "margin-top:8px;white-space:pre-line;";
  market.appendChild(marketData);

  const marketStatus = document.createElement("div");
  marketStatus.style.cssText =
    "color:#00ff88;margin-top:8px;font-size:11px;";
  market.appendChild(marketStatus);

  function updateStocks() {
    let output = "";

    for (const stock of stocks) {
      const old = stock.price;
      stock.price += rand(-80, 80);
      stock.price = Math.max(0, stock.price);

      const arrow = stock.price >= old ? "📈" : "📉";
      const color = stock.price >= old ? "#00ff88" : "#ff3344";

      output += `${arrow} ${stock.name}: $${stock.price}\n`;
    }

    marketData.textContent = output;
    marketData.style.color = pick(colors);

    marketStatus.textContent = pick([
      "MARKET STATUS: EXTREMELY NORMAL",
      "MARKET STATUS: BREAD",
      "MARKET STATUS: PANIC",
      "MARKET STATUS: CEO NOT FOUND",
      "MARKET STATUS: TOASTER CRASH",
      "MARKET STATUS: ???"
    ]);
  }

  // random floating nonsense
  function spawnGarbage() {
    if (BL6.nodes.size > 130) return;

    const el = make(
      pick(garbage),
      `
        position:absolute;
        left:${rand(0, 95)}vw;
        top:${rand(0, 95)}vh;
        font-size:${rand(13, 55)}px;
        font-weight:1000;
        color:${pick(colors)};
        -webkit-text-stroke:1px black;
        text-shadow:3px 3px 0 black;
        white-space:nowrap;
        animation:bl6-wobble ${rand(1, 3)}s infinite;
      `
    );

    later(() => remove(el), rand(1500, 4000));
  }

  // giant text attacks
  function giantText() {
    if (BL6.nodes.size > 130) return;

    const el = make(
      pick([
        ...headlines,
        ...announcements,
        ...garbage,
        "BREAKING: THE CEO HAS BEEN REPLACED BY BREAD",
        "THE MARKET IS NOW A TOASTER",
        "APPLESOFT HAS OBJECTED TO THE COLOR PURPLE",
        "NOBRO STOCKS HAVE ENTERED THE FOURTH DIMENSION",
        "BRAIN LIQUIDATION HAS LIQUIDATED ITS OWN LIQUIDATOR"
      ]),
      `
        position:absolute;
        left:${rand(0, 60)}vw;
        top:${rand(0, 85)}vh;
        max-width:95vw;
        font-size:${rand(25, 75)}px;
        font-weight:1000;
        color:${pick(colors)};
        -webkit-text-stroke:2px black;
        text-shadow:5px 5px black;
        overflow-wrap:anywhere;
        animation:bl6-pop .3s;
      `
    );

    later(() => remove(el), rand(1000, 2500));
  }

  // popup spam
  function popup() {
    if (BL6.nodes.size > 130) return;

    const el = make(
      pick([
        ...announcements,
        ...headlines,
        ...objections.flatMap(o => o.lines)
      ]),
      `
        position:absolute;
        left:${rand(0, 75)}vw;
        top:${rand(0, 80)}vh;
        max-width:280px;
        background:${pick(colors)};
        color:${pick(["white", "black"])};
        border:4px solid ${pick(colors)};
        padding:12px;
        font-size:${rand(15, 25)}px;
        font-weight:1000;
        text-shadow:2px 2px black;
        box-shadow:0 0 20px ${pick(colors)};
        animation:bl6-pop .15s;
      `
    );

    later(() => remove(el), rand(1000, 2500));
  }

  // breaking news
  function headline() {
    const el = make(
      `🚨 BREAKING NEWS: ${pick(headlines)} 🚨`,
      `
        position:absolute;
        left:${rand(0, 10)}vw;
        top:${rand(15, 85)}vh;
        max-width:90vw;
        padding:10px;
        background:${pick(colors)};
        color:white;
        border:3px solid white;
        font-size:${rand(17, 30)}px;
        font-weight:1000;
        text-shadow:3px 3px black;
        animation:bl6-pop .2s;
      `
    );

    later(() => remove(el), 3500);
  }

  // objections
  function objection() {
    const company = pick(objections);
    const el = make(
      `${company.name} LEGAL DEPARTMENT: ${pick(company.lines)}`,
      `
        position:absolute;
        left:${rand(5, 30)}vw;
        top:${rand(10, 80)}vh;
        max-width:75vw;
        background:#ff003c;
        color:white;
        border:5px double white;
        padding:18px;
        font-size:${rand(20, 35)}px;
        font-weight:1000;
        text-shadow:3px 3px black;
        box-shadow:0 0 30px red;
        animation:bl6-pop .2s;
      `
    );

    later(() => remove(el), 3000);
  }

  // random screen color flashes
  function colorFlash() {
    root.style.background =
      `linear-gradient(${rand(0, 360)}deg,
      ${pick(colors)}22,
      ${pick(colors)}33,
      transparent)`;
  }

  // random graph nonsense
  function updateGraph() {
    const graph = make(
      pick(["📈", "📉", "〽️", "💹"]) +
      " ".repeat(rand(1, 3)) +
      pick(["BREAD", "NOBRO", "POTATO", "BRAIN"]) +
      " STOCK " +
      pick(["▲", "▼", "🚀", "💥"]) +
      rand(0, 99999),
      `
        position:absolute;
        left:${rand(0, 65)}vw;
        top:${rand(0, 90)}vh;
        font-size:${rand(20, 45)}px;
        font-weight:1000;
        color:${pick(colors)};
        text-shadow:3px 3px black;
        transform:rotate(${rand(-20, 20)}deg);
      `
    );

    later(() => remove(graph), 1800);
  }

  // optional sound, only after user interaction
  function noise() {
    if (!BL6.audio) return;

    try {
      const ctx = BL6.audio;
      const oscillator = ctx.createOscillator();
      const gain = ctx.createGain();

      oscillator.type = pick(["square", "sawtooth", "triangle"]);
      oscillator.frequency.value = rand(100, 1200);
      gain.gain.value = 0.025;

      oscillator.connect(gain);
      gain.connect(ctx.destination);

      oscillator.start();
      oscillator.stop(ctx.currentTime + 0.08);
    } catch (_) {}
  }

  // controls
  const controls = document.createElement("div");
  controls.className = "bl6-panel";
  controls.style.top = "65px";
  controls.style.left = "12px";
  controls.style.right = "auto";
  controls.style.width = "170px";
  controls.textContent = "CORPORATE CONTROL PANEL";
  root.appendChild(controls);
  track(controls);

  const soundButton = document.createElement("button");
  soundButton.className = "bl6-button";
  soundButton.textContent = "ENABLE CORPORATE NOISE";
  controls.appendChild(soundButton);

  soundButton.addEventListener("click", () => {
    try {
      const Audio = window.AudioContext || window.webkitAudioContext;
      if (!Audio) return;

      if (!BL6.audio) BL6.audio = new Audio();
      BL6.audio.resume();
      soundButton.textContent = "NOISE ENABLED";
    } catch (_) {
      soundButton.textContent = "AUDIO FAILED";
    }
  });

  const stopButton = document.createElement("button");
  stopButton.className = "bl6-button";
  stopButton.style.background = "#cc0000";
  stopButton.textContent = "LIQUIDATE THIS SCRIPT";
  controls.appendChild(stopButton);

  stopButton.addEventListener("click", () => {
    window.stopBrainLiquidation6();
  });

  // ticker overload
  ticker(
    "🚨 BREAKING NEWS 🚨 BREAD STOCK COLLAPSES 🚨 CEO MISSING 🚨",
    "#e00032", 0, 65
  );

  ticker(
    "APPLESOFT OBJECTS • NOBRO OBJECTS TO APPLESOFT • BRAIN LIQUIDATION OBJECTS TO BOTH",
    "#7200bb", 38, 95
  );

  ticker(
    "BUY CRUMBS • SELL POTATO • BUY BREAD • SELL NOTHING • MARKET CONFUSION",
    "#008b63", 110, 125
  );

  // initial market state
  updateStocks();

  // THE GREAT CORPORATE TIMER COLLAPSE
  every(spawnGarbage, 40);
  every(giantText, 450);
  every(popup, 500);
  every(headline, 700);
  every(updateStocks, 120);
  every(updateGraph, 250);
  every(colorFlash, 300);
  every(noise, 900);

  // objections arrive at unpredictable intervals
  function scheduleObjection() {
    if (!BL6.running) return;

    objection();

    later(
      scheduleObjection,
      rand(1000, 6000)
    );
  }

  later(scheduleObjection, 1500);

  // giant corporate announcements
  function scheduleAnnouncement() {
    if (!BL6.running) return;

    const el = make(
      pick(announcements),
      `
        position:absolute;
        inset:30% 5% auto;
        text-align:center;
        font-size:${rand(30, 65)}px;
        font-weight:1000;
        color:${pick(colors)};
        -webkit-text-stroke:2px black;
        text-shadow:5px 5px black;
        animation:bl6-pop .3s;
      `
    );

    later(() => remove(el), 1800);
    later(scheduleAnnouncement, 2500);
  }

  later(scheduleAnnouncement, 1000);

  // stop / cleanup function
  window.stopBrainLiquidation6 = () => {
    if (!BL6.running) return;

    BL6.running = false;

    for (const timer of BL6.timers) {
      clearInterval(timer);
      clearTimeout(timer);
    }

    BL6.timers.length = 0;

    if (BL6.audio) {
      try {
        BL6.audio.close();
      } catch (_) {}
    }

    root.remove();
    BL6.nodes.clear();

    delete window.stopBrainLiquidation6;

    console.log(
      "[brain liquidation 6] corporate operations terminated."
    );
  };

  console.log(
    "[brain liquidation 6] injected. shareholders are confused."
  );
})();
