/*
  storage.js
  Handles saving and loading game statistics and user preferences to/from localStorage
*/

const STORAGE_KEY_STATS = 'tic-tac-toe-stats';
const STORAGE_KEY_PREFS = 'tic-tac-toe-prefs';

export function saveStats(stats) {
  try {
    const serialized = JSON.stringify(stats);
    localStorage.setItem(STORAGE_KEY_STATS, serialized);
  } catch (e) {
    console.error('Failed to save stats:', e);
  }
}

export function loadStats() {
  try {
    const serialized = localStorage.getItem(STORAGE_KEY_STATS);
    if (!serialized) return null;
    return JSON.parse(serialized);
  } catch (e) {
    console.error('Failed to load stats:', e);
    return null;
  }
}

export function savePreferences(prefs) {
  try {
    const serialized = JSON.stringify(prefs);
    localStorage.setItem(STORAGE_KEY_PREFS, serialized);
  } catch (e) {
    console.error('Failed to save preferences:', e);
  }
}

export function loadPreferences() {
  try {
    const serialized = localStorage.getItem(STORAGE_KEY_PREFS);
    if (!serialized) return null;
    return JSON.parse(serialized);
  } catch (e) {
    console.error('Failed to load preferences:', e);
    return null;
  }
}
