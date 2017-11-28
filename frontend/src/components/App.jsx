import React from 'react';
import PropTypes from 'prop-types';
import backgroundPath from '../images/background-space.png';
import HeaderContainer from '../containers/HeaderContainer';
import MenuContainer from '../containers/MenuContainer';
import InstructionsContainer from '../containers/InstructionsContainer';
import FeedbackModalContainer  from '../containers/FeedbackModalContainer';

const propTypes = {
  children: PropTypes.node,
};

export default class App extends React.Component {
  render() {
    return (
      <div
        style={{
          backgroundImage: `url(${backgroundPath})`,
          backgroundSize: '500px auto',
          backgroundColor: '#111122',
          paddingBottom: 25,
          overflowX: 'hidden',
        }}
      >
        <InstructionsContainer />
        <HeaderContainer />
        <MenuContainer />
        { this.props.children }
        <FeedbackModalContainer />
      </div>
    );
  }
}


App.propTypes = propTypes;
