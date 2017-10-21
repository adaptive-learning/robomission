import { getTaskEnvironment, getInitialFieldsFromTaskEnvironment } from './taskEnvironment';

export function getColor(state, taskEnvironmentId) {
  const gameState = getGameState(state, taskEnvironmentId);
  const { fields } = gameState;
  const [y, x] = findSpaceshipPosition(fields);
  const field = fields[y][x];
  const color = field[0];  // TODO: more explicit way to get background
  return color;
}


export function getPosition(state, taskEnvironmentId) {
  const gameState = getGameState(state, taskEnvironmentId);
  const { fields } = gameState;
  const [_y, x] = findSpaceshipPosition(fields);
  const position = x + 1;
  return position;
}


export function isSolved(state, taskEnvironmentId) {
  return getGameStage(state, taskEnvironmentId) === 'solved';
}


export function getFailReason(state, taskEnvironmentId) {
  const { fields, spaceship, diamonds, stage } = getGameState(state, taskEnvironmentId);
  if (stage === 'dead') {
    if (beyondLastRow(fields, spaceship)) {
      return 'crashed-last-row';
    }
    if (beyondEdges(fields, spaceship)) {
      return 'crashed-edge';
    }
    if (onAsteoroid(fields, spaceship)) {
      return 'crashed-asteoroid';
    }
    if (onMeteoroid(fields, spaceship)) {
      return 'crashed-meteoroid';
    }
  }
  if (stage === 'stopped') {
    if (!lastRowReached(spaceship)) {
      return 'last-row-not-reached';
    }
    if (diamonds.taken < diamonds.total) {
      return 'missing-diamonds';
    }
  }
  return null;
}


export function isDead(state, taskEnvironmentId) {
  return getGameStage(state, taskEnvironmentId) === 'dead';
}


export function getGameStage(state, taskEnvironmentId) {
  const gameState = getGameState(state, taskEnvironmentId);
  return gameState.stage;
}


export function getGameState(state, taskEnvironmentId) {
  const taskEnvironment = getTaskEnvironment(state, taskEnvironmentId);
  const gameState = computeGameStateOfTaskEnvironment(taskEnvironment);
  return gameState;
}


// --------------------------------------------------------------------------
// TODO: move the code below to the core (?)

function computeGameStateOfTaskEnvironment(taskEnvironment) {
  const { pastActions, currentAction } = taskEnvironment;
  const initialState = getInitialGameState(taskEnvironment);
  let currentState = doActionMoves(initialState, pastActions);
  if (currentAction !== null) {
    currentState = doAction(currentState, currentAction);
  }
  /*
  const someActionsTaken = taskEnvironment.pastActions.length > 0;
  // TODO: DRY identical someActionsTaken computation at two places (or avoid
  // finalGameStage computation altogether, it feels like a hack...)
  const finalGameStage = decideGameStage(
    currentState.fields,
    currentState.spaceship,
    taskEnvironment.interpreting,
    someActionsTaken);
  return { ...currentState, stage: finalGameStage };
  */
  return currentState;
}


function getInitialGameState(taskEnvironment) {
  const fields = getInitialFieldsFromTaskEnvironment(taskEnvironment);
  const spaceship = findSpaceshipPosition(fields);
  const diamonds = {
    taken: 0,
    total: countDiamonds(fields),
  };
  const energy = {
    current: taskEnvironment.task.setting.energy,
    full: taskEnvironment.task.setting.energy,
  };
  const someActionsTaken = taskEnvironment.pastActions.length > 0;
  const stage = decideGameStage(fields, spaceship, taskEnvironment.interpreting, someActionsTaken);
  return { fields, spaceship, stage, diamonds, energy };
}


function decideGameStage(fields, spaceship, interpreting, someActionsTaken) {
  let stage = 'preparing';
  if (spaceship !== null) {
    // the order of cases is important, e.g. game can only be solved once the
    // program ends
    if (isSpaceshipDead(fields, spaceship)) {
      stage = 'dead';
    } else if (interpreting) {
      stage = 'running';
    } else if (gameSolved(fields, spaceship)) {
      stage = 'solved';
    } else if (someActionsTaken) {
      stage = 'stopped';
    } else {
      stage = 'initial';
    }
  }
  return stage;
}


function doActionMoves(state, actionMoves) {
  return actionMoves.reduce(doActionMove, state);
}


function doActionMove(state, action) {
  const semiState = doAction(state, action);
  const { fields, spaceship, stage, diamonds, energy } = semiState;
  let nextFields = performObjectEvolution(fields);
  if (!isSpaceshipDead(nextFields, spaceship)) {
    nextFields = computeFieldsAfterMove(nextFields, action);
  }
  const nextDiamonds = {
    taken: diamonds.total - countDiamonds(nextFields),
    total: diamonds.total,
  };
  const nextEnergy = {
    current: Math.max(energy.current - energyCost(action), 0),
    full: energy.full,
  };
  const nextSpaceship = findSpaceshipPosition(nextFields);
  const nextStage = decideGameStage(nextFields, nextSpaceship, stage === 'running', true);
  const nextState = {
    fields: nextFields,
    spaceship: nextSpaceship,
    stage: nextStage,
    diamonds: nextDiamonds,
    energy: nextEnergy,
  };
  return nextState;
}


