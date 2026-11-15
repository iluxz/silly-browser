(() => {
  // silly+ supporter script: star trail on every page
  const stars = ["⭐", "✨", "💫", "🌟"];
  const trail = [];
  const MAX = 20;

  document.addEventListener("mousemove", (e) => {
    if (trail.length >= MAX) {
      const old = trail.shift();
      old.remove();
    }
    const s = document.createElement("div");
    s.textContent = stars[Math.floor(Math.random() * stars.length)];
    s.style.cssText = "position:fixed;pointer-events:none;z-index:999999;font-size:14px;left:" + (e.clientX + 4) + "px;top:" + (e.clientY + 4) + "px;transition:opacity .8s,transform .8s;opacity:1;";
    document.body.appendChild(s);
    trail.push(s);
    setTimeout(() => {
      s.style.opacity = "0";
      s.style.transform = "translateY(-20px) scale(0.5)";
      setTimeout(() => { s.remove(); trail.splice(trail.indexOf(s), 1); }, 800);
    }, 300);
  });

  // supporter badge in console
  console.log("%c⭐ silly+ supporter", "color:#ffd700;font-size:16px;font-weight:bold;text-shadow:0 0 4px #ffd700");
  console.log("[silly+] star trail active! move your mouse.");
})();
