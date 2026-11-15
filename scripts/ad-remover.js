// silly browser - ad remover (best effort)
(function() {
  const selectors = ['[class*="ad-"]','[id*="ad-"]','[class*="banner"]','iframe[src*="ads"]','[class*="sponsor"]','[class*="promo"]'];
  let removed = 0;
  selectors.forEach(s => {
    document.querySelectorAll(s).forEach(el => { el.remove(); removed++; });
  });
  console.log("[silly] ad remover: removed " + removed + " elements.");
})();
