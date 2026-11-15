// silly browser - cursor trail
// makes your cursor leave a trail of colorful dots
(function() {
  const colors = ['#ff00ff','#00ffff','#ffff00','#ff0000','#00ff00','#0000ff'];
  let i = 0;
  document.addEventListener('mousemove', function(e) {
    const dot = document.createElement('div');
    dot.style.cssText = 'position:fixed;pointer-events:none;z-index:999999;width:8px;height:8px;border-radius:50%;background:' + colors[i % colors.length] + ';left:' + (e.clientX - 4) + 'px;top:' + (e.clientY - 4) + 'px;transition:opacity 0.5s,transform 0.5s;';
    document.body.appendChild(dot);
    i++;
    setTimeout(function() {
      dot.style.opacity = '0';
      dot.style.transform = 'scale(0)';
    }, 50);
    setTimeout(function() { dot.remove(); }, 600);
  });
  console.log('[silly] cursor trail active!');
})();
