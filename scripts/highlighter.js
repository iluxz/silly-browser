// silly browser - element highlighter (hover to see box)
(function() {
  const box = document.createElement("div");
  box.style.cssText = "position:fixed;pointer-events:none;z-index:999999;border:2px solid #ff6b6b;background:rgba(255,107,107,0.1);transition:all .1s;display:none;";
  document.body.appendChild(box);
  document.addEventListener("mousemove", e => {
    const el = document.elementFromPoint(e.clientX, e.clientY);
    if (!el || el === box) return;
    const r = el.getBoundingClientRect();
    box.style.left = r.left + "px";
    box.style.top = r.top + "px";
    box.style.width = r.width + "px";
    box.style.height = r.height + "px";
    box.style.display = "block";
  });
  console.log("[silly] element highlighter active! hover to inspect.");
})();
