import { LOCATION_CHANGE } from 'react-router-redux';
import {
  FETCH_STATIC_DATA_FULFILLED,
  UPDATE_STUDENT_FULFILLED,
  SET_TASK,
  SEE_INSTRUCTION_PENDING,
  SHOW_INSTRUCTIONS,
  } from '../action-types';
import { practicePageTaskEnvironmentId } from '../selectors/taskEnvironment';


const initial = {
  byId: {},
  all: [],
  seen: [],
  scheduled: [],
  activeIndex: null,
};


export default function reduceInstructions(state = initial, action) {
  switch (action.type) {
    case FETCH_STATIC_DATA_FULFILLED: {
      const instructionList = action.payload.instructions.map(parseInstruction);
      return {
        ...state,
        byId: createEntityMap(instructionList),
        all: instructionList.map(instruction => instruction.id),
      };
    }
    case UPDATE_STUDENT_FULFILLED: {
      return {
        ...state,
        seen: action.payload.seenInstructions,
      };
    }
    case SET_TASK: {
      if (action.payload.taskEnvironmentId !== practicePageTaskEnvironmentId) {
        return state;
      }
      const scheduled = getRelevantUnseenInstructions(action.payload.task, state.seen);
      return {
        ...state,
        scheduled,
        activeIndex: (scheduled.length > 0) ? 0 : null,
      };
    }
    case LOCATION_CHANGE: {
      if (action.payload.pathname === '/task-editor') {
        const scheduled = state.seen.includes('env.task-editor') ? [] : ['env.task-editor'];
        return {
          ...state,
          scheduled,
          activeIndex: (scheduled.length > 0) ? 0 : null,
        };
      }
      return state;
    }
    case SEE_INSTRUCTION_PENDING: {
      if (action.payload.instructionId !== state.scheduled[state.activeIndex]) {
        return state;
      }
      let nextIndex = state.activeIndex + 1;
      if (nextIndex >= state.scheduled.length) {
        nextIndex = null;
      }
      return {
        ...state,
        activeIndex: nextIndex,
        seen: [...state.seen, action.payload.instructionId],
      };
    }
    case SHOW_INSTRUCTIONS: {
      if (state.activeIndex !== null) {
        return state;
      }
      if (state.scheduled.length === 0) {
        return state;
      }
      return {
        ...state,
        activeIndex: 0,
      };
    }
  }
  return state;
}


const viewData = {
  'env.space-world': {
    selector: '.instructionable-env-space-world',
    position: 'bottom',
  },
  'env.toolbox': {
    selector: '.blocklyFlyout',
    position: 'right',
  },
  'env.snapping': {
    selector: '.instructionable-env-snapping',
    position: 'bottom-left',
  },
  'env.controls': {
    selector: '.instructionable-env-controls',
    position: 'bottom-left',
  },
  'object.wormhole': {
    selector: '.instructionable-object-wormhole',
    position: 'bottom-left',
  },
  'object.diamond': {
    selector: '.instructionable-object-diamond',
    position: 'bottom-left',
  },
  'object.asteroid': {
    selector: '.instructionable-object-asteroid',
    position: 'bottom-left',
  },
  'object.meteoroid': {
    selector: '.instructionable-object-meteoroid',
    position: 'bottom-left',
  },
  'diamonds-status': {
    selector: '.instructionable-diamonds-status',
    position: 'bottom-left',
  },
  'energy-status': {
    selector: '.instructionable-energy-status',
    position: 'bottom-left',
  },
  'length-limit': {
    selector: '.instructionable-length-limit',
    position: 'bottom-left',
  },
  'block.fly': {
    selector: '.instructionable-block-fly',
    position: 'bottom-left',
  },
  'block.shoot': {
    selector: '.instructionable-block-shoot',
    position: 'bottom-left',
  },
  'block.repeat': {
    selector: '.instructionable-block-repeat',
    position: 'bottom-left',
  },
  'block.while': {
    selector: '.instructionable-block-while',
    position: 'bottom-left',
  },
  'block.color': {
    selector: '.instructionable-block-color',
    position: 'bottom-left',
  },
  'block.position': {
    selector: '.instructionable-block-position',
    position: 'bottom-left',
  },
  'block.if': {
    selector: '.instructionable-block-if',
    position: 'bottom-left',
  },
  'block.if-else': {
    selector: '.instructionable-block-if-else',
    position: 'bottom-left',
  },
  'env.task-editor': {
    selector: '.instructionable-env-task-editor',
    position: 'left',
  },
};


function parseInstruction(data) {
  const instructionId = data['instruction_id'];
  if (viewData[instructionId] === undefined) {
    console.warn(`Missing view data for instruction '${instructionId}'`);
  }
  const instruction = {
    ...viewData[instructionId],
    id: instructionId,
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


const ordering = [
  'env.space-world',
  'env.toolbox',
  'env.snapping',
  'env.controls',
  'object.asteroid',
  'object.meteoroid',
  'object.diamond',
  'object.wormhole',
  'diamonds-status',
  'energy-status',
  'length-limit',
  'block.fly',
  'block.shoot',
  'block.repeat',
  'block.while',
  'block.color',
  'block.position',
  'block.if',
  'block.if-else',
];


function getRelevantUnseenInstructions(task, seen) {
  // return ['env.snapping', 'length-limit'];
  const instructions = getRelevantInstructions(task);
  const unseen = instructions.filter(instruction => seen.indexOf(instruction) < 0);
  return unseen;
}


function getRelevantInstructions(task) {
  return ordering.filter(instruction => containsInstruction(task, task.toolbox, instruction));
}


function containsInstruction(task, toolbox, instruction) {
  switch (instruction) {
    case 'env.space-world':
    case 'env.toolbox':
    case 'env.snapping':
    case 'env.controls':
      return true;
    case 'object.asteroid':
      return containsObject(task, 'A');
    case 'object.meteoroid':
      return containsObject(task, 'M');
    case 'object.wormhole':
      return containsObject(task, 'W');
    case 'object.diamond':
    case 'diamonds-status':
      return containsObject(task, 'D');
    case 'energy-status':
      return task.setting.energy != null;
    case 'length-limit':
      return task.setting.length != null;
    case 'block.fly':
    case 'block.shoot':
    case 'block.repeat':
    case 'block.while':
    case 'block.color':
    case 'block.position':
    case 'block.if':
    case 'block.if-else':
      return toolbox.blocks.indexOf(instruction.slice(6)) >= 0;
    default:
      throw new Error(`Missing containsInstruction definition for ${instruction}`);
  }
}


function containsObject(task, objectLabel) {
  const allLabels = task.setting.fields.map(
    row => row.map(field => field[0] + field[1].join('')).join('')).join('');
  return allLabels.indexOf(objectLabel) >= 0;
}
