// frontend/assets/js/sidebar.js
// Injects sidebar HTML and sets active nav item

function renderSidebar(activePage) {
  const user = getUser();
  const initial = user ? user.username[0].toUpperCase() : 'A';
  const username = user ? user.username : 'admin';

  const navItems = [
    { page: 'dashboard',    icon: '◈', label: 'Dashboard',    href: 'dashboard.html' },
    { page: 'products',     icon: '⬡', label: 'Products',     href: 'products.html' },
    { page: 'transactions', icon: '⇌', label: 'Transactions', href: 'transactions.html' },
    { page: 'reports',      icon: '⌗', label: 'Reports',      href: 'reports.html' },
  ];

  const navHTML = navItems.map(n => `
    <a href="${n.href}" class="nav-item ${activePage === n.page ? 'active' : ''}">
      <span class="icon">${n.icon}</span> ${n.label}
    </a>
  `).join('');

  return `
    <aside class="sidebar">
      <div class="sidebar-brand">Inven<span>AI</span></div>
      <nav class="sidebar-nav">${navHTML}</nav>
      <div class="sidebar-footer">
        <div class="sidebar-user">
          <div class="avatar">${initial}</div>
          <span>${username}</span>
        </div>
        <button onclick="logout()" class="btn-outline w-full" style="font-size:0.8rem;">
          ⏻ Logout
        </button>
      </div>
    </aside>
  `;
}

function initPage(activePage) {
  requireLogin();
  const app = document.getElementById('app');
  if (app) {
    app.insertAdjacentHTML('afterbegin', renderSidebar(activePage));
  }
}
