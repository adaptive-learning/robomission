import React from 'react';
import PropTypes from 'prop-types';
//import StarBorder from 'material-ui/svg-icons/toggle/star-border';
//import Star from 'material-ui/svg-icons/toggle/star';
import Puzzle from 'material-ui/svg-icons/action/extension';


const propTypes = {
  value: PropTypes.number.isRequired,
  max: PropTypes.number.isRequired,
  color: PropTypes.string,
  height: PropTypes.number,
};

const defaultProps = {
  color: '#eee', // 'white',
  height: 20,
};

class Rating extends React.Component {
  createStar(index) {
    // We decided to draw all "stars" filled.
    // TODO: Rename Star (it's not star anymore.)
    return (
      <Puzzle key={index} color={this.props.color}/>
    );
    /*
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
    */
  }

  render() {
    const { value, max, color, height, ...otherProps } = this.props;
    const stars = Array.from({length: max}, (_, i) => this.createStar(i));
    return (
      <span style={{ display: 'inline-block' }} {...otherProps}>
        {stars}
      </span>
    );
  }
}


Rating.propTypes = propTypes;
Rating.defaultProps = defaultProps;

export default Rating;
