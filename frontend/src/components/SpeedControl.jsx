import React from 'react';
import PropTypes from 'prop-types';
import Slider from 'material-ui/Slider';
import muiThemeable from 'material-ui/styles/muiThemeable';


const propTypes = {
  speed: PropTypes.number.isRequired,
  min: PropTypes.number.isRequired,
  max: PropTypes.number.isRequired,
  width: PropTypes.number.isRequired,
  onChange: PropTypes.func.isRequired,
};

const defaultProps = {
  width: 200,
  min: 1,
  max: 5,
};

class SpeedControl extends React.Component {
  handleChange = (event, value) => {
    this.props.onChange(value);
  };

  render() {
    return (
      <Slider
        min={this.props.min}
        max={this.props.max}
        step={1}
        value={this.props.speed}
        onChange={this.handleChange}
      />
    );
  }
}


SpeedControl.propTypes = propTypes;
SpeedControl.defaultProps = defaultProps;
SpeedControl = muiThemeable()(SpeedControl);

export default SpeedControl;
