//import { getMode } from '../selectors/app';
//import { getPracticePageTask } from '../selectors/taskEnvironment';

export function getScheduledInstructions(state) {
  if (!state.instructions.shown) {
    return [];
  }
  const newInstructions = getNewInstructions(state);
  if (newInstructions.length > 0) {
    return newInstructions;
  }
  return getAllInstructions(state);
}


export function getAllInstructions(state) {
  const { byId, all } = state.instructions;
  const relevant = filterRelevant(state, all);
  console.log('all', relevant);
  const instructions = relevant.map(id => byId[id]);
  return instructions;
}


export function getNewInstructions(state) {
  const { all, byId } = state.instructions;
  const unseenRelevant = filterRelevant(state, filterUnseen(state, all));
  console.log('new', unseenRelevant);
  const instructions = unseenRelevant.map(id => byId[id]);
  return instructions;
}


export function getNNewInstructions(state) {
  return getNewInstructions(state).length;
}


function filterUnseen(state, instructions) {
  const { seen } = state.instructions;
  const unseen = instructions.filter(id => !seen.includes(id));
  return unseen;
}


function filterRelevant(state, instructions) {
  const withInstructables = Object.keys(state.instructions.instructables);
  console.log('filterRelevant', instructions, 'withInstructables', withInstructables);
  const relevant = instructions.filter(id => withInstructables.includes(id));
  return relevant;
}


//function containsInstruction(task, instruction) {
//  switch (instruction) {
//    case 'env.space-world':
//    case 'env.toolbox':
//    case 'env.snapping':
//    case 'env.controls':
//      return true;
//    case 'object.asteroid':
//      return containsObject(task, 'A');
//    case 'object.meteoroid':
//      return containsObject(task, 'M');
//    case 'object.wormhole':
//      return containsObject(task, 'W');
//    case 'object.diamond':
//    case 'diamonds-status':
//      return containsObject(task, 'D');
//    case 'energy-status':
//      return task.setting.energy != null;
//    case 'length-limit':
//      return task.setting.length != null;
//    case 'block.fly':
//    case 'block.shoot':
//    case 'block.repeat':
//    case 'block.while':
//    case 'block.color':
//    case 'block.position':
//    case 'block.if':
//    case 'block.if-else':
//      return task.toolbox.blocks.indexOf(instruction.slice(6)) >= 0;
//    default:
//      throw new Error(`Missing containsInstruction definition for ${instruction}`);
//  }
//}
//
//
//function containsObject(task, objectLabel) {
//  return fields.indexOf(objectLabel) >= 0;
//}
