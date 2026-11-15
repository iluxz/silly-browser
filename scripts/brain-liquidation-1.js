(() => {
  window.stopSillyMeltdown?.();

  const S = {
    nodes: [],
    timers: []
  };

  const add = (el) => {
    document.body.appendChild(el);
    S.nodes.push(el);
    return el;
  };

  const messages = [
    "the internet is melting",
    "error: too much silly detected",
    "your browser has become sentient",
    "please remain calm. the pixels are escaping.",
    "system notification: everything is fine.",
    "the website has been promoted to ceo.",
    "loading more internet...",
    "404: common sense not found"
  ];

  const banner = add(document.createElement("div"));
  banner.textContent = "⚠ THE INTERNET IS MELTING ⚠";

  Object.assign(banner.style, {
    position: "fixed",
    top: "0",
    left: "0",
    width: "100%",
    padding: "15px",
    textAlign: "center",
    background: "#ff3d63",
    color: "white",
    font: "bold 20px monospace",
    zIndex: "2147483647",
    boxShadow: "0 5px 20px #0005"
  });

  S.timers.push(setInterval(() => {
    const el = document.createElement("div");
    el.textContent = messages[Math.floor(Math.random() * messages.length)];

    Object.assign(el.style, {
      position: "fixed",
      left: Math.random() * 75 + 5 + "vw",
      top: Math.random() * 75 + 10 + "vh",
      padding: "12px",
      background: ["#fff0a8", "#d9c4ff", "#b9f4ff", "#ffc9dc"][
        Math.floor(Math.random() * 4)
      ],
      color: "#292033",
      border: "2px solid #292033",
      borderRadius: "8px",
      font: "bold 13px monospace",
      zIndex: "2147483646",
      boxShadow: "4px 4px 0 #0004"
    });

    add(el);
    S.timers.push(setTimeout(() => el.remove(), 4000));
  }, 1200));

  const emojis = ["💀", "🧠", "🗿", "🌐", "⚠️", "📦", "🥔"];

  S.timers.push(setInterval(() => {
    const el = document.createElement("div");
    el.textContent = emojis[Math.floor(Math.random() * emojis.length)];

    Object.assign(el.style, {
      position: "fixed",
      left: Math.random() * 95 + "vw",
      top: Math.random() * 95 + "vh",
      fontSize: "32px",
      pointerEvents: "none",
      zIndex: "2147483645",
      transform: `rotate(${Math.random() * 360}deg)`
    });

    add(el);
    S.timers.push(setTimeout(() => el.remove(), 3000));
  }, 500));

  S.timers.push(setInterval(() => {
    banner.style.background =
      ["#ff3d63", "#8d55e8", "#167c80", "#d68a22"][
        Math.floor(Math.random() * 4)
      ];
  }, 700));

  window.sillyMeltdown = S;

  window.stopSillyMeltdown = () => {
    S.timers.forEach(clearInterval);
    S.timers.forEach(clearTimeout);
    S.nodes.forEach(el => el.remove());
    delete window.sillyMeltdown;
    delete window.stopSillyMeltdown;
    console.log("[silly meltdown] internet restored.");
  };

  console.log("[silly meltdown] initiated.");
})();
