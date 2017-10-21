import React, { PropTypes } from 'react';
import { connect } from 'react-redux';
import SettingEditor from '../components/SettingEditor';
import { changeSetting,
         importTask,
         exportTask,
         setEditorType } from '../actions/taskEnvironment';
import { switchVimMode } from '../actions/taskEditor';
import { getSpaceWorldText,
         isSpaceWorldTextValid,
         getTask,
         getEditorType } from '../selectors/taskEnvironment';
import { isVimModeEnabled } from '../selectors/taskEditor';


class SettingEditorWrapper extends React.Component {
  constructor(props) {
    super(props);

    this.handleChangeSetting = spaceWorldText => {
      this.props.changeSetting(this.props.taskEnvironmentId, { spaceWorldText });
      this.forceUpdate();
    };

    this.handleTaskIdChange = event => {
      const id = event.target.value;
      this.props.changeSetting(this.props.taskEnvironmentId, { id });
    };

    this.handleCategoryChange = (event, index, value) => {
      let category = value;
      if (category.length === 0) {
        category = null;
      }
      this.props.changeSetting(this.props.taskEnvironmentId, { category });
    };

    this.handleEnergyChange = event => {
      const energyString = event.target.value;
      const energyNumber = parseInt(energyString, 10);
      const energy = isNaN(energyNumber) ? null : energyNumber;
      this.props.changeSetting(this.props.taskEnvironmentId, { energy });
    };

    this.handleLengthLimitChange = event => {
      const lengthLimitString = event.target.value;
      const lengthLimitNumber = parseInt(lengthLimitString, 10);
      const length = isNaN(lengthLimitNumber) ? null : lengthLimitNumber;
      this.props.changeSetting(this.props.taskEnvironmentId, { length });
    };

    this.handleEditorTypeChange = () => {
      const newEditorType = (this.props.editorType === 'blockly') ? 'code' : 'blockly';
      this.props.setEditorType(this.props.taskEnvironmentId, newEditorType);
    };

    this.handleSwitchMode = this.props.switchVimMode.bind(this);
    this.exportTask = this.props.exportTask.bind(this, this.props.taskEnvironmentId);
    this.importTask = this.props.importTask.bind(this, this.props.taskEnvironmentId);
  }

  render() {
    return (
      <SettingEditor
        spaceWorldText={this.props.spaceWorldText}
        isValid={this.props.isValid}
        onChange={this.handleChangeSetting}
        taskId={this.props.taskId}
        onTaskIdChange={this.handleTaskIdChange}
        category={this.props.category || ''}
        onCategoryChange={this.handleCategoryChange}
        energy={this.props.energy}
        onEnergyChange={this.handleEnergyChange}
        lengthLimit={this.props.lengthLimit}
        onLengthLimitChange={this.handleLengthLimitChange}
        vimMode={this.props.vimMode}
        onSwitchMode={this.handleSwitchMode}
        onImport={this.importTask}
        onExport={this.exportTask}
        blocklyEditorType={this.props.editorType === 'blockly'}
        onEditorTypeChange={this.handleEditorTypeChange}
      />
    );
  }
}

SettingEditorWrapper.propTypes = {
  taskEnvironmentId: PropTypes.string.isRequired,
  spaceWorldText: PropTypes.string.isRequired,
  isValid: PropTypes.bool.isRequired,
  changeSetting: PropTypes.func.isRequired,
  taskId: PropTypes.string.isRequired,
  category: PropTypes.string,
  energy: PropTypes.number,
  lengthLimit: PropTypes.number,
  vimMode: PropTypes.bool.isRequired,
  switchVimMode: PropTypes.func.isRequired,
  importTask: PropTypes.func.isRequired,
  exportTask: PropTypes.func.isRequired,
  editorType: PropTypes.oneOf(['code', 'blockly']).isRequired,
  setEditorType: PropTypes.func.isRequired,
};

function mapStateToProps(state, props) {
  const { taskEnvironmentId } = props;
  const { id, category, setting } = getTask(state, taskEnvironmentId);
  const { energy, length } = setting;
  const spaceWorldText = getSpaceWorldText(state, taskEnvironmentId);
  const isValid = isSpaceWorldTextValid(state, taskEnvironmentId);
  const editorType = getEditorType(state, taskEnvironmentId);
  const vimMode = isVimModeEnabled(state);
  return {
    taskEnvironmentId,
    taskId: id,
    category,
    energy,
    lengthLimit: length,
    spaceWorldText,
    isValid,
    vimMode,
    editorType,
  };
}

const actionCreators = { changeSetting, switchVimMode, importTask, exportTask, setEditorType };
const SettingEditorContainer = connect(mapStateToProps, actionCreators)(SettingEditorWrapper);
export default SettingEditorContainer;
