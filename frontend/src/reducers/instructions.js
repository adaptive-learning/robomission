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
      const nextState = {
        ...state,
        byId: createEntityMap(instructionList),
        all: instructionList.map(instruction => instruction.id),
      };
      if (state.seen === null) {
        // To avoid flickering instruction button.
        nextState.seen = state.all;
      }
      return nextState;
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
      return {
        ...state,
        shown: action.payload.show && state.all.length > 0,
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
  'env-levelbar': {
    position: 'bottom',
  },
  'env-help': {
    position: 'bottom',
  },
  'env-feedback': {
    position: 'bottom',
  },
  'env-login': {
    position: 'bottom',
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
  'task-wormhole': {
    position: 'bottom-left',
  },
  'task-diamond': {
    position: 'bottom-left',
  },
  'task-asteroid': {
    position: 'bottom-left',
  },
  'task-meteoroid': {
    position: 'bottom-left',
  },
  'task-diamond-status': {
    position: 'bottom-left',
  },
  'task-energy-status': {
    position: 'bottom-left',
  },
  'task-length-limit': {
    position: 'bottom-left',
  },
  'task-block-fly': {
    position: 'bottom-left',
  },
  'task-block-shoot': {
    position: 'bottom-left',
  },
  'task-block-repeat': {
    position: 'bottom-left',
  },
  'task-block-while': {
    position: 'bottom-left',
  },
  'task-block-color': {
    position: 'bottom-left',
  },
  'task-block-position': {
    position: 'bottom-left',
  },
  'task-block-if': {
    position: 'bottom-left',
  },
  'task-block-if-else': {
    position: 'bottom-left',
  },

  'editor-setting': {
    position: 'left',
  },
  'editor-space-world': {
    position: 'left',
  },

  'overview-levels': {
    position: 'bottom',
  },
  'overview-recommended-task': {
    position: 'bottom',
  },
  'overview-solved-task': {
    position: 'bottom',
  },
  'overview-difficulty': {
    position: 'bottom',
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
