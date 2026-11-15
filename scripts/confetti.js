// silly browser - confetti explosion
// click anywhere to trigger a confetti explosion
(function() {
  const colors = ['#ff0000','#ff7f00','#ffff00','#00ff00','#0000ff','#4b0082','#9400d3','#ff69b4','#00ffff','#ffffff'];
  document.addEventListener('click', function(e) {
    for (let i = 0; i < 30; i++) {
      const piece = document.createElement('div');
      const angle = Math.random() * Math.PI * 2;
      const speed = 2 + Math.random() * 4;
      const vx = Math.cos(angle) * speed;
      const vy = Math.sin(angle) * speed - 3;
      piece.style.cssText = 'position:fixed;pointer-events:none;z-index:999999;width:8px;height:8px;background:' + colors[Math.floor(Math.random()*colors.length)] + ';left:' + e.clientX + 'px;top:' + e.clientY + 'px;border-radius:' + (Math.random() > 0.5 ? '50%' : '0');
      document.body.appendChild(piece);
      let x = e.clientX, y = e.clientY, vy2 = vy, gravity = 0.15;
      const interval = setInterval(function() {
        x += vx; y += vy2; vy2 += gravity;
        piece.style.left = x + 'px'; piece.style.top = y + 'px';
        piece.style.opacity = parseFloat(piece.style.opacity || 1) - 0.01;
        if (y > window.innerHeight + 50 || parseFloat(piece.style.opacity) <= 0) {
          piece.remove(); clearInterval(interval);
        }
      }, 16);
    }
  });
  console.log('[silly] confetti explosion active! click anywhere!');
})();
