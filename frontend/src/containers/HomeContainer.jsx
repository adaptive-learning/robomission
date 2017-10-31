import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Home from '../components/Home';
import { setTaskById } from '../actions/taskEnvironment';
import { isNewStudent } from '../selectors/student';
import { isSpaceWorldDemoSolved, isProgramDemoSolved } from '../selectors/home';


const propTypes = {
  spaceWorldDemoSolved: PropTypes.bool,
  programDemoSolved: PropTypes.bool,
  newStudent: PropTypes.bool,
  setTaskById: PropTypes.func,
};

const getProps = state => ({
  spaceWorldDemoSolved: isSpaceWorldDemoSolved(state),
  programDemoSolved: isProgramDemoSolved(state),
  newStudent: isNewStudent(state),
});

const actionCreators = { setTaskById };

class HomeContainer extends React.Component {
  componentDidMount() {
    this.props.setTaskById('home-commands', 'beware-of-asteroid');
    this.props.setTaskById('home-program', 'three-steps-forward');
  }

  render() {
    return (
      <Home
        spaceWorldDemoSolved={this.props.spaceWorldDemoSolved}
        programDemoSolved={this.props.programDemoSolved}
        newStudent={this.props.newStudent}
      />
    );
  }
}

HomeContainer.propTypes = propTypes;
HomeContainer = connect(getProps, actionCreators)(HomeContainer);

export default HomeContainer;
