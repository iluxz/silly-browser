(() => {
  if (window.sillyApocalypse) return;

  const state = window.sillyApocalypse = {
    running: true,
    timers: [],
    elements: [],
    originalTitle: document.title
  };

  const $ = (tag, css, text = "") => {
    const el = document.createElement(tag);
    el.style.cssText = css;
    el.textContent = text;
    document.body.appendChild(el);
    state.elements.push(el);
    return el;
  };

  const emojis = [
    "💀","🗿","🍞","🦎","🚨","🧠","🧌",
    "🐸","🧀","🛸","🧦","🥔","⚠️","🦆"
  ];

  const messages = [
    "THE SILLY HAS BREACHED CONTAINMENT",
    "NOBRO.exe HAS STOPPED THINKING",
    "YOUR WEBSITE IS NOW PROPERTY OF BREAD",
    "CRITICAL GOOBER OVERLOAD",
    "THE COUNCIL HAS REJECTED YOUR CSS",
    "PLEASE INSERT 7 POTATOES",
    "WINDOWS HAS LEFT THE DIMENSION",
    "WHY IS THERE A LIZARD IN MY RAM",
    "SILLY LEVELS: UNREASONABLE",
    "THIS IS NOT A DRILL. THIS IS A SPOON."
  ];

  const random = arr =>
    arr[Math.floor(Math.random() * arr.length)];

  const style = document.createElement("style");
  style.textContent = `
    @keyframes sillySpin {
      to { transform: rotate(360deg); }
    }
    @keyframes sillyBounce {
      0%,100% { transform: translateY(0) rotate(0); }
      50% { transform: translateY(-45px) rotate(180deg); }
    }
    @keyframes sillyRainbow {
      to { filter: hue-rotate(360deg); }
    }
    @keyframes sillyPulse {
      0%,100% { scale: 1; }
      50% { scale: 1.15; }
    }
    .silly-chaos {
      position: fixed;
      pointer-events: none;
      z-index: 2147483646;
      font-family: Consolas, monospace;
      font-weight: 900;
    }
  `;
  document.head.appendChild(style);

  // THE PAGE HAS LOST ITS COLORS
  document.documentElement.style.animation =
    "sillyRainbow 4s linear infinite";

  // FLOATING CREATURE POPULATION
  const spawn = () => {
    const el = $("div", `
      position:fixed;
      left:${Math.random() * 95}vw;
      top:${Math.random() * 90}vh;
      font-size:${20 + Math.random() * 55}px;
      animation:sillyBounce ${0.5 + Math.random() * 2}s infinite;
      z-index:2147483646;
      pointer-events:none;
    `, random(emojis));

    state.timers.push(setTimeout(() => {
      el.remove();
      state.elements = state.elements.filter(x => x !== el);
    }, 10000));
  };

  // UNAUTHORIZED ANNOUNCEMENTS
  const announce = () => {
    const el = $("div", `
      position:fixed;
      top:${Math.random() * 75}vh;
      left:${Math.random() * 65}vw;
      background:#111;
      color:#00ff41;
      border:3px solid #00ff41;
      padding:14px;
      font: bold 16px Consolas,monospace;
      box-shadow:0 0 25px #00ff41;
      z-index:2147483647;
      animation:sillyPulse .3s infinite;
      max-width:300px;
    `, random(messages));

    state.timers.push(setTimeout(() => {
      el.remove();
      state.elements = state.elements.filter(x => x !== el);
    }, 3500));
  };

  // THE SILLY METER
  const meter = $("div", `
    position:fixed;
    bottom:15px;
    left:15px;
    padding:12px;
    background:#090909;
    color:#00ff41;
    border:2px solid #00ff41;
    font: bold 13px Consolas,monospace;
    z-index:2147483647;
    pointer-events:none;
    box-shadow:0 0 20px #00ff4166;
  `, "SILLY LEVEL: 0%");

  let silly = 0;

  const meterTimer = setInterval(() => {
    silly += Math.floor(Math.random() * 999);
    meter.textContent =
      `SILLY LEVEL: ${silly.toLocaleString()}%\n` +
      `BRAIN CELLS: ${Math.max(0, 3 - Math.floor(silly / 10000))}\n` +
      `REALITY: UNSTABLE`;
  }, 400);

  state.timers.push(meterTimer);

  // CHAOS PRODUCTION
  const spawnTimer = setInterval(spawn, 250);
  const announceTimer = setInterval(announce, 1800);

  state.timers.push(spawnTimer, announceTimer);

  // THE TITLE IS NO LONGER YOURS
  let titleIndex = 0;
  const titleTimer = setInterval(() => {
    document.title = random([
      "💀 SILLY BROWSER 💀",
      "NOBRO",
      "THE INTERNET IS MELTING",
      "BREAD DETECTED",
      "HELP",
      "SILLY.exe"
    ]);
  }, 1200);

  state.timers.push(titleTimer);

  // EMERGENCY SHUTDOWN
  window.stopSillyApocalypse = () => {
    state.running = false;
    state.timers.forEach(clearInterval);
    state.timers.forEach(clearTimeout);
    state.elements.forEach(el => el.remove());

    style.remove();
    meter.remove();

    document.documentElement.style.animation = "";
    document.title = state.originalTitle;

    delete window.sillyApocalypse;
    delete window.stopSillyApocalypse;

    console.log("SILLY APOCALYPSE TERMINATED.");
  };

  console.log("WARNING: SILLY LEVELS EXCEEDING LIMITS.");
})();
