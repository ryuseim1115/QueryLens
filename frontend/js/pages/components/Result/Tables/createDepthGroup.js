export function createDepthGroup(depth) {
  const depthGroupEl = document.createElement('div');
  depthGroupEl.className = 'depth-group';
  depthGroupEl.dataset.depth = depth;
  return depthGroupEl;
}
