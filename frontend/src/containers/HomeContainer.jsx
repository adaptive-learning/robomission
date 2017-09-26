import React, { PropTypes } from 'react';
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


@connect(state => ({
  spaceWorldDemoSolved: isSpaceWorldDemoSolved(state),
  programDemoSolved: isProgramDemoSolved(state),
  newStudent: isNewStudent(state),
}), { setTaskById })
export default class HomeContainer extends React.Component {
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
