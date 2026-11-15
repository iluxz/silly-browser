(() => {
  // silly+ premium: gravity (elements fall to the bottom)
  const els = document.querySelectorAll("img, button, h1, h2, h3, p, a, div");
  const targets = Array.from(els).slice(0, 40);
  targets.forEach((el, i) => {
    const rect = el.getBoundingClientRect();
    el.style.position = "fixed";
    el.style.left = rect.left + "px";
    el.style.top = rect.top + "px";
    el.style.transition = "top 2s ease-in, transform 2s ease-in";
    setTimeout(() => {
      el.style.top = (window.innerHeight - rect.height - 10) + "px";
      el.style.transform = "rotate(" + (Math.random() * 20 - 10) + "deg)";
    }, i * 50);
  });
  console.log("[silly+] gravity activated! %d elements falling.", targets.length);
})();
