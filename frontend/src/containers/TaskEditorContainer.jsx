import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import TaskEditor from '../components/TaskEditor';
import { setTask } from '../actions';
import { stripIndentation } from '../utils/text'


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
  setting: {
    toolbox: 'shoot',
    fields: stripIndentation`\
      |b |b |b |b |b |
      |k |k |k |k |k |
      |k |k |k |k |k |
      |k |k |k |k |k |
      |k |k |kS|k |k |`,
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
