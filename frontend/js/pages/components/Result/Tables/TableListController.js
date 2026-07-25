import { createDepthGroup } from './createDepthGroup.js';
import { createQueryBlockGroup } from './createQueryBlockGroup.js';
import { createResultItem } from './createResultItem.js';

export function displayTables(queryBlocks) {
  if (!queryBlocks.length) return;

  const tablesEl = document.querySelector('.tables-list');
  tablesEl.innerHTML = '';
  tablesEl.style.display = 'flex';
  tablesEl.style.alignItems = 'flex-start';
  tablesEl.style.position = 'relative';

  // queryBlocksはdepthの降順（ネストが深い順）で渡されるため、先頭要素のdepthが最大値になる
  let currentDepth = queryBlocks[0].depth;
  let depthGroupEl = createDepthGroup(currentDepth);
  tablesEl.appendChild(depthGroupEl);

  queryBlocks.forEach((queryBlock) => {
    // 同じdepthのブロックはqueryBlocks内で連続しているため、depthの変化を検知する
    if (queryBlock.depth !== currentDepth) {
      currentDepth = queryBlock.depth;
      depthGroupEl = createDepthGroup(currentDepth);
      tablesEl.appendChild(depthGroupEl);
    }

    depthGroupEl.appendChild(createQueryBlockGroup(queryBlock));
  });

  // queryBlocksは深さの降順なので、末尾要素が必ずdepth0（クエリ全体）になる
  const rootQueryBlock = queryBlocks[queryBlocks.length - 1];
  const resultDepthGroupEl = createDepthGroup(currentDepth - 1);
  const resultGroupEl = document.createElement('div');
  resultGroupEl.className = 'query-block-group';
  resultGroupEl.appendChild(createResultItem(rootQueryBlock));
  resultDepthGroupEl.appendChild(resultGroupEl);
  tablesEl.appendChild(resultDepthGroupEl);
}
