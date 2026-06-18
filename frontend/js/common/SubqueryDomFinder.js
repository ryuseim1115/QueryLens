export function findParentAliasEl(subquery) {
  const parentGroupEl = document.querySelector(
    `.depth-group[data-depth="${subquery.depth - 1}"]`,
  );
  if (!parentGroupEl) return null;
  return [...parentGroupEl.querySelectorAll('.table-item')].find(
    (item) => item.dataset.alias === subquery.parent_alias,
  );
}
