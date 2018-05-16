import React from 'react';
import PropTypes from 'prop-types';
import RaisedButton from 'material-ui/RaisedButton';
import SpeedControl from '../components/SpeedControl';
import { translate } from '../localization';
import Instructable from '../containers/Instructable';

export default function GameControls({ controls, speed, onClick }) {
  function visible(controlName) {
    return controls[controlName] === 'active' || controls[controlName] === 'passive';
  }

  function disabled(controlName) {
    return controls[controlName] === 'passive';
  }

  function handleSpeedChange(speed) {
    return onClick('speed', speed);
  }

  function conditionallyRenderControlButton(name, label, emph = null, minWidth = 50) {
    if (!(visible(name))) {
      return null;
    }
    let button = (
      <RaisedButton
        label={label}
        disabled={disabled(name)}
        primary={emph === 'primary'}
        secondary={emph === 'accent'}
        style={{ margin: 2, minWidth }}
        onClick={() => onClick(name)}
      />
    );
    if (name === 'run') {
      button = (
        <Instructable instruction="task-controls" position="bottom-left">
          {button}
        </Instructable>
      );
    }
    return button;
  }

  function conditionallyRenderSpeedControl() {
    if (!(visible('speed'))) {
      return null;
    }
    return (
      <SpeedControl
        speed={speed}
        onChange={handleSpeedChange}
      />
    );
  }

  return (
    <span style={{ display: 'block', margin: '5px 4px' }}>
      {(visible('fly') || visible('left') || visible('right') || visible('shoot')) &&
        <span style={{ display: 'block', marginBottom: '2px' }}>
          {conditionallyRenderControlButton('left', '↖', 'primary')}
          {conditionallyRenderControlButton('fly', '↑', 'primary')}
          {conditionallyRenderControlButton('right', '↗', 'primary')}
          {conditionallyRenderControlButton('shoot', '★', 'primary')}
        </span>
      }
      {conditionallyRenderControlButton('run', translate('Run'), 'primary', 88)}
      {conditionallyRenderControlButton('reset', 'Reset', 'accent', false, 88)}
      {conditionallyRenderSpeedControl()}
    </span>
  );
}

GameControls.propTypes = {
  controls: PropTypes.object,
  onClick: PropTypes.func,
};

GameControls.defaultProps = {
  controls: { commands: 'active', run: 'active', reset: 'hidden' },
  onClick: null,
};
