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
  const instructions = all.map(id => byId[id]);
  return instructions.filter(isRelevant);
}


export function getNewInstructions(state) {
  // TODO: Simplify.
  const { all, seen, byId } = state.instructions;
  const unseen = all.filter(id => !seen.includes(id));
  const instructions = unseen.map(id => byId[id]);
  return instructions.filter(isRelevant);
}


export function getNNewInstructions(state) {
  return getNewInstructions(state).length;
}


function isRelevant(instruction) {
  // Try to find a corresponding element; if not found declare as non-relevant.
  // TODO: Unhack (make it more explicit, fast, reliable).
  return document.getElementsByClassName(instruction.selectorClass).length > 0;
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
