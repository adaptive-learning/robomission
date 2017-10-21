import { FETCH_WORLD_SUCCESS } from '../action-types';

export default function reduceToolboxes(state = {}, action) {
  switch (action.type) {
    case FETCH_WORLD_SUCCESS: {
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
    id: data['name'],
    blocks: data['blocks'],
  };
  return toolbox;
}
