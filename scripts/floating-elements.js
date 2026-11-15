// silly browser - floating elements
// makes all images and divs gently float up and down
(function() {
  const style = document.createElement('style');
  style.textContent = '@keyframes sillyFloat { 0%,100% { transform: translateY(0px); } 50% { transform: translateY(-10px); } }';
  document.head.appendChild(style);
  const els = document.querySelectorAll('img, div, span, p, h1, h2, h3');
  els.forEach(function(el, i) {
    el.style.animation = 'sillyFloat ' + (2 + Math.random() * 2) + 's ease-in-out infinite';
    el.style.animationDelay = (Math.random() * 2) + 's';
  });
  console.log('[silly] floating elements active!');
})();
