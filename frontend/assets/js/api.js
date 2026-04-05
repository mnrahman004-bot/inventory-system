// frontend/assets/js/api.js
// Central API handler - all fetch() calls go through here

/**
 * Generic API request helper.
 * Automatically attaches the Authorization Bearer token.
 */
async function apiRequest(endpoint, method = 'GET', body = null) {
  const token = getToken();
  const headers = { 'Content-Type': 'application/json' };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const options = { method, headers };
  if (body && method !== 'GET') {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(`${CONFIG.API_BASE}${endpoint}`, options);

    // Handle 401 - redirect to login
    if (response.status === 401) {
      clearAuth();
      window.location.href = '../pages/login.html';
      return null;
    }

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || `HTTP ${response.status}`);
    }
    return data;
  } catch (err) {
    console.error(`[API] ${method} ${endpoint} failed:`, err.message);
    throw err;
  }
}

// ── Auth ──────────────────────────────────────────
async function apiLogin(username, password) {
  const res = await fetch(`${CONFIG.API_BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Login failed');
  return data;
}

// ── Products ─────────────────────────────────────
const ProductAPI = {
  getAll:  ()           => apiRequest('/products'),
  getOne:  (id)         => apiRequest(`/products/${id}`),
  create:  (data)       => apiRequest('/products', 'POST', data),
  update:  (id, data)   => apiRequest(`/products/${id}`, 'PUT', data),
  delete:  (id)         => apiRequest(`/products/${id}`, 'DELETE'),
};

// ── Transactions ──────────────────────────────────
const TransactionAPI = {
  getAll:  ()     => apiRequest('/transactions'),
  create:  (data) => apiRequest('/transactions', 'POST', data),
  chart:   ()     => apiRequest('/transactions/chart'),
};

// ── Dashboard ─────────────────────────────────────
const DashboardAPI = {
  getStats: () => apiRequest('/reports/dashboard'),
};

// ── Reports ───────────────────────────────────────
const ReportAPI = {
  exportCSV: async (type = 'products') => {
    const token = getToken();
    const url = `${CONFIG.API_BASE}/reports/export?type=${type}`;
    const response = await fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Export failed');
    const blob = await response.blob();
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${type}_report.csv`;
    link.click();
  }
};

// ── AI Prediction ─────────────────────────────────
const PredictionAPI = {
  predict: (productId, days = 30) => apiRequest(`/predict/${productId}?days=${days}`),
};
