// silly browser - text replacer (edit the map below)
(function() {
  const map = {"hello":"howdy","world":"earth","the":"teh"};
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(n => {
    let t = n.nodeValue;
    Object.keys(map).forEach(k => { t = t.split(k).join(map[k]); });
    n.nodeValue = t;
  });
  console.log("[silly] text replacer active!");
})();
