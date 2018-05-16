import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import BlocklyEditor from '../components/BlocklyEditor';
import {
  getRoboAst,
  getEditorSessionId,
  getHighlightedBlock,
  getLengthLimit,
  getToolbox
  } from '../selectors/taskEnvironment';
import { editProgramAst, registerInstructables } from '../actions';
import { expandBlocks } from '../core/toolbox';
import { getAllBlocksList } from '../core/blocks';


class BlocklyEditorWrapper extends React.Component {
  constructor(props) {
    super(props);
    this.changeRoboAst = this.props.changeRoboAst.bind(this, this.props.taskEnvironmentId);
    this.registerInstructables = this.props.registerInstructables.bind(this);
    const generalInstructions =  ['task-toolbox', 'task-snapping'];
    const blockInstructions = getAllBlocksList().map(id => `task-block-${id}`);
    this.allInstructions = generalInstructions.concat(blockInstructions);
  }

  componentDidMount() {
    this.updateInstructables();
  }

  componentDidUpdate(prevProps) {
    if (prevProps.editorSessionId !== this.props.editorSessionId) {
      this.updateInstructables();
    }
  }

  componentWillUnmount() {
    this.registerInstructables([], this.allInstructions);
  }

  resize() {
    this.blocklyEditor.resize();
  }

  updateInstructables() {
    // Toolbox.
    let instructables = [ { instructionId: 'task-toolbox', position: 'right' } ];
    // TODO: Find a way through a public API.
    const toolboxSvg = this.blocklyEditor.blocklyToolbox.svgGroup_;
    toolboxSvg.classList.add('instructable-task-toolbox');
    // Snapping.
    const programBlocks = this.blocklyEditor.blocklyWorkspace.getAllBlocks();
    for (const block of programBlocks) {
      if (block.type === 'start') {
        const svgElement = block.getSvgRoot();
        svgElement.classList.add('instructable-task-snapping');
        instructables.push({ instructionId: 'task-snapping', position: 'bottom-left' });
      }
    }
    // Blocks.
    const blocks = getAllBlocksList();
    const toolboxBlocks = this.blocklyEditor.blocklyToolbox.getAllBlocks();
    for (const block of toolboxBlocks) {
      const svgElement = block.getSvgRoot();
      // TODO: Sync the class with store.instructions.
      const instructionId = `task-block-${block.type}`;
      const instructableClassName = `instructable-${instructionId}`;
      // TODO: addClass only working in modern browsers -> include polyfill
      // (alternatively, use Blockly.utils.addClass)
      svgElement.classList.add(instructableClassName);
      instructables.push({ instructionId, position: 'bottom-left' });
    }

    // TODO: Make it more explicit that it's OK to send all instructions as
    // the second parameter (and not just the ones that are unregistered
    // (currently, it works just because of an implementation detail of
    // first unregistering, than registering in the reducer).
    this.registerInstructables(instructables, this.allInstructions);
  }

  render() {
    return (
      <BlocklyEditor
        ref={ref => { this.blocklyEditor = ref; }}
        roboAst={this.props.roboAst}
        toolboxBlocks={expandBlocks(this.props.toolbox)}
        lengthLimit={this.props.lengthLimit}
        editorSessionId={this.props.editorSessionId}
        highlightedBlock={this.props.highlightedBlock}
        onChange={this.changeRoboAst}
      />
    );
  }
}

BlocklyEditorWrapper.propTypes = {
  taskEnvironmentId: PropTypes.string.isRequired,
  toolbox: PropTypes.array.isRequired,
  editorSessionId: PropTypes.number,
  roboAst: PropTypes.object.isRequired,
  lengthLimit: PropTypes.number,
  changeRoboAst: PropTypes.func.isRequired,
};

function mapStateToProps(state, props) {
  const { taskEnvironmentId } = props;
  const roboAst = getRoboAst(state, taskEnvironmentId);
  const editorSessionId = getEditorSessionId(state, taskEnvironmentId);
  const highlightedBlock = getHighlightedBlock(state, taskEnvironmentId);
  const { limit: lengthLimit } = getLengthLimit(state, taskEnvironmentId);
  const toolbox = getToolbox(state, taskEnvironmentId);
  return { taskEnvironmentId, toolbox, roboAst, lengthLimit, editorSessionId, highlightedBlock };
}


const actionCreators = {
  registerInstructables,
  changeRoboAst: editProgramAst,
};
const BlocklyEditorContainer = connect(mapStateToProps,
                                       actionCreators,
                                       null,
                                       { withRef: true })(BlocklyEditorWrapper);
export default BlocklyEditorContainer;
