export function getToolboxId(state, categoryId) {
  return state.categories[categoryId].toolbox;
}


export function getCategoryLevel(state, categoryId) {
  return state.categories[categoryId].level;
}
