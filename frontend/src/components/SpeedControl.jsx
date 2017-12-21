import React from 'react';
import PropTypes from 'prop-types';
import Slider from 'material-ui/Slider';
import muiThemeable from 'material-ui/styles/muiThemeable';
import Image from '../components/Image';
import Text from '../localization/Text';


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
      <div style={{ marginTop: 15 }}>
        <Image
          imageId="speedometer"
          style={{ height: 35, marginRight: 10, float: 'left' }} />
        <div
          style={{ height: 35, float: 'left' }}
        >
          <Text id="Speed" />
          {`: ${this.props.speed}`}
          <Slider
            min={this.props.min}
            max={this.props.max}
            step={1}
            value={this.props.speed}
            onChange={this.handleChange}
            style={{ width: 120 }}
            sliderStyle={{ marginTop: 2, marginBottom: 0 }}
          />
        </div>
      </div>
    );
  }
}


SpeedControl.propTypes = propTypes;
SpeedControl.defaultProps = defaultProps;
SpeedControl = muiThemeable()(SpeedControl);

export default SpeedControl;
