/*
  app.js
  Entry point and UI logic integration with gameEngine and storage modules
*/
import GameEngine from './gameEngine.js';
import {saveStats, loadStats} from './storage.js';
import {incrementStat} from './utils.js';

const game = new GameEngine();

// Elements
const cells = document.querySelectorAll('.cell');
const statusEl = document.getElementById('status');
const restartBtn = document.getElementById('restart-btn');
const xWinsEl = document.getElementById('x-wins');
const oWinsEl = document.getElementById('o-wins');
const drawsEl = document.getElementById('draws');

// Game stats loaded from localStorage or defaults
let stats = loadStats() || { X: { wins: 0, losses: 0, draws: 0 }, O: { wins: 0, losses: 0, draws: 0 } };

function updateScoreboard() {
  xWinsEl.textContent = stats.X.wins;
  oWinsEl.textContent = stats.O.wins;
  drawsEl.textContent = stats.X.draws; // draws are same for both
}

function updateUI() {
  // Update cells
  cells.forEach((cell, index) => {
    cell.textContent = game.board[index] || '';
    cell.disabled = game.isGameOver || Boolean(game.board[index]);
  });
  // Update status message
  statusEl.textContent = game.getGameStatus();
}

function handleCellClick(e) {
  const index = Number(e.target.getAttribute('data-cell-index'));
  try {
    game.makeMove(index);
  } catch (error) {
    alert(error.message);
    return;
  }
  updateUI();

  if (game.isGameOver) {
    if (game.winner === 'Draw') {
      // Increment draw stats for both players
      stats.X.draws++;
      stats.O.draws++;
      saveStats(stats);
    } else {
      // Increment winner wins and loser losses
      incrementStat(stats, game.winner, 'win');
      const loser = (game.winner === 'X') ? 'O' : 'X';
      incrementStat(stats, loser, 'loss');
      saveStats(stats);
    }
    updateScoreboard();
  }
}

function restartGame() {
  game.startNewGame();
  updateUI();
}

// Initialization
updateScoreboard();
updateUI();

// Event listeners
cells.forEach(cell => cell.addEventListener('click', handleCellClick));
restartBtn.addEventListener('click', restartGame);

window.addEventListener('load', () => {
  // On load, could load preferences in future or other setup
});
