(() => {
  window.stopBrainLiquidationTres?.();

  const S = {
    nodes: [],
    timers: [],
    running: true,
    revenue: 0,
    braincells: 50,
    acquisitions: 0,
    debt: 0
  };

  const add = (el) => {
    document.body.appendChild(el);
    S.nodes.push(el);
    return el;
  };

  const announcements = [
    "nobro technologies has acquired a suspicious rock.",
    "potato computing has announced potato 2.",
    "the bread foundation has lost its entire bread supply.",
    "windows 95 holdings has declared bankruptcy and restarted.",
    "lizard capital has invested in a ceiling fan.",
    "spoon industries has acquired 400 spoons.",
    "roof gator industries has entered the market.",
    "the ceo has requested another braincell.",
    "shareholders have begun communicating in morse code.",
    "brain liquidation inc. has acquired the moon. probably."
  ];

  const ceoMessages = [
    "i have reviewed the numbers. there are numbers.",
    "we are experiencing unprecedented spoon growth.",
    "the economy is a social construct.",
    "please stop feeding the server potatoes.",
    "i am pleased to announce that i found a braincell.",
    "our financial department is a calculator.",
    "the board meeting has been postponed due to lizard activity."
  ];

  const panel = add(document.createElement("div"));
  panel.innerHTML = `
    <div style="font-size:21px;font-weight:900">
      🧠 brain liquidation inc.
    </div>
    <div style="opacity:.65;font-size:11px;margin:4px 0 12px">
      corporate operations terminal · version tres
    </div>
    <div id="bl3-revenue">revenue: $0</div>
    <div id="bl3-brain">braincells: 50</div>
    <div id="bl3-debt">corporate debt: $0</div>
    <div id="bl3-acquisitions">acquisitions: 0</div>
    <hr style="border-color:#ffffff33">
    <div id="bl3-status">status: operational-ish</div>
    <div style="margin-top:12px;font-size:10px;opacity:.6">
      stock: BRAIN · exchange: basement
    </div>
  `;

  Object.assign(panel.style, {
    position: "fixed",
    top: "15px",
    right: "15px",
    width: "290px",
    padding: "18px",
    background: "#171522",
    color: "#e8ddff",
    border: "2px solid #9d75ed",
    borderRadius: "14px",
    font: "13px monospace",
    lineHeight: "1.7",
    zIndex: "2147483647",
    boxShadow: "0 8px 35px #0009"
  });

  const ticker = add(document.createElement("div"));
  ticker.textContent =
    " BRAIN ▲ +900%  |  NOBRO ▲ +12  |  POTATO COMPUTING ▲ 404  |  WINDOWS 95 ▼ NOT RESPONDING  | ";

  Object.assign(ticker.style, {
    position: "fixed",
    bottom: "0",
    left: "0",
    width: "100%",
    padding: "12px 0",
    background: "#241634",
    color: "#d9bcff",
    font: "bold 13px monospace",
    whiteSpace: "nowrap",
    overflow: "hidden",
    zIndex: "2147483647",
    borderTop: "2px solid #9d75ed"
  });

  const tickerText = document.createElement("span");
  tickerText.textContent = ticker.textContent.repeat(3);
  ticker.appendChild(tickerText);

  let tickerPosition = 0;

  S.timers.push(setInterval(() => {
    tickerPosition -= 2;
    if (tickerPosition < -tickerText.offsetWidth / 3) {
      tickerPosition = 0;
    }
    tickerText.style.display = "inline-block";
    tickerText.style.transform = `translateX(${tickerPosition}px)`;
  }, 30));

  function popup(message, color = "#fff0b8") {
    const el = document.createElement("div");
    el.textContent = message;

    Object.assign(el.style, {
      position: "fixed",
      left: Math.random() * 65 + 5 + "vw",
      top: Math.random() * 65 + 10 + "vh",
      maxWidth: "270px",
      padding: "13px 16px",
      background: color,
      color: "#302438",
      border: "2px solid #9d75ed",
      borderRadius: "10px",
      font: "bold 13px monospace",
      boxShadow: "0 5px 22px #0006",
      zIndex: "2147483646"
    });

    add(el);
    S.timers.push(setTimeout(() => el.remove(), 5500));
  }

  function update() {
    panel.querySelector("#bl3-revenue").textContent =
      "revenue: $" + Math.floor(S.revenue).toLocaleString();

    panel.querySelector("#bl3-brain").textContent =
      "braincells: " + S.braincells.toFixed(1);

    panel.querySelector("#bl3-debt").textContent =
      "corporate debt: $" + Math.floor(S.debt).toLocaleString();

    panel.querySelector("#bl3-acquisitions").textContent =
      "acquisitions: " + S.acquisitions;

    panel.querySelector("#bl3-status").textContent =
      S.braincells < 10 ? "status: braincell emergency" :
      S.debt > S.revenue ? "status: financially questionable" :
      S.revenue > 100000 ? "status: suspiciously successful" :
      "status: operational-ish";
  }

  S.timers.push(setInterval(() => {
    S.revenue += Math.random() * 2500;
    S.debt += Math.random() * 700;
    S.braincells = Math.max(0, S.braincells - Math.random() * 1.5);
    update();
  }, 1000));

  S.timers.push(setInterval(() => {
    S.acquisitions++;
    popup(
      "📈 ACQUISITION #" + S.acquisitions + ": " +
      announcements[Math.floor(Math.random() * announcements.length)],
      "#dfffdc"
    );
  }, 8000));

  S.timers.push(setInterval(() => {
    popup(
      "👔 CEO UPDATE: " +
      ceoMessages[Math.floor(Math.random() * ceoMessages.length)],
      "#e9dcff"
    );
  }, 11000));

  S.timers.push(setInterval(() => {
    const el = document.createElement("div");
    const items = ["🧠", "💵", "🥔", "🍞", "🦎", "📈", "🥄"];

    el.textContent = items[Math.floor(Math.random() * items.length)];

    Object.assign(el.style, {
      position: "fixed",
      left: Math.random() * 95 + "vw",
      top: "105vh",
      fontSize: "28px",
      pointerEvents: "none",
      zIndex: "2147483645",
      transition: "transform 8s linear, opacity 8s linear"
    });

    add(el);

    requestAnimationFrame(() => {
      el.style.transform = "translateY(-120vh) rotate(540deg)";
      el.style.opacity = "0";
    });

    S.timers.push(setTimeout(() => el.remove(), 8500));
  }, 900));

  window.brainLiquidationTres = S;

  window.stopBrainLiquidationTres = () => {
    S.running = false;
    S.timers.forEach(clearInterval);
    S.timers.forEach(clearTimeout);
    S.nodes.forEach(el => el.remove());
    delete window.brainLiquidationTres;
    delete window.stopBrainLiquidationTres;
    console.log("[brain liquidation] tres shut down.");
  };

  update();
  console.log("[brain liquidation] tres is operational.");
})();
