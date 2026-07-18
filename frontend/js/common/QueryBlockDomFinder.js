export function findParentAliasEl(queryBlock) {
  const parentGroupEl = document.querySelector(
    `.depth-group[data-depth="${queryBlock.depth - 1}"]`,
  );
  if (!parentGroupEl) return null;
  return [...parentGroupEl.querySelectorAll('.table-item')].find(
    (item) => item.dataset.alias === queryBlock.parent_alias,
  );
}
