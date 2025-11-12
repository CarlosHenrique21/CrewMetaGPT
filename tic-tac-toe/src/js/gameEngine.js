/*
  gameEngine.js
  Handles game state, rules, move validation, win/draw detection
*/

export default class GameEngine {
  constructor() {
    this.board = Array(9).fill(null); // 3x3 grid flattened
    this.currentPlayer = 'X';
    this.isGameOver = false;
    this.winner = null; // 'X', 'O', or 'Draw'
    this.moveHistory = [];
  }

  startNewGame() {
    this.board.fill(null);
    this.currentPlayer = 'X';
    this.isGameOver = false;
    this.winner = null;
    this.moveHistory = [];
  }

  // Validate and perform move
  makeMove(cellIndex) {
    if (this.isGameOver) {
      throw new Error('Game is already over.');
    }
    if (cellIndex < 0 || cellIndex > 8) {
      throw new Error('Invalid cell index.');
    }
    if (this.board[cellIndex] !== null) {
      throw new Error('Cell is already occupied.');
    }
    this.board[cellIndex] = this.currentPlayer;
    this.moveHistory.push(cellIndex);
    if (this.checkWin(this.currentPlayer)) {
      this.isGameOver = true;
      this.winner = this.currentPlayer;
    } else if (this.board.every(cell => cell !== null)) {
      this.isGameOver = true;
      this.winner = 'Draw';
    } else {
      this.currentPlayer = this.currentPlayer === 'X' ? 'O' : 'X';
    }
  }

  // Returns true if player has won
  checkWin(player) {
    // Winning combinations indices
    const wins = [
      [0,1,2],[3,4,5],[6,7,8], // Rows
      [0,3,6],[1,4,7],[2,5,8], // Columns
      [0,4,8],[2,4,6]          // Diagonals
    ];

    return wins.some(combo => combo.every(i => this.board[i] === player));
  }

  // Undo the last move
  undoMove() {
    if (this.moveHistory.length === 0 || this.isGameOver) {
      throw new Error('No moves to undo or game is over.');
    }
    const lastMove = this.moveHistory.pop();
    this.board[lastMove] = null;
    this.isGameOver = false;
    this.winner = null;
    this.currentPlayer = this.currentPlayer === 'X' ? 'O' : 'X';
  }

  getGameStatus() {
    if (this.isGameOver) {
      if (this.winner === 'Draw') {
        return 'Draw';
      }
      return `${this.winner} wins`;
    }
    return `${this.currentPlayer}'s turn`;
  }
}
