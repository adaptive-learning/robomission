import React, { PropTypes } from 'react';
import { Link } from 'react-router';
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
        label={<span style={{ position: 'relative', top: 1 }}><TaskName taskId={task.taskId} /></span>}
        primary={true}
      />
    </Link>
  );
}


NextTaskButton.propTypes = {
  task: PropTypes.object,
};
