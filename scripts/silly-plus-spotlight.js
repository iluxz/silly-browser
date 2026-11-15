(() => {
  // silly+ premium: cursor spotlight (darkens page, spotlight follows cursor)
  const overlay = document.createElement("div");
  overlay.style.cssText = "position:fixed;inset:0;pointer-events:none;z-index:999998;background:radial-gradient(circle 120px at 50% 50%, transparent 0%, rgba(0,0,0,0.6) 100%);transition:background .1s;";
  document.body.appendChild(overlay);
  document.addEventListener("mousemove", (e) => {
    overlay.style.background = "radial-gradient(circle 120px at " + e.clientX + "px " + e.clientY + "px, transparent 0%, rgba(0,0,0,0.6) 100%)";
  });
  console.log("[silly+] cursor spotlight active! move your mouse.");
})();