function computeFieldsAfterMove(fields, action) {
  let direction = null;
  switch (action) {
    case 'world-evolution': {
      return fields;
    }
    case 'left': {
      direction = 'left';
      break;
    }
    case 'right': {
      direction = 'right';
      break;
    }
    default: {
      direction = 'ahead';
      break;
    }
  }
  const nextFields = performObjectEvolution(performMove(fields, direction));
  return nextFields;
}


function doAction(state, action) {
  const { fields, energy } = state;
  const spaceship = findSpaceshipPosition(fields);
    // NOTE: sure, given the limited size of the grid, finding position is O(1)
    // operation, but if there is a performance problem, I would recommend to
    // look at this and use a better data structure
  if (isSpaceshipDead(fields, spaceship)) {
    return state;
  }
  if (energy.full !== null && energyCost(action) > energy.current) {
    return state;
  }
  let nextFields = fields;
  switch (action) {
    case 'fly':
    case 'left':
    case 'right': {
      break;
    }
    case 'shoot': {
      nextFields = performShot(fields);
      break;
    }
    case 'world-evolution': {
      nextFields = evolveWorld(fields);
      break;
    }
    default: {
      throw new Error(`Undefined action ${action}`);
    }
  }
  const nextState = {
    ...state,
    fields: nextFields,
    // TODO: energy should be deduced here, not in actionMove
    // TODO: ? recomputing stage ?
  };
  return nextState;
}


function energyCost(action) {
  return (action === 'shoot') ? 1 : 0;
}


function evolveWorld(fields) {
  const spaceshipPosition = findSpaceshipPosition(fields);
  const objects = fields[spaceshipPosition[0]][spaceshipPosition[1]][1];
  let newFields = fields;
  for (const object of objects) {
    if ('WXYZ'.includes(object)) {
      newFields = applyWormholeEffect(fields, spaceshipPosition, object);
    }
  }
  return newFields;
}


function applyWormholeEffect(fields, position, wormholeChar = 'W') {
  const wormholePositions = getPositionsWithObject(fields, wormholeChar);
  const newSpaceshipPosition = selectNewPosition(wormholePositions, position);
  const newFields = fields.map((row, i) => row.map((field, j) => {
    if (i === position[0] && j === position[1]) {
      return [field[0], removeSpaceship(field[1])];
    } else if (i === newSpaceshipPosition[0] && j === newSpaceshipPosition[1]) {
      return [field[0], [...field[1], 'S']];
    }
    return field;
  }));
  return newFields;
}


function selectNewPosition(possiblePositions, currentPosition) {
  const n = possiblePositions.length;
  const i = Math.floor(Math.random() * (n - 1));
  const newPosition = possiblePositions[i];
  if (newPosition[0] === currentPosition[0] && newPosition[1] === currentPosition[1]) {
    return possiblePositions[n - 1];
  }
  return newPosition;
}


function performObjectEvolution(fields) {
  // TODO: factor out 2D map / (world bg+objects map?) into a separate utility function
  const newFields = fields.map((row) => row.map((field) => {
    const [background, objects] = field;
    const explosion = (objects.indexOf('explosion') > -1);
    const removeAllIfExplosion = oldObjects => ((explosion) ? [] : oldObjects);
    const effects = new Set(['laser', 'laser-start', 'laser-end']);
    const removeEffects = oldObjects => oldObjects.filter(obj => !effects.has(obj));
    const evolvedObjects = removeAllIfExplosion(removeEffects(objects));
    const remainingObjects = takeObjectsBySpaceship(evolvedObjects);
    return [background, remainingObjects];
  }));
  return newFields;
}


function takeObjectsBySpaceship(objects) {
  const spaceshipHere = (objects.indexOf('S') > -1);
  if (!spaceshipHere) {
    return objects;
  }
  const remainingObjects = objects.filter(obj => obj !== 'D');
  return remainingObjects;
}


/**
 * Return new 2D fields after move of the spaceship represented as object 'S'.
 * Dicection is one of 'left', 'ahead', 'right'.
 */
