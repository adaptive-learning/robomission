//import { getMode } from '../selectors/app';
//import { getPracticePageTask } from '../selectors/taskEnvironment';
import { getNewRelevantInstructions } from '../reducers/instructions';

export function getScheduledInstructions(state) {
  if (!state.instructions.shown) {
    return [];
  }
  const { byId, scheduled } = state.instructions;
  return scheduled.map(id => byId[id]);
}


export function getNNewInstructions(state) {
  return getNewRelevantInstructions(state.instructions).length;
}
