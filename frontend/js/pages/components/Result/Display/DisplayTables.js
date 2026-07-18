import { highlightQuery } from './DisplayQuery.js';

export function displayTables(queryBlocks) {
  if (!queryBlocks.length) return;

  const tablesEl = document.querySelector('.tables-list');
  tablesEl.innerHTML = '';
  tablesEl.style.display = 'flex';
  tablesEl.style.alignItems = 'flex-start';
  tablesEl.style.position = 'relative';

  let currentDepth = queryBlocks[0].depth;
  let depthGroupEl = createDepthGroup(currentDepth);
  tablesEl.appendChild(depthGroupEl);

  queryBlocks.forEach((queryBlock) => {
    if (queryBlock.depth !== currentDepth) {
      currentDepth = queryBlock.depth;
      depthGroupEl = createDepthGroup(currentDepth);
      tablesEl.appendChild(depthGroupEl);
    }

    const queryBlockGroupEl = document.createElement('div');
    queryBlockGroupEl.className = 'query-block-group';
    queryBlockGroupEl.dataset.startIndex = queryBlock.start_index;

    queryBlock.tables_name_alias.forEach((table) => {
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
        highlightQuery(queryBlock.start_index, queryBlock.end_index);
      };
      tableEl.addEventListener('click', activate);
      tableEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          activate(e);
        }
      });
      queryBlockGroupEl.appendChild(tableEl);
    });

    depthGroupEl.appendChild(queryBlockGroupEl);
  });
}

function createDepthGroup(depth) {
  const el = document.createElement('div');
  el.className = 'depth-group';
  el.dataset.depth = depth;
  return el;
}
