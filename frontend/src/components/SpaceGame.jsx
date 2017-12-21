import React from 'react';
import PropTypes from 'prop-types';
import GameStatus from './GameStatus';
import SpaceWorld from './SpaceWorld';
import GameControls from './GameControls';


export default function SpaceGame({
    taskId,
    level,
    gameState,
    lengthLimit,
    width,
    controls,
    speed,
    onControlClicked,
    showHeader,
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
  const gameStatus = (
    <GameStatus
      taskId={taskId}
      level={level}
      diamonds={diamonds}
      energy={energy}
      length={lengthLimit}
      solved={stage === 'solved'}
      dead={stage === 'dead'}
    />
  );
  return (
    <span style={{ display: 'inline-block', verticalAlign: 'top' }}>
      {showHeader && gameStatus}
      <SpaceWorld
        fields={fields}
        width={width}
      />
      <GameControls
        controls={controlsSetting}
        speed={speed}
        onClick={onControlClicked}
      />
    </span>
  );
}

SpaceGame.propTypes = {
  taskId: PropTypes.string,
  gameState: PropTypes.object.isRequired,
  lengthLimit: PropTypes.object,
  onControlClicked: PropTypes.func,
  controls: PropTypes.array,
  speed: PropTypes.number.isRequired,
  width: PropTypes.number,
  showHeader: PropTypes.bool,
};

SpaceGame.defaultProps = {
  taskId: 'nameless-task',
  lengthLimit: { limit: null },
  controls: [],
  width: 280,
  showHeader: false,
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

