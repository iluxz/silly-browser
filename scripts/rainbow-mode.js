// silly browser - rainbow mode
// makes the entire page slowly shift through rainbow colors
(function() {
  let hue = 0;
  setInterval(function() {
    hue = (hue + 1) % 360;
    document.body.style.filter = 'hue-rotate(' + hue + 'deg)';
  }, 50);
  console.log('[silly] rainbow mode active!');
})();
