import React, { PropTypes } from 'react';
import { connect } from 'react-redux';
import TaskEditor from '../components/TaskEditor';
import { parseSpaceWorld } from '../core/spaceWorldDescription';
import { setTask } from '../actions/taskEnvironment';


class TaskEditorWrapper extends React.Component {
  componentWillMount() {
    this.props.setTask(this.props.taskEnvironmentId, this.props.initialTask);
  }

  render() {
    return (
      <TaskEditor
        taskEnvironmentId={this.props.taskEnvironmentId}
      />
    );
  }
}

TaskEditorWrapper.propTypes = {
  taskEnvironmentId: PropTypes.string.isRequired,
  initialTask: PropTypes.object.isRequired,
  setTask: PropTypes.func.isRequired,
};

const defaultInitialTask = {
  id: 'nameless-task',
  category: 'uncategorized',
  setting: {
    fields: parseSpaceWorld(`\
      |b |b |b |b |b |
      |k |k |k |k |k |
      |k |k |k |k |k |
      |k |k |k |k |k |
      |k |k |kS|k |k |`),
  },
};

TaskEditorWrapper.defaultProps = {
  taskEnvironmentId: 'TASK_ENVIRONMENT_FOR_TASK_EDITOR',
  initialTask: defaultInitialTask,
};

// eslint-disable-next-line no-unused-vars
function mapStateToProps(state) {
  return {};
}

const actionCreators = { setTask };
const TaskEditorContainer = connect(mapStateToProps, actionCreators)(TaskEditorWrapper);
export default TaskEditorContainer;
