(() => {
  // silly browser - 3 in a row (tic-tac-toe) overlay
  if (window.sillyTicTacToe) return;
  window.sillyTicTacToe = true;

  const board = Array(9).fill(null);
  let current = "X";
  let gameOver = false;

  const container = document.createElement("div");
  container.id = "silly-ttt";
  container.style.cssText = "position:fixed;bottom:20px;right:20px;z-index:2147483647;background:#1a1530;border:3px solid #8b6cf0;border-radius:16px;padding:12px;font-family:Consolas,monospace;box-shadow:0 0 20px #8b6cf088;";

  const title = document.createElement("div");
  title.textContent = "3 in a row";
  title.style.cssText = "color:#8b6cf0;font-weight:900;font-size:14px;margin-bottom:8px;text-align:center;";
  container.appendChild(title);

  const status = document.createElement("div");
  status.textContent = "your turn (X)";
  status.style.cssText = "color:#e0ddf5;font-size:12px;margin-bottom:8px;text-align:center;";
  container.appendChild(status);

  const grid = document.createElement("div");
  grid.style.cssText = "display:grid;grid-template-columns:repeat(3,50px);gap:4px;";
  container.appendChild(grid);

  const cells = [];
  for (let i = 0; i < 9; i++) {
    const cell = document.createElement("button");
    cell.style.cssText = "width:50px;height:50px;font-size:24px;font-weight:900;background:#252040;color:#e0ddf5;border:2px solid #8b6cf0;border-radius:8px;cursor:pointer;";
    cell.onclick = () => makeMove(i);
    cells.push(cell);
    grid.appendChild(cell);
  }

  const resetBtn = document.createElement("button");
  resetBtn.textContent = "new game";
  resetBtn.style.cssText = "margin-top:8px;width:100%;padding:6px;background:#8b6cf0;color:#fff;border:0;border-radius:8px;cursor:pointer;font:700 12px Consolas;";
  resetBtn.onclick = reset;
  container.appendChild(resetBtn);

  // close button
  const closeBtn = document.createElement("button");
  closeBtn.textContent = "×";
  closeBtn.style.cssText = "position:absolute;top:4px;right:8px;background:none;border:0;color:#9a93b8;font-size:18px;cursor:pointer;";
  closeBtn.onclick = () => container.remove();
  container.appendChild(closeBtn);

  document.body.appendChild(container);

  const wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];

  function checkWin() {
    for (const [a,b,c] of wins) {
      if (board[a] && board[a] === board[b] && board[a] === board[c]) return board[a];
    }
    if (board.every(c => c)) return "draw";
    return null;
  }

  function makeMove(i) {
    if (gameOver || board[i]) return;
    board[i] = current;
    cells[i].textContent = current;
    cells[i].style.color = current === "X" ? "#5cb8f0" : "#ff8fb1";
    const result = checkWin();
    if (result) {
      gameOver = true;
      if (result === "draw") {
        status.textContent = "it's a draw!";
      } else {
        status.textContent = result + " wins!";
        // highlight winning cells
        for (const [a,b,c] of wins) {
          if (board[a] === result) {
            cells[a].style.background = "#3a3060";
            cells[b].style.background = "#3a3060";
            cells[c].style.background = "#3a3060";
          }
        }
      }
    } else {
      current = current === "X" ? "O" : "X";
      status.textContent = "your turn (" + current + ")";
    }
  }

  function reset() {
    board.fill(null);
    gameOver = false;
    current = "X";
    status.textContent = "your turn (X)";
    cells.forEach(c => {
      c.textContent = "";
      c.style.background = "#252040";
      c.style.color = "#e0ddf5";
    });
  }

  console.log("[silly] 3 in a row active! click to play.");
})();
