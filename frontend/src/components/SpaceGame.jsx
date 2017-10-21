import React, { PropTypes } from 'react';
import GameStatus from './GameStatus';
import SpaceWorld from './SpaceWorld';
import GameControls from './GameControls';


export default function SpaceGame({
    taskId,
    gameState,
    lengthLimit,
    width,
    controls,
    onControlClicked,
  }) {
  const { fields, stage, diamonds, energy } = gameState;
  const gameOver = (stage === 'solved' || stage === 'dead');
  const initialStage = (stage === 'initial');
  const preparing = (stage === 'preparing');
  const controlsSetting = {
    fly: evaluateVisibility(
      controls.indexOf('fly') < 0 || preparing,
      gameOver),
    left: evaluateVisibility(
      controls.indexOf('left') < 0 || preparing,
      gameOver),
    right: evaluateVisibility(
      controls.indexOf('right') < 0 || preparing,
      gameOver),
    shoot: evaluateVisibility(
      controls.indexOf('shoot') < 0 || preparing,
      gameOver),
    run: evaluateVisibility(
      controls.indexOf('run') < 0 || preparing || !(initialStage),
      false),
    reset: evaluateVisibility(
      controls.indexOf('reset') < 0 || preparing || (initialStage && controls.indexOf('run') >= 0),
      initialStage),
  };
  return (
    <span style={{ display: 'inline-block', verticalAlign: 'top' }}>
      <GameStatus
        taskId={taskId}
        diamonds={diamonds}
        energy={energy}
        length={lengthLimit}
        solved={stage === 'solved'}
        dead={stage === 'dead'}
      />
      <SpaceWorld
        fields={fields}
        width={width}
      />
      <GameControls controls={controlsSetting} onClick={onControlClicked} />
    </span>
  );
}

SpaceGame.propTypes = {
  taskId: PropTypes.string,
  gameState: PropTypes.object.isRequired,
  lengthLimit: PropTypes.object,
  onControlClicked: PropTypes.func,
  controls: PropTypes.array,
  width: PropTypes.number,
};

SpaceGame.defaultProps = {
  taskId: 'nameless-task',
  lengthLimit: { limit: null },
  controls: [],
  width: 280,
};


function evaluateVisibility(hiddenCondition, passiveCondition) {
  if (hiddenCondition) {
    return 'hidden';
  }
  if (passiveCondition) {
    return 'passive';
  }
  return 'active';
}

