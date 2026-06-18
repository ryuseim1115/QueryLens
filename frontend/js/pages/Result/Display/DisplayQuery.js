let _originalQuery = '';

export function displayQuery(query) {
  _originalQuery = query;
  const queryDisplayEl = document.querySelector('.query-display');
  queryDisplayEl.textContent = query;
}

function escapeHtml(text) {
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

export function highlightQuery(start_index, end_index) {
  const queryDisplayEl = document.querySelector('.query-display');
  const before = escapeHtml(_originalQuery.slice(0, start_index));
  const highlighted = escapeHtml(_originalQuery.slice(start_index, end_index));
  const after = escapeHtml(_originalQuery.slice(end_index));
  queryDisplayEl.innerHTML = `${before}<mark>${highlighted}</mark>${after}`;
}
