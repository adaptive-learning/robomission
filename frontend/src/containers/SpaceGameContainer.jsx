import React, { PropTypes } from 'react';
import { connect } from 'react-redux';
import SpaceGame from '../components/SpaceGame';
import { createTaskEnvironment,
         runProgram,
         resetGame,
         doActionMove } from '../actions/taskEnvironment';
import { getGameState } from '../selectors/gameState';
import { getTaskId, getLengthLimit, getGamePanelWidth } from '../selectors/taskEnvironment';


class SpaceGameWrapper extends React.Component {
  constructor(props) {
    super(props);
    this.handleControlClicked = this.handleControlClicked.bind(this);
  }

  componentWillMount() {
    this.props.createTaskEnvironment(this.props.taskEnvironmentId);
  }

  handleControlClicked(control) {
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
      default:
        throw new Error(`Undefined control ${control}`);
    }
  }

  render() {
    return (
      <SpaceGame
        taskId={this.props.taskId}
        gameState={this.props.gameState}
        lengthLimit={this.props.lengthLimit}
        width={this.props.width}
        controls={this.props.controls}
        onControlClicked={this.handleControlClicked}
      />
    );
  }

}

SpaceGameWrapper.propTypes = {
  taskEnvironmentId: PropTypes.string.isRequired,
  taskId: PropTypes.string,
  controls: PropTypes.array,
  gameState: PropTypes.object.isRequired,
  lengthLimit: PropTypes.object.isRequired,
  width: PropTypes.number.isRequired,
  runProgram: PropTypes.func.isRequired,
  resetGame: PropTypes.func.isRequired,
  doActionMove: PropTypes.func.isRequired,
  createTaskEnvironment: PropTypes.func.isRequired,
};

function mapStateToProps(state, props) {
  const { taskEnvironmentId, controls } = props;
  const gameState = getGameState(state, taskEnvironmentId);
  const lengthLimit = getLengthLimit(state, taskEnvironmentId);
  const taskId = getTaskId(state, taskEnvironmentId);
  const width = getGamePanelWidth(state, taskEnvironmentId);
  return { taskEnvironmentId, taskId, gameState, lengthLimit, width, controls };
}


const actionCreators = { createTaskEnvironment, runProgram, resetGame, doActionMove };
const SpaceGameContainer = connect(mapStateToProps, actionCreators)(SpaceGameWrapper);
export default SpaceGameContainer;
