(() => {
  window.stopBrainLiquidation2?.();

  const S = {
    nodes: [],
    timers: [],
    running: true,
    revenue: 0,
    braincells: 100
  };

  const add = (el) => {
    document.body.appendChild(el);
    S.nodes.push(el);
    return el;
  };

  const style = (el, css) => Object.assign(el.style, css);

  const panel = add(document.createElement("div"));
  panel.innerHTML = `
    <div style="font-size:20px;font-weight:900;margin-bottom:8px">
      🧠 brain liquidation inc.
    </div>
    <div>quarterly financial report</div>
    <hr style="border-color:#ffffff44">
    <div id="bli-revenue">revenue: $0</div>
    <div id="bli-brain">braincells: 100</div>
    <div id="bli-status">status: questionably profitable</div>
    <div style="font-size:11px;margin-top:12px;opacity:.7">
      ticker: BRAIN · est. 1995
    </div>
  `;

  style(panel, {
    position: "fixed",
    top: "18px",
    right: "18px",
    zIndex: "2147483647",
    width: "260px",
    padding: "18px",
    background: "#21152e",
    color: "#f5eaff",
    border: "2px solid #b68cff",
    borderRadius: "14px",
    font: "14px monospace",
    boxShadow: "0 8px 35px #0008"
  });

  const announcements = [
    "nobro technologies has acquired 3 spoons.",
    "potato computing reports a 900% potato increase.",
    "the bread foundation has misplaced the bread.",
    "windows 95 holdings has stopped responding.",
    "neuron destruction llc has filed a suspicious invoice.",
    "the ceo has discovered a second braincell.",
    "shareholders are requesting an explanation.",
    "brain liquidation inc. is now accepting rocks."
  ];

  function popup(message) {
    const el = document.createElement("div");
    el.textContent = message;

    style(el, {
      position: "fixed",
      left: Math.random() * 65 + 5 + "vw",
      top: Math.random() * 65 + 10 + "vh",
      zIndex: "2147483646",
      padding: "12px 16px",
      maxWidth: "260px",
      background: "#fff0b8",
      color: "#382b1d",
      border: "2px solid #d6a84d",
      borderRadius: "10px",
      font: "bold 13px monospace",
      boxShadow: "0 5px 20px #0005"
    });

    add(el);
    S.timers.push(setTimeout(() => el.remove(), 5000));
  }

  const floating = ["💵", "🧠", "🥔", "🍞", "📈", "🪑", "🦎"];

  S.timers.push(setInterval(() => {
    if (!S.running) return;

    S.revenue += Math.floor(Math.random() * 900);
    S.braincells = Math.max(0, S.braincells - Math.random() * 2);

    panel.querySelector("#bli-revenue").textContent =
      "revenue: $" + S.revenue.toLocaleString();

    panel.querySelector("#bli-brain").textContent =
      "braincells: " + S.braincells.toFixed(1);

    panel.querySelector("#bli-status").textContent =
      S.braincells < 20 ? "status: critical brain shortage" :
      S.revenue > 10000 ? "status: suspiciously wealthy" :
      "status: questionably profitable";
  }, 1000));

  S.timers.push(setInterval(() => {
    const el = document.createElement("div");
    el.textContent = floating[Math.floor(Math.random() * floating.length)];

    style(el, {
      position: "fixed",
      left: Math.random() * 95 + "vw",
      top: "105vh",
      fontSize: "30px",
      zIndex: "2147483645",
      pointerEvents: "none",
      transition: "transform 7s linear, opacity 7s linear"
    });

    add(el);

    requestAnimationFrame(() => {
      el.style.transform = "translateY(-120vh) rotate(720deg)";
      el.style.opacity = "0";
    });

    S.timers.push(setTimeout(() => el.remove(), 7500));
  }, 650));

  S.timers.push(setInterval(() => {
    popup(announcements[Math.floor(Math.random() * announcements.length)]);
  }, 4500));

  window.brainLiquidation2 = S;

  window.stopBrainLiquidation2 = () => {
    S.running = false;
    S.timers.forEach(clearInterval);
    S.timers.forEach(clearTimeout);
    S.nodes.forEach(el => el.remove());
    delete window.brainLiquidation2;
    delete window.stopBrainLiquidation2;
    console.log("[brain liquidation] #2 shut down.");
  };

  console.log("[brain liquidation] #2 is operational.");
})();
