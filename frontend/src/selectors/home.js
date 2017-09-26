import { isSolved } from '../selectors/gameState';

const spaceWorldDemoEnvironmentId = 'home-commands';
const programDemoEnvironmentId = 'home-program';

export function isSpaceWorldDemoSolved(state) {
  return isSolved(state, spaceWorldDemoEnvironmentId);
}


export function isProgramDemoSolved(state) {
  return isSolved(state, programDemoEnvironmentId);
}
