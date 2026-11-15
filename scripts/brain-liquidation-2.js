(() => {
  if (window.brainLiquidation2) return;

  const S = window.brainLiquidation2 = {
    timers: [],
    nodes: [],
    originalTitle: document.title,
    count: 0
  };

  const random = a => a[Math.floor(Math.random() * a.length)];
  const emojis = [
    "💀","🗿","🍞","🦎","🧠","🚨","🐸",
    "🥔","🧌","🦆","📉","🛸","⚠️","🧀",
    "🧯","🪑","🫠","💻"
  ];

  const messages = [
    "BRAIN CELL DEFAULTED ON ITS LOANS",
    "CRITICAL NOBRO DETECTED",
    "THE NEURONS HAVE UNIONIZED",
    "WINDOWS HAS FILED FOR DIVORCE",
    "YOUR LAST BRAIN CELL IS ON BREAK",
    "ERROR 404: THOUGHT NOT FOUND",
    "THE POTATO IS NOW THE ADMINISTRATOR",
    "PLEASE RETURN YOUR COGNITIVE LICENSE",
    "INTEL HAS LEFT THE BUILDING",
    "NVIDIA IS SELLING YOUR NEURONS",
    "THE COUNCIL DEMANDS MORE BREAD",
    "REALITY.EXE HAS STOPPED RESPONDING",
    "YOUR MOUSE IS NOW A GOVERNMENT EMPLOYEE",
    "THOUGHT.exe WAS NOT RESPONDING",
    "THE SILLY HAS BECOME SENTIENT"
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
    @keyframes brainSpin {
      to { transform:rotate(360deg); }
    }
    @keyframes brainBounce {
      0%,100% { transform:translateY(0) rotate(0); }
      50% { transform:translateY(-80px) rotate(180deg); }
    }
    @keyframes brainPulse {
      0%,100% { scale:1; }
      50% { scale:1.2; }
    }
    @keyframes brainShake {
      0%,100% { translate:0 0; }
      25% { translate:8px -5px; }
      75% { translate:-8px 5px; }
    }
    .brain-liquid {
      position:fixed;
      pointer-events:none;
      z-index:2147483646;
      font-family:Consolas,monospace;
      font-weight:900;
    }
  `;
  document.head.appendChild(style);

  // THE EMOJI FACTORY
  function spawnEmoji() {
    const e = add("div", `
      position:fixed;
      left:${Math.random()*95}vw;
      top:${Math.random()*90}vh;
      font-size:${20+Math.random()*70}px;
      animation:brainBounce ${0.3+Math.random()*1.5}s infinite;
      z-index:2147483646;
      pointer-events:none;
    `, random(emojis));

    later(() => remove(e), 7000);
  }

  // FAKE ERROR WINDOWS
  function errorWindow() {
    const e = add("div", `
      position:fixed;
      left:${Math.random()*65}vw;
      top:${Math.random()*65}vh;
      width:260px;
      padding:12px;
      background:#c0c0c0;
      color:black;
      border:3px outset white;
      font: bold 13px Arial;
      z-index:2147483647;
      box-shadow:5px 5px 0 #0008;
      animation:brainShake .15s infinite;
    `, "");

    const title = document.createElement("div");
    title.textContent = "⚠ BRAIN.EXE ERROR";
    title.style.cssText =
      "background:navy;color:white;padding:6px;margin-bottom:10px";
    e.appendChild(title);

    const body = document.createElement("div");
    body.textContent = random(messages);
    e.appendChild(body);

    const button = document.createElement("button");
    button.textContent = "ok i guess";
    button.style.cssText = "margin-top:12px;padding:5px 18px";
    button.onclick = () => remove(e);
    e.appendChild(button);

    later(() => remove(e), 6500);
  }

  // GIANT ANNOUNCEMENTS
  function announcement() {
    const e = add("div", `
      position:fixed;
      top:${Math.random()*75}vh;
      left:${Math.random()*45}vw;
      color:${random(["#ff0044","#00ff41","#ffff00","#00ccff"])};
      font:bold ${20+Math.random()*35}px Consolas;
      text-shadow:3px 3px black;
      z-index:2147483647;
      pointer-events:none;
      animation:brainPulse .3s infinite;
      max-width:90vw;
    `, random(messages));

    later(() => remove(e), 2500);
  }

  // THE FINANCIAL DEPARTMENT
  const meter = add("div", `
    position:fixed;
    bottom:12px;
    left:12px;
    background:#050505;
    color:#00ff41;
    border:2px solid #00ff41;
    padding:12px;
    font: bold 13px Consolas;
    z-index:2147483647;
    pointer-events:none;
    white-space:pre-line;
    box-shadow:0 0 20px #00ff4166;
  `, "BRAIN LIQUIDATION INC.");

  function diagnostics() {
    S.count += Math.floor(Math.random()*5000);
    meter.textContent =
      "BRAIN LIQUIDATION INC.\n" +
      "----------------------\n" +
      "THOUGHTS: " + S.count + "\n" +
      "BRAIN CELLS: " + random(["-4","0","404","NULL","OVERDUE"]) + "\n" +
      "CPU: " + random(["POTATO","BREAD","NOBRO","YES"]) + "\n" +
      "REALITY: " + random(["MISSING","FROZEN","GOOFY","DELISTED"]) + "\n" +
      "STOCK PRICE: -999999%";
  }

  // TIMER MANAGEMENT
  function later(fn, ms) {
    const id = setTimeout(fn, ms);
    S.timers.push({id, interval:false});
  }

  function repeat(fn, ms) {
    const id = setInterval(fn, ms);
    S.timers.push({id, interval:true});
  }

  function remove(e) {
    e.remove();
    S.nodes = S.nodes.filter(n => n !== e);
  }

  // THE MARKET CRASHES
  repeat(spawnEmoji, 120);
  repeat(errorWindow, 1800);
  repeat(announcement, 700);
  repeat(diagnostics, 350);

  // THE DOCUMENT TITLE IS CONFISCATED
  repeat(() => {
    document.title = random([
      "💀 BRAIN LIQUIDATION",
      "NOBRO.EXE",
      "ERROR 404",
      "POTATO ADMIN",
      "HELP",
      "THE COUNCIL",
      "BREAD BROWSER"
    ]);
  }, 800);

  // EMERGENCY TERMINATION
  window.stopBrainLiquidation2 = () => {
    S.timers.forEach(t =>
      t.interval ? clearInterval(t.id) : clearTimeout(t.id)
    );

    S.nodes.forEach(n => n.remove());
    style.remove();
    document.title = S.originalTitle;

    delete window.brainLiquidation2;
    delete window.stopBrainLiquidation2;

    console.log("BRAIN LIQUIDATION #2: TERMINATED.");
  };

  console.log("BRAIN LIQUIDATION #2: MARKET COLLAPSE INITIATED.");
})();
