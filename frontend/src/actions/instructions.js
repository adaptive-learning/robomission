import { SHOW_INSTRUCTIONS } from '../action-types';
import { seeInstruction as reportSeenInstruction } from '../actions/api';

export function showInstructions() {
  return {
    type: SHOW_INSTRUCTIONS,
    payload: {},
  };
}

export function seeInstruction(instructionId) {
  return reportSeenInstruction(instructionId);
}
