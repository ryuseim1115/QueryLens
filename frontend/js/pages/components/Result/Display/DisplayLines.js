import { findParentAliasEl } from '../../../../common/QueryBlockDomFinder.js';

export function displayLines(queryBlocks) {
  const tablesEl = document.querySelector('.tables-list');
  const tablesRect = tablesEl.getBoundingClientRect();

  const canvas = document.createElement('canvas');
  canvas.style.position = 'absolute';
  canvas.style.top = '0px';
  canvas.style.left = '0px';
  canvas.style.pointerEvents = 'none';
  canvas.width = tablesEl.offsetWidth;
  canvas.height = tablesEl.offsetHeight;
  tablesEl.appendChild(canvas);

  const ctx = canvas.getContext('2d');
  ctx.strokeStyle = '#60a5fa';

  for (const queryBlock of queryBlocks) {
    if (!queryBlock.parent_alias) continue;

    const parentEl = findParentAliasEl(queryBlock);
    if (!parentEl) continue;
    const parentRect = parentEl.getBoundingClientRect();
    const toX = parentRect.x - tablesRect.x;
    const toY = parentRect.y + parentRect.height / 2 - tablesRect.y;

    const queryBlockGroupEl = document.querySelector(
      `.query-block-group[data-start-index="${queryBlock.start_index}"]`,
    );
    for (const table of queryBlockGroupEl.querySelectorAll('.table-item')) {
      const rect = table.getBoundingClientRect();
      const fromX = rect.x + rect.width - tablesRect.x;
      const fromY = rect.y + rect.height / 2 - tablesRect.y;

      ctx.beginPath();
      ctx.moveTo(fromX, fromY);
      ctx.lineTo(toX, toY);
      ctx.stroke();
    }
  }
}
