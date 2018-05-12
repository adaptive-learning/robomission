import React from 'react';
import PropTypes from 'prop-types';
import AceEditor from 'react-ace';
import Toggle from 'material-ui/Toggle';
import { List, ListItem } from 'material-ui/List';
import Paper from 'material-ui/Paper';
import Divider from 'material-ui/Divider';
import IconDescription from 'material-ui/svg-icons/action/description';
import IconUpload from 'material-ui/svg-icons/content/unarchive';
import IconDownload from 'material-ui/svg-icons/content/move-to-inbox';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import TextField from 'material-ui/TextField';
import muiThemeable from 'material-ui/styles/muiThemeable';

import 'brace/theme/solarized_dark';
import 'brace/keybinding/vim';
import '../core/spaceWorldHighlighter';


function SettingEditor({
  spaceWorldText,
  spaceWorldErrors,
  onChange,
  taskId,
  onTaskIdChange,
  toolbox,
  onToolboxChange,
  energy,
  onEnergyChange,
  lengthLimit,
  onLengthLimitChange,
  vimMode,
  onSwitchMode,
  onImport,
  onExport,
  blocklyEditorType,
  onEditorTypeChange,
  muiTheme,
}) {
  const annotations = spaceWorldErrors.map(
    ({ row, col, message }) => ({ row, column: col, text: message, type: 'error'}));

  return (
    <div
      className="instructionable-env-task-editor"
      style={{ overflowX: 'hidden', backgroundColor: muiTheme.palette.canvasColor }}
    >
      <div style={{ marginLeft: 5, marginBottom: 10 }}>
        <div>
          <TextField
            id="setting-editor-task-id"
            floatingLabelText="Task Name"
            value={taskId}
            onChange={onTaskIdChange}
          />
        </div>
        <div>
          <SelectField
            floatingLabelText="Toolbox"
            value={toolbox}
            onChange={onToolboxChange}
          >
            <MenuItem value={'fly'} primaryText="fly" />
            <MenuItem value={'shoot'} primaryText="shoot" />
          </SelectField>
        </div>
        <div>
          <TextField
            id="setting-editor-energy"
            floatingLabelText="Energy"
            floatingLabelFixed={true}
            value={energy || ''}
            onChange={onEnergyChange}
          />
        </div>
        <div>
          <TextField
            id="setting-editor-length-limit"
            floatingLabelText="Length Limit"
            floatingLabelFixed={true}
            value={lengthLimit || ''}
            onChange={onLengthLimitChange}
          />
        </div>
      </div>
      <AceEditor
        value={spaceWorldText}
        onChange={onChange}
        mode="spaceworld"
        theme="solarized_dark"
        fontSize={18}
        keyboardHandler={vimMode ? 'vim' : null}
        annotations={annotations}
        editorProps={{ $blockScrolling: true }}
        width="100%"
        height="300px"
        style={{ display: 'block' }}
      />
      <div>
        <Paper style={{ width: 350, margin: 10 }}>
          <List>
            <ListItem
              primaryText="Vim SpaceWorld editor"
              rightToggle={<Toggle toggled={vimMode} onToggle={onSwitchMode} />}
            />
            <ListItem
              primaryText="Blockly editor"
              rightToggle={<Toggle toggled={blocklyEditorType} onToggle={onEditorTypeChange} />}
            />
          </List>
          <Divider />
          <List>
            <ListItem primaryText="Import task" onClick={onImport} leftIcon={<IconUpload />} />
            <ListItem primaryText="Export task" onClick={onExport} leftIcon={<IconDownload />} />
          </List>
          <Divider />
          <List>
            <ListItem
              href="https://github.com/adaptive-learning/flocs-visual-components/blob/master/docs/space-world.md"
              target="_blank"
              rel="noreferrer noopener"
              primaryText="Open SpaceWorld desription"
              leftIcon={<IconDescription />}
            />
          </List>
        </Paper>
      </div>
    </div>
  );
}

SettingEditor.propTypes = {
  spaceWorldText: PropTypes.string.isRequired,
  spaceWorldErrors: PropTypes.array.isRequired,
  onChange: PropTypes.func.isRequired,
  taskId: PropTypes.string.isRequired,
  onTaskIdChange: PropTypes.func.isRequired,
  toolbox: PropTypes.string.isRequired,
  onToolboxChange: PropTypes.func.isRequired,
  energy: PropTypes.number,
  onEnergyChange: PropTypes.func.isRequired,
  lengthLimit: PropTypes.number,
  onLengthLimitChange: PropTypes.func.isRequired,
  vimMode: PropTypes.bool.isRequired,
  onSwitchMode: PropTypes.func.isRequired,
  onImport: PropTypes.func.isRequired,
  onExport: PropTypes.func.isRequired,
  blocklyEditorType: PropTypes.bool.isRequired,
  onEditorTypeChange: PropTypes.func.isRequired,
  muiTheme: PropTypes.object.isRequired,
};


export default muiThemeable()(SettingEditor);
