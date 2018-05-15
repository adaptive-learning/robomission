import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { registerInsructionable } from '../actions';


const getProps = state => ({
});

const actionCreators = {
  registerInsructionable,
};



class Instructionable extends React.Component {
  // TODO: highlightedArea: bool
  constructor(props) {
    super(props);
    this.registerInsructionable = props.registerInsructionable.bind(this);
  }

  componentDidMount() {
    this.registerInsructionable(this.props.instruction, true);
  }

  componentWillUnmount() {
    this.registerInsructionable(this.props.instruction, false);
  }


  render() {
    // TODO: enforce single child (propTypes, put a class on it?)
    // or on ourserlf but make sure you take the complete area of the children
    const className = `instructionable-${this.props.instruction}`;
    return (
      <span className={className}>
        {this.props.children}
      </span>
    );
  }
}

Instructionable.propTypes = {
  instruction: PropTypes.string.isRequired,
  registerInsructionable: PropTypes.func.isRequired,
};

Instructionable = connect(getProps, actionCreators)(Instructionable);
export default Instructionable;
