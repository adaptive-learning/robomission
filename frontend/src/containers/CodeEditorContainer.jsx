import React, { PropTypes } from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import CodeEditor from '../components/CodeEditor';
import { changeCode } from '../actions/taskEnvironment';


class CodeEditorWrapper extends React.Component {
  constructor(props) {
    super(props);
    this.changeCode = this.props.changeCode.bind(this, this.props.taskEnvironmentId);
  }

  render() {
    return (
      <CodeEditor
        code={this.props.code}
        onChange={this.changeCode}
      />
    );
  }
}

CodeEditorWrapper.propTypes = {
  taskEnvironmentId: PropTypes.string.isRequired,
  code: PropTypes.string.isRequired,
  changeCode: PropTypes.func.isRequired,
};

function mapStateToProps(state, props) {
  const { taskEnvironmentId } = props;
  const taskEnvironment = state.taskEnvironments[taskEnvironmentId];
  const code = taskEnvironment.code;
  return { taskEnvironmentId, code };
}


function mapDispatchToProps(dispatch) {
  return bindActionCreators({ changeCode }, dispatch);
}


const CodeEditorContainer = connect(mapStateToProps, mapDispatchToProps)(CodeEditorWrapper);
export default CodeEditorContainer;
