import React from 'react';
import PropTypes from 'prop-types';
import StarBorder from 'material-ui/svg-icons/toggle/star-border';
import Star from 'material-ui/svg-icons/toggle/star';


const propTypes = {
  value: PropTypes.number.isRequired,
  max: PropTypes.number.isRequired,
  color: PropTypes.string,
  height: PropTypes.number,
  className: PropTypes.string,  // TODO: Generalize (Apply all other props to
                                // the top-level span.)
};

const defaultProps = {
  color: 'white',
  height: 20,
  className: '',
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
      <span className={this.props.className}>
        {stars}
      </span>
    );
  }
}


Rating.propTypes = propTypes;
Rating.defaultProps = defaultProps;

export default Rating;
