import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import SpaceGame from '../components/SpaceGame';
import { createTaskEnvironment,
         runProgram,
         resetGame,
         setSpeed,
         doActionMove } from '../actions';
import { getGameState } from '../selectors/gameState';
import {
  getTaskId,
  getTaskLevel,
  getLengthLimit,
  getGamePanelWidth,
  getSpeed,
  } from '../selectors/taskEnvironment';


class SpaceGameWrapper extends React.Component {
  constructor(props) {
    super(props);
    this.handleControlClicked = this.handleControlClicked.bind(this);
  }

  componentWillMount() {
    this.props.createTaskEnvironment(this.props.taskEnvironmentId);
  }

  handleControlClicked(control, value) {
    switch (control) {
      case 'fly':
      case 'left':
      case 'right':
      case 'shoot':
        this.props.doActionMove(this.props.taskEnvironmentId, control, false);
        break;
      case 'run':
        this.props.runProgram(this.props.taskEnvironmentId);
        break;
      case 'reset':
        this.props.resetGame(this.props.taskEnvironmentId);
        break;
      case 'speed':
        this.props.setSpeed(this.props.taskEnvironmentId, value);
        break;
      default:
        throw new Error(`Undefined control ${control}`);
    }
  }

  render() {
    return (
      <SpaceGame
        taskId={this.props.taskId}
        level={this.props.level}
        gameState={this.props.gameState}
        lengthLimit={this.props.lengthLimit}
        width={this.props.width}
        controls={this.props.controls}
        speed={this.props.speed}
        onControlClicked={this.handleControlClicked}
        showHeader={this.props.showHeader}
      />
    );
  }

}

SpaceGameWrapper.propTypes = {
  taskEnvironmentId: PropTypes.string.isRequired,
  taskId: PropTypes.string,
  controls: PropTypes.array,
  speed: PropTypes.number.isRequired,
  gameState: PropTypes.object.isRequired,
  lengthLimit: PropTypes.object.isRequired,
  width: PropTypes.number.isRequired,
  runProgram: PropTypes.func.isRequired,
  resetGame: PropTypes.func.isRequired,
  setSpeed: PropTypes.func.isRequired,
  doActionMove: PropTypes.func.isRequired,
  createTaskEnvironment: PropTypes.func.isRequired,
  showHeader: PropTypes.bool,
};

SpaceGameWrapper.defaultProps = {
  showHeader: true,
}

function mapStateToProps(state, props) {
  const { taskEnvironmentId, controls } = props;
  const gameState = getGameState(state, taskEnvironmentId);
  const lengthLimit = getLengthLimit(state, taskEnvironmentId);
  const taskId = getTaskId(state, taskEnvironmentId);
  const level = getTaskLevel(state, taskEnvironmentId);
  const width = getGamePanelWidth(state, taskEnvironmentId);
  const speed = getSpeed(state, taskEnvironmentId);
  return { taskEnvironmentId, taskId, level, gameState, lengthLimit, width, controls, speed };
}


const actionCreators = {
  runProgram: runProgram.start,
  createTaskEnvironment,
  resetGame,
  setSpeed,
  doActionMove,
};
const SpaceGameContainer = connect(mapStateToProps, actionCreators)(SpaceGameWrapper);
export default SpaceGameContainer;
