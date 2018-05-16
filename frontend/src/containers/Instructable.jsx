import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { registerInstructable } from '../actions';


const getProps = state => ({
});


const actionCreators = {
  registerInstructable,
};


const addClass = (component, className) => {
  const originalClasses = component.props.className ? ` ${component.props.className}` : '';
  return React.cloneElement(component, {
    className: className + originalClasses,
  });
}


class Instructable extends React.Component {
  // TODO: highlightedArea: bool + onClick (only when highlighted)
  constructor(props) {
    super(props);
    this.registerInstructable = props.registerInstructable.bind(this);
  }

  componentDidMount() {
    this.registerInstructable(this.props.instruction, true, this.props.position);
  }

  componentWillUnmount() {
    this.registerInstructable(this.props.instruction, false);
  }


  render() {
    // TODO: Get the class name via props from store (to make sure they are
    // in sync.
    const className = `instructable-${this.props.instruction}`;
    const child = React.Children.only(this.props.children);
    return addClass(child, className);
  }
}

Instructable.propTypes = {
  instruction: PropTypes.string.isRequired,
  position: PropTypes.string,
  registerInstructable: PropTypes.func.isRequired,
  children: PropTypes.element.isRequired,
};


Instructable.defaultProps = {
  position: 'auto',
};

Instructable = connect(getProps, actionCreators)(Instructable);
export default Instructable;
