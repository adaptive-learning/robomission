import {
  FETCH_WORLD_SUCCESS,
  FETCH_STUDENT_SUCCESS,
  SEE_INSTRUCTION_REQUEST,
  SHOW_INSTRUCTIONS,
  } from '../action-types';


const initial = {
  byId: {},
  all: [],
  seen: null,  // to distinguish between initial state and no-instruction-seen
  shown: false,
};


export default function reduceInstructions(state = initial, action) {
  switch (action.type) {
    case FETCH_WORLD_SUCCESS: {
      const instructionList = action.payload.instructions.map(parseInstruction);
      const state = {
        ...state,
        byId: createEntityMap(instructionList),
        all: instructionList.map(instruction => instruction.id),
      };
      if (state.seen === null) {
        // To avoid flickering instruction button.
        state.seen = state.all;
      }
      return state;
    }
    case FETCH_STUDENT_SUCCESS: {
      return {
        ...state,
        seen: action.payload.seenInstructions,
      }
    }
    case SEE_INSTRUCTION_REQUEST: {
      if (state.seen.includes(action.payload.instructionId)) {
        return state;
      }
      return {
        ...state,
        seen: [...state.seen, action.payload.instructionId],
      };
    }
    case SHOW_INSTRUCTIONS: {
      if (state.shown || state.all.length === 0) {
        return state;
      }
      return {
        ...state,
        shown: true,
      };
    }
    default: {
      return state;
    }
  }
}


const viewData = {
  'env-recommended-task-button': {
    position: 'top',
  },
  'env-menu': {
    position: 'right',
  },
  'task-space-world': {
    position: 'bottom',
  },
  'task-toolbox': {
    position: 'right',
  },
  'task-snapping': {
    position: 'bottom-left',
  },
  'task-controls': {
    position: 'bottom-left',
  },
  'object-wormhole': {
    position: 'bottom-left',
  },
  'object-diamond': {
    position: 'bottom-left',
  },
  'object-asteroid': {
    position: 'bottom-left',
  },
  'object-meteoroid': {
    position: 'bottom-left',
  },
  'diamonds-status': {
    position: 'bottom-left',
  },
  'energy-status': {
    position: 'bottom-left',
  },
  'length-limit': {
    position: 'bottom-left',
  },
  'block-fly': {
    position: 'bottom-left',
  },
  'block-shoot': {
    position: 'bottom-left',
  },
  'block-repeat': {
    position: 'bottom-left',
  },
  'block-while': {
    position: 'bottom-left',
  },
  'block-color': {
    position: 'bottom-left',
  },
  'block-position': {
    position: 'bottom-left',
  },
  'block-if': {
    position: 'bottom-left',
  },
  'block-if-else': {
    position: 'bottom-left',
  },
  'env-task-editor': {
    position: 'left',
  },
};


function parseInstruction(data) {
  const instructionId = data['name'];
  if (viewData[instructionId] === undefined) {
    console.warn(`Missing view data for instruction '${instructionId}'`);
  }
  const selectorClass = `instructionable-${instructionId}`;
  const instruction = {
    ...viewData[instructionId],
    id: instructionId,
    // save both class and selector
    selectorClass: selectorClass,
    selector: `.${selectorClass}`,
  };

  return instruction;
}


// TODO: factor out to some common utils (core.entities?)
function createEntityMap(list) {
  const map = {};
  for (const entity of list) {
    map[entity.id] = entity;
  }
  return map;
}
