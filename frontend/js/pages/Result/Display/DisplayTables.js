import { highlightQuery } from './DisplayQuery.js';

export function displayTables(subqueries) {
  if (!subqueries.length) return;

  const tablesEl = document.querySelector('.tables-list');
  tablesEl.innerHTML = '';
  tablesEl.style.display = 'flex';
  tablesEl.style.alignItems = 'flex-start';
  tablesEl.style.position = 'relative';

  let currentDepth = subqueries[0].depth;
  let depthGroupEl = createDepthGroup(currentDepth);
  tablesEl.appendChild(depthGroupEl);

  subqueries.forEach((subquery) => {
    if (subquery.depth !== currentDepth) {
      currentDepth = subquery.depth;
      depthGroupEl = createDepthGroup(currentDepth);
      tablesEl.appendChild(depthGroupEl);
    }

    const subqueryGroupEl = document.createElement('div');
    subqueryGroupEl.className = 'subquery-group';
    subqueryGroupEl.dataset.startIndex = subquery.start_index;

    subquery.tables_name_alias.forEach((table) => {
      const tableEl = document.createElement('div');
      tableEl.className = 'table-item';
      tableEl.setAttribute('role', 'button');
      tableEl.setAttribute('tabindex', '0');
      tableEl.textContent =
        table.name && table.alias
          ? `${table.name} (${table.alias})`
          : table.name || table.alias;
      tableEl.dataset.alias = table.alias || '';
      const activate = (e) => {
        e.stopPropagation();
        highlightQuery(subquery.start_index, subquery.end_index);
      };
      tableEl.addEventListener('click', activate);
      tableEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          activate(e);
        }
      });
      subqueryGroupEl.appendChild(tableEl);
    });

    depthGroupEl.appendChild(subqueryGroupEl);
  });
}

function createDepthGroup(depth) {
  const el = document.createElement('div');
  el.className = 'depth-group';
  el.dataset.depth = depth;
  return el;
}
