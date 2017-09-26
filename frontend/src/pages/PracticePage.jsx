import React from 'react';
import { connect } from 'react-redux';
import PracticeContainer from '../containers/PracticeContainer';
import { practicePageTaskEnvironmentId } from '../selectors/taskEnvironment';


function getProps(state, props) {
  return {
    taskId: props.routeParams.taskId,
  };
}

@connect(getProps)
export default class PracticePage extends React.Component {
  render() {
    return (
      <div
        style={{
          position: 'absolute',
          top: 64,  // TODO: unhardcode using app height in flocs-theme
          bottom: 0,
          left: 0,
          right: 0,
        }}
      >
        <PracticeContainer
          taskEnvironmentId={practicePageTaskEnvironmentId}
          taskId={this.props.taskId}
        />
      </div>
    );
  }
}
