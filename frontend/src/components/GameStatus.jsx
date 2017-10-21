import React, { PropTypes } from 'react';
import TaskName from './TaskName';
import Icon from './Icon';

export default function GameStatus({ taskId, solved, dead, diamonds, energy, length }) {
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
      <span style={{ display: 'block' }}>
        <TaskName taskId={taskId} />
        {solved && <span style={{ float: 'right' }}>&#10003;</span>}
        {dead && <span style={{ float: 'right' }}>&#10005;</span>}
      </span>
      <span style={{ display: 'block' }}>
        { diamonds.total > 0 &&
          <span
            className="instructionable-diamonds-status"
            style={counterStyle}
          >
            <Icon name="diamond" style={{ marginRight: 2 }} />
            {diamonds.taken}/{diamonds.total}
          </span>
        }
        { energy.full !== null &&
          <span
            className="instructionable-energy-status"
            style={counterStyle}
          >
            <Icon name="energy" style={{ marginRight: 2 }} />
            {energy.current}/{energy.full}
          </span>
        }
        { length.limit !== null &&
          <span
            className="instructionable-length-limit"
            style={counterStyle}
          >
            <Icon name="length" style={{ marginRight: 2 }} />
            {length.used}/{length.limit}
          </span>
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
