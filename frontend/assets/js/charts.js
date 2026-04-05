// frontend/assets/js/charts.js
// Chart.js wrappers for dashboard visualizations

let stockTrendChart = null;
let salesPurchasesChart = null;
let categoryChart = null;

/**
 * Renders a line chart showing stock levels over time.
 */
function renderStockTrendChart(canvasId, labels, data) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  if (stockTrendChart) stockTrendChart.destroy();

  stockTrendChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Stock Quantity',
        data,
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99,102,241,0.12)',
        borderWidth: 2.5,
        pointRadius: 4,
        pointBackgroundColor: '#6366f1',
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: { mode: 'index', intersect: false }
      },
      scales: {
        x: { grid: { display: false } },
        y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } }
      }
    }
  });
}

/**
 * Renders a grouped bar chart for Sales (OUT) vs Purchases (IN).
 */
function renderSalesPurchasesChart(canvasId, chartData) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  if (salesPurchasesChart) salesPurchasesChart.destroy();

  // Build label/value arrays from raw API data
  const dayMap = {};
  chartData.forEach(row => {
    if (!dayMap[row.day]) dayMap[row.day] = { IN: 0, OUT: 0 };
    dayMap[row.day][row.type] = row.total;
  });

  const labels = Object.keys(dayMap).sort().slice(-14); // last 14 days
  const inData  = labels.map(d => dayMap[d]?.IN  || 0);
  const outData = labels.map(d => dayMap[d]?.OUT || 0);

  salesPurchasesChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Purchases (IN)',
          data: inData,
          backgroundColor: 'rgba(16,185,129,0.75)',
          borderRadius: 5,
        },
        {
          label: 'Sales (OUT)',
          data: outData,
          backgroundColor: 'rgba(239,68,68,0.75)',
          borderRadius: 5,
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        tooltip: { mode: 'index' }
      },
      scales: {
        x: { grid: { display: false } },
        y: { beginAtZero: true }
      }
    }
  });
}

/**
 * Renders a doughnut chart showing category distribution.
 */
function renderCategoryChart(canvasId, categories) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  if (categoryChart) categoryChart.destroy();

  const labels = categories.map(c => c.category);
  const data   = categories.map(c => c.total_qty || c.count);

  const palette = [
    '#6366f1', '#10b981', '#f59e0b', '#ef4444',
    '#3b82f6', '#8b5cf6', '#ec4899', '#14b8a6'
  ];

  categoryChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data,
        backgroundColor: palette.slice(0, labels.length),
        borderWidth: 2,
        borderColor: '#1e2030'
      }]
    },
    options: {
      responsive: true,
      cutout: '65%',
      plugins: {
        legend: { position: 'bottom' },
        tooltip: {
          callbacks: {
            label: ctx => ` ${ctx.label}: ${ctx.parsed} units`
          }
        }
      }
    }
  });
}
