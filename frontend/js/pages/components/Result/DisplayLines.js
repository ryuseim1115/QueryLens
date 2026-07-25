import { findParentAliasEl } from '../../../common/QueryBlockDomFinder.js';

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

  const resultEl = document.querySelector('.result-item');

  for (const queryBlock of queryBlocks) {
    // ルートブロック（クエリ全体）自体は下のresultElへの接続でまとめて処理する
    if (queryBlock.depth === 0) continue;

    const targetEl = resolveTargetEl(queryBlock, queryBlocks, resultEl);
    if (!targetEl) continue;

    const queryBlockGroupEl = document.querySelector(
      `.query-block-group[data-start-index="${queryBlock.start_index}"]`,
    );
    drawLinesToTarget(ctx, queryBlockGroupEl, targetEl, tablesRect);
  }

  // queryBlocksは深さの降順なので、末尾要素が必ずdepth0（クエリ全体）になる
  const rootQueryBlock = queryBlocks[queryBlocks.length - 1];
  const rootQueryBlockGroupEl = document.querySelector(
    `.query-block-group[data-start-index="${rootQueryBlock.start_index}"]`,
  );
  drawLinesToTarget(ctx, rootQueryBlockGroupEl, resultEl, tablesRect);
}

// queryBlockの接続先要素を決める。
// エイリアス（CTE名/サブクエリのAS）を持つブロックはそのエイリアスのテーブル項目へ。
// WHERE句のスカラサブクエリのようにエイリアスを持たないブロックは、自身を直接
// 含むブロックを遡り、エイリアスが見つかるかルート（=結果）に辿り着くまで探す
function resolveTargetEl(queryBlock, queryBlocks, resultEl) {
  if (queryBlock.parent_alias) {
    const aliasEl = findParentAliasEl(queryBlock);
    if (aliasEl) return aliasEl;
  }

  const containingBlock = queryBlocks.find(
    (candidate) =>
      candidate.depth === queryBlock.depth - 1 &&
      candidate.start_index <= queryBlock.start_index &&
      candidate.end_index >= queryBlock.end_index,
  );
  if (!containingBlock) return null;
  if (containingBlock.depth === 0) return resultEl;

  return resolveTargetEl(containingBlock, queryBlocks, resultEl);
}

// queryBlockGroupEl内の各テーブル項目からtargetElへ線を引く
function drawLinesToTarget(ctx, queryBlockGroupEl, targetEl, tablesRect) {
  const targetRect = targetEl.getBoundingClientRect();
  const toX = targetRect.x - tablesRect.x;
  const toY = targetRect.y + targetRect.height / 2 - tablesRect.y;

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
