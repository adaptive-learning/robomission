import React, { PropTypes } from 'react';
import AceEditor from 'react-ace';

import 'brace/theme/solarized_dark';
import '../core/roboCodeHighlighter';


export default class CodeEditor extends React.Component {
  componentDidUpdate() {
    if (this.props.code === '') {
      this.aceEditor.editor.focus();
    }
  }

  render() {
    return (
      <AceEditor
        ref={(ref) => { this.aceEditor = ref; }}
        value={this.props.code}
        onChange={this.props.onChange}
        mode="robocode"
        theme="solarized_dark"
        fontSize={18}
        focus={true}
        editorProps={{ $blockScrolling: true }}
        width="100%"
        height="100%"
        style={{ display: 'inline-block', marginBottom: '-5px' }}
      />
    );
  }
}

CodeEditor.propTypes = {
  code: PropTypes.string,
  onChange: PropTypes.func,
};

CodeEditor.defaultProps = {
  code: '',
  onChange: null,
};
