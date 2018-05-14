import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import RaisedButton from 'material-ui/RaisedButton';
import TaskIcon from 'material-ui/svg-icons/av/play-arrow';
import TaskName from './TaskName';


export default function NextTaskButton({ task }) {
  const style = {
    minWidth: 200,
    display: 'inline-block',
  };
  if (task === null) {
    return (
      <RaisedButton
        style={style}
        className="instructionable-env-recommended-task-button"
        label="..."
        primary={true}
        disabled={false}
      />
    );
  }
  return (
    <Link to={task.url}>
      <RaisedButton
        icon={<TaskIcon style={{ marginLeft: 8 }}/>}
        style={style}
        className="instructionable-env-recommended-task-button"
        label={<span style={{ position: 'relative', top: 1 }}><TaskName taskId={task.taskId} /></span>}
        primary={true}
      />
    </Link>
  );
}


NextTaskButton.propTypes = {
  task: PropTypes.object,
};
