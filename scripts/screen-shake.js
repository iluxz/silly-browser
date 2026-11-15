// silly browser - screen shake
// makes the page shake gently every few seconds
(function() {
  setInterval(function() {
    document.body.style.transition = 'transform 0.1s';
    document.body.style.transform = 'translate(' + (Math.random()*6-3) + 'px,' + (Math.random()*6-3) + 'px) rotate(' + (Math.random()*2-1) + 'deg)';
    setTimeout(function() {
      document.body.style.transform = 'translate(0,0) rotate(0deg)';
    }, 100);
  }, 3000);
  console.log('[silly] screen shake active!');
})();
