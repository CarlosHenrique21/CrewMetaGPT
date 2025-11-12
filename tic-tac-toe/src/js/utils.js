/*
  utils.js
  Utility functions
*/

// Simple helper to update scoreboard counts safely
export function incrementStat(stats, player, statType) {
  if (!stats[player]) {
    stats[player] = { wins: 0, losses: 0, draws: 0 };
  }
  if (statType === 'win') {
    stats[player].wins++;
  } else if (statType === 'loss') {
    stats[player].losses++;
  } else if (statType === 'draw') {
    stats['X'].draws++;
    stats['O'].draws++;
  }
}
