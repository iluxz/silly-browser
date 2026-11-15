// silly browser - meme text
// replaces random words on the page with silly replacements
(function() {
  const replacements = {
    'the': 'teh', 'and': 'an', 'you': 'u', 'are': 'r', 'to': '2', 'for': '4',
    'money': 'moneys', 'good': 'gud', 'great': 'gr8', 'love': 'luv',
    'please': 'pls', 'because': 'bcuz', 'people': 'peeps', 'friend': 'fren',
    'cat': 'kitty', 'dog': 'doggo', 'computer': 'compy', 'internet': 'interwebz'
  };
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(function(node) {
    let text = node.textContent;
    for (const [word, repl] of Object.entries(replacements)) {
      const regex = new RegExp('\\b' + word + '\\b', 'gi');
      text = text.replace(regex, repl);
    }
    node.textContent = text;
  });
  console.log('[silly] meme text active!');
})();
