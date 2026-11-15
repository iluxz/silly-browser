// silly browser - element picker (click to get selector)
(function() {
  const box = document.createElement("div");
  box.style.cssText = "position:fixed;pointer-events:none;z-index:999999;border:2px solid #ff6b6b;background:rgba(255,107,107,0.15);transition:all .08s;";
  document.body.appendChild(box);
  let active = true;
  const handler = (e) => {
    if (!active) return;
    const el = document.elementFromPoint(e.clientX, e.clientY);
    if (!el || el === box) return;
    const r = el.getBoundingClientRect();
    box.style.left = r.left + "px";
    box.style.top = r.top + "px";
    box.style.width = r.width + "px";
    box.style.height = r.height + "px";
    e.preventDefault();
    e.stopPropagation();
    // build selector
    let sel = el.tagName.toLowerCase();
    if (el.id) sel = "#" + el.id;
    else if (el.className) sel += "." + el.className.trim().split(/\s+/).join(".");
    console.log("[silly picker] selector:", sel, "| text:", (el.textContent||"").slice(0,60));
    if (navigator.clipboard) navigator.clipboard.writeText(sel).catch(()=>{});
    active = false;
    box.style.border = "2px solid #69db7c";
    setTimeout(() => { box.remove(); active = true; }, 1500);
  };
  document.addEventListener("click", handler, true);
  console.log("[silly] element picker active! click any element to get its selector (copied to clipboard).");
})();
