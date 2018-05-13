import React from 'react';
import PropTypes from 'prop-types';
import StarBorder from 'material-ui/svg-icons/toggle/star-border';
import Star from 'material-ui/svg-icons/toggle/star';


const propTypes = {
  value: PropTypes.number,
  max: PropTypes.number,
  color: PropTypes.string,
  height: PropTypes.number,
};

const defaultProps = {
  color: 'white',
  height: 20,
};

class Rating extends React.Component {
  createStar(index) {
    const filled = index < this.props.value;
    if (filled) {
      return (
        <Star key={index} color={this.props.color}/>
      );
    } else {
      return (
        <StarBorder key={index} color={this.props.color}/>
      );
    }
  }

  render() {
    const stars = Array.from(
      {length: this.props.max},
      (_, i) => this.createStar(i));
    return (
      <span>
        {stars}
      </span>
    );
  }
}


Rating.propTypes = propTypes;
Rating.defaultProps = defaultProps;

export default Rating;
