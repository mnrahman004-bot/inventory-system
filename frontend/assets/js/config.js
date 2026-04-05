// frontend/assets/js/config.js
// Central configuration for the frontend

const CONFIG = {
  // Change this to your deployed backend URL on Render
  API_BASE: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'
    : 'https://your-app.onrender.com/api',  // ← update before deploying

  TOKEN_KEY: 'inv_token',
  USER_KEY:  'inv_user',
};

// Token helpers
function getToken() {
  return localStorage.getItem(CONFIG.TOKEN_KEY);
}

function setToken(token) {
  localStorage.setItem(CONFIG.TOKEN_KEY, token);
}

function getUser() {
  try {
    return JSON.parse(localStorage.getItem(CONFIG.USER_KEY) || 'null');
  } catch { return null; }
}

function setUser(user) {
  localStorage.setItem(CONFIG.USER_KEY, JSON.stringify(user));
}

function clearAuth() {
  localStorage.removeItem(CONFIG.TOKEN_KEY);
  localStorage.removeItem(CONFIG.USER_KEY);
}

function isLoggedIn() {
  return !!getToken();
}

function requireLogin() {
  if (!isLoggedIn()) {
    window.location.href = '../pages/login.html';
  }
}

function logout() {
  clearAuth();
  window.location.href = '../pages/login.html';
}
