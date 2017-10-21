import React, { PropTypes } from 'react';
import SplitPane from 'react-split-pane';
import TaskEnvironmentContainer from '../containers/TaskEnvironmentContainer';
import SettingEditorContainer from '../containers/SettingEditorContainer';


export default class TaskEditor extends React.Component {
  constructor(props) {
    super(props);
    this.handleSplitChange = this.resize.bind(this);
  }

  resize() {
    if (this.taskEnvironment != null) {
      this.taskEnvironment.resize();
    }
  }

  render() {
    const { taskEnvironmentId } = this.props;
    return (
      <SplitPane
        split="vertical"
        defaultSize="50%"
        maxSize={-350}
        resizerStyle={{
          backgroundColor: '#aaa',
          width: 4,
          cursor: 'col-resize',
        }}
        pane2Style={{
          overflowY: 'auto',
        }}
        onChange={this.handleSplitChange}
      >
        <TaskEnvironmentContainer
          taskEnvironmentId={taskEnvironmentId}
          controls={['fly', 'left', 'right', 'shoot', 'run', 'reset']}
          ref={ref => { this.taskEnvironment = ref ? ref.getWrappedInstance() : null; }}
        />
        <SettingEditorContainer
          taskEnvironmentId={taskEnvironmentId}
        />
      </SplitPane>
    );
  }
}

TaskEditor.propTypes = {
  taskEnvironmentId: PropTypes.string.isRequired,
};

TaskEditor.defaultProps = {
  taskEnvironmentId: 'TASK_ENVIRONMENT_FOR_TASK_EDITOR',
};