function performMove(fields, direction) {
  const oldSpaceshipPosition = findSpaceshipPosition(fields);
  const dx = { left: -1, ahead: 0, right: 1 }[direction];
  const newSpaceshipPosition = [oldSpaceshipPosition[0] - 1, oldSpaceshipPosition[1] + dx];
  const newFields = fields.map((row, i) => row.map((field, j) => {
    const [background, oldObjects] = field;
    let newObjects = oldObjects;
    if (i === oldSpaceshipPosition[0] && j === oldSpaceshipPosition[1]) {
      if (outsideWorld(fields, newSpaceshipPosition)) {
        let border = null;
        if (i === 0) {
          border = 'top';
        } else if (j === 0) {
          border = 'left';
        } else {
          border = 'right';
        }
        newObjects = [`spaceship-out-${border}`];
      } else {
        newObjects = removeSpaceship(oldObjects);
      }
    }
    if (i === newSpaceshipPosition[0] && j === newSpaceshipPosition[1]) {
      if (onRock(fields, newSpaceshipPosition)) {
        newObjects = [...newObjects, 'spaceship-broken'];
      } else {
        newObjects = [...newObjects, 'S'];
      }
    }
    return [background, newObjects];
  }));
  return newFields;
}


function removeSpaceship(objects) {
  return objects.filter(object => object !== 'S');
}


function performShot(fields) {
  const [yStart, x] = findSpaceshipPosition(fields);
  const noObjectAt = y => fields[y][x][1].length === 0;
  let yEnd = yStart - 1;
  while (yEnd > 0 && noObjectAt(yEnd)) {
    yEnd--;
  }
  const newFields = fields.map((row, i) => row.map((field, j) => {
    const [background, oldObjects] = field;
    let newObjects = oldObjects;
    if (j === x) {
      if (i === yStart) {
        newObjects = ['laser-start', ...oldObjects];
      } else if (yStart > i && i > yEnd) {
        newObjects = ['laser', ...oldObjects];
      } else if (i === yEnd) {
        newObjects = ['laser-end', ...oldObjects.map(shootObject)];
      }
    }
    return [background, newObjects];
  }));
  return newFields;
}


function shootObject(obj) {
  // TODO: improve readability and maintainability
  const shootableObjects = new Set(['M']);
  const shotObject = (shootableObjects.has(obj)) ? 'explosion' : obj;
  return shotObject;
}


function findSpaceshipPosition(fields) {
  for (let i = 0; i < fields.length; i++) {
    for (let j = 0; j < fields[i].length; j++) {
      const objects = fields[i][j][1];
      if (objects.some(obj => obj === 'spaceship-out-top')) {
        return [i - 1, j];
      }
      if (objects.some(obj => obj === 'spaceship-out-left')) {
        return [i, j - 1];
      }
      if (objects.some(obj => obj === 'spaceship-out-right')) {
        return [i, j + 1];
      }
      if (objects.some(obj => obj === 'S' || obj.startsWith('spaceship'))) {
        return [i, j];
      }
    }
  }
  return null;
}


function getPositionsWithObject(fields, searchedObject) {
  // TODO: rewrite: unnest fields -> simple filter + don't use magic literals
  const positions = [];
  for (let i = 0; i < fields.length; i++) {
    for (let j = 0; j < fields[i].length; j++) {
      const objects = fields[i][j][1];
      if (objects.some(obj => obj === searchedObject)) {
        positions.push([i, j]);
      }
    }
  }
  return positions;
}


function gameSolved(fields, spaceship) {
  if (isSpaceshipDead(fields, spaceship)) {
    return false;
  }
  const solved = countDiamonds(fields) === 0 && lastRowReached(spaceship);
  return solved;
}


function lastRowReached(spaceship) {
  return spaceship[0] === 0;
}


function isSpaceshipDead(fields, spaceship) {
  return outsideWorld(fields, spaceship) || onRock(fields, spaceship);
}


function outsideWorld(fields, position) {
  const [y, x] = position;
  const [minX, maxX] = [0, fields[0].length - 1];
  const [minY, maxY] = [0, fields.length - 1];
  return (x < minX || x > maxX || y < minY || y > maxY);
}


function beyondLastRow(fields, position) {
  const [y, x] = position;
  return y < 0;
}


function beyondEdges(fields, position) {
  const [y, x] = position;
  const [minX, maxX] = [0, fields[0].length - 1];
  return (x < minX || x > maxX);
}


function onRock(fields, position) {
  const rockObjects = new Set(['M', 'A']);  // TODO: factor out to common world description?)
  const [y, x] = position;
  const objects = fields[y][x][1];
  return objects.some(object => rockObjects.has(object));
}


function onAsteoroid(fields, position) {
  const [y, x] = position;
  const objects = fields[y][x][1];
  return objects.includes('A');
}


function onMeteoroid(fields, position) {
  const [y, x] = position;
  const objects = fields[y][x][1];
  return objects.includes('M');
}


function countDiamonds(fields) {
  let count = 0;
  fields.forEach(row => row.forEach(field => field[1].forEach(object => {
    count += (object === 'D') ? 1 : 0;
  })));
  return count;
}
