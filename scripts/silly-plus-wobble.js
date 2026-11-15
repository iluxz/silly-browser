(() => {
  // silly+ premium: page wobble (subtle earthquake effect)
  let intensity = 0.5;
  setInterval(() => {
    const x = (Math.random() - 0.5) * intensity;
    const y = (Math.random() - 0.5) * intensity;
    const r = (Math.random() - 0.5) * intensity * 0.5;
    document.body.style.transform = "translate(" + x + "px," + y + "px) rotate(" + r + "deg)";
  }, 50);
  console.log("[silly+] page wobble active! intensity:", intensity);
})();
