import React from 'react';
import PropTypes from 'prop-types';
import TaskName from './TaskName';
import Icon from './Icon';
import Instructable from '../containers/Instructable';

export default function GameStatus({ taskId, level, solved, dead, diamonds, energy, length }) {
  const counterStyle = {
    paddingRight: 4,
    marginRight: 6,
  };
  return (
    <span
      style={{
        display: 'block',
        fontSize: 20,
        marginLeft: 2,
        marginTop: 1,
      }}
    >
      <span className="text" style={{ display: 'block' }}>
        <TaskName taskId={taskId} />
        <span style={{ float: 'right', marginRight: 5 }}>
          L{level}
        </span>
        {solved && <span style={{ float: 'right' }}>&#10003;</span>}
        {dead && <span style={{ float: 'right' }}>&#10005;</span>}
      </span>
      <span className="text" style={{ display: 'block' }}>
        { diamonds.total > 0 &&
          <Instructable instruction="task-diamond-status" position="bottom-left">
            <span style={counterStyle} >
              <Icon name="diamond" style={{ marginRight: 2 }} />
              {diamonds.taken}/{diamonds.total}
            </span>
          </Instructable>
        }
        { energy.full !== null &&
          <Instructable instruction="task-energy-status" position="bottom-left">
            <span style={counterStyle}>
              <Icon name="energy" style={{ marginRight: 2 }} />
              {energy.current}/{energy.full}
            </span>
          </Instructable>
        }
        { length.limit !== null &&
          <Instructable instruction="task-length-limit" position="bottom-left">
            <span style={counterStyle} >
              <Icon name="length" style={{ marginRight: 2 }} />
              {length.used}/{length.limit}
            </span>
          </Instructable>
        }
      </span>
    </span>
  );
}

GameStatus.propTypes = {
  taskId: PropTypes.string.isRequired,
  diamonds: PropTypes.object.isRequired,
  energy: PropTypes.object.isRequired,
  length: PropTypes.object.isRequired,
  solved: PropTypes.bool,
  dead: PropTypes.bool,
};

GameStatus.defaultProps = {
  solved: false,
  dead: false,
};
