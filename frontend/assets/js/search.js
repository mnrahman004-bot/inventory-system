// frontend/assets/js/search.js
// Real-time search and category filter for product/transaction tables

/**
 * Filters table rows by a search query and optional category.
 * @param {string} tableId   - The <tbody> element ID to filter
 * @param {string} query     - Search text
 * @param {string} category  - Category filter ('all' = no filter)
 * @param {number[]} cols    - Column indices to search within
 * @param {number} catCol    - Column index that holds the category
 */
function filterTable(tableId, query, category = 'all', cols = [1, 2], catCol = 2) {
  const tbody = document.getElementById(tableId);
  if (!tbody) return;

  const rows = tbody.querySelectorAll('tr');
  const q = query.toLowerCase().trim();

  rows.forEach(row => {
    const cells = row.querySelectorAll('td');
    if (!cells.length) return;

    // Text match: check specified columns
    const textMatch = cols.some(i => {
      const cell = cells[i];
      return cell && cell.textContent.toLowerCase().includes(q);
    });

    // Category match
    const catCell = cells[catCol];
    const catMatch = category === 'all' || !catCell ||
      catCell.textContent.trim().toLowerCase() === category.toLowerCase();

    row.style.display = textMatch && catMatch ? '' : 'none';
  });
}

/**
 * Populates a category <select> dropdown from table data.
 * @param {string} tableId   - tbody ID to read categories from
 * @param {string} selectId  - select element ID to populate
 * @param {number} catCol    - column index containing category
 */
function populateCategoryFilter(tableId, selectId, catCol = 2) {
  const tbody = document.getElementById(tableId);
  const select = document.getElementById(selectId);
  if (!tbody || !select) return;

  const categories = new Set();
  tbody.querySelectorAll('tr').forEach(row => {
    const cell = row.querySelectorAll('td')[catCol];
    if (cell) categories.add(cell.textContent.trim());
  });

  // Remove old dynamic options (keep "All Categories")
  select.querySelectorAll('option:not([value="all"])').forEach(o => o.remove());

  categories.forEach(cat => {
    const opt = document.createElement('option');
    opt.value = cat;
    opt.textContent = cat;
    select.appendChild(opt);
  });
}

/**
 * Wire up search input + category filter for a table.
 */
function initTableSearch({ inputId, selectId, tableId, cols, catCol }) {
  const input = document.getElementById(inputId);
  const select = document.getElementById(selectId);

  const doFilter = () => {
    const q = input ? input.value : '';
    const cat = select ? select.value : 'all';
    filterTable(tableId, q, cat, cols, catCol);
  };

  if (input) input.addEventListener('input', doFilter);
  if (select) select.addEventListener('change', doFilter);
}
