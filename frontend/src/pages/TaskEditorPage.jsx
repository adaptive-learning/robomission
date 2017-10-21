import React from 'react';
import TaskEditorContainer from '../containers/TaskEditorContainer';


export default class TaskEditorPage extends React.Component {
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
        <TaskEditorContainer />
      </div>
    );
  }
}
