import { FETCH_STATIC_DATA_FULFILLED } from '../action-types';

export default function reduceCategories(state = {}, action) {
  switch (action.type) {
    case FETCH_STATIC_DATA_FULFILLED: {
      const categoryList = action.payload.categories.map(parseCategory);
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
    id: data['category_id'],
    level: data['level'],
    toolbox: data['toolbox'],
    tasks: data['tasks'],
  };
  return category;
}
