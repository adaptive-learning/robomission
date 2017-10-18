import { FETCH_STATIC_DATA_FULFILLED } from '../action-types';

export default function reduceCategories(state = {}, action) {
  switch (action.type) {
    case FETCH_STATIC_DATA_FULFILLED: {
      // TODO: Remove notion of categories and use rich levels instead.
      const categoryList = action.payload.levels.map(parseCategory);
      const categories = {};
      for (const category of categoryList) {
        categories[category.id] = category;
      }
      return categories;
    }
  }
  return state;
}

function parseCategory(data) {
  const category = {
    id: data['name'],
    level: data['level'],
    toolbox: data['toolbox'],
    tasks: data['tasks'],
  };
  return category;
}
