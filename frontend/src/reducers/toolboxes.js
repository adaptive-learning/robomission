import { FETCH_STATIC_DATA_FULFILLED } from '../action-types';

export default function reduceToolboxes(state = {}, action) {
  switch (action.type) {
    case FETCH_STATIC_DATA_FULFILLED: {
      const toolboxList = action.payload.toolboxes.map(parseToolbox);
      const toolboxes = {};
      for (const toolbox of toolboxList) {
        toolboxes[toolbox.id] = toolbox;
      }
      return toolboxes;
    }
  }
  return state;
}

function parseToolbox(data) {
  const toolbox = {
    id: data['toolbox_id'],
    blocks: data['blocks'],
  };
  return toolbox;
}
