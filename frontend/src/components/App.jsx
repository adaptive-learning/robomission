import React from 'react';
import PropTypes from 'prop-types';
import backgroundPath from '../images/background-space.png';
import HeaderContainer from '../containers/HeaderContainer';
import MenuContainer from '../containers/MenuContainer';
import InstructionsContainer from '../containers/InstructionsContainer';
import FeedbackModalContainer  from '../containers/FeedbackModalContainer';
import LoginModal from '../components/LoginModal';


const propTypes = {
  children: PropTypes.node,
  showLoginModal: PropTypes.bool.isRequired,
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
        <LoginModal
          open={this.props.showLoginModal}
          credentials={this.props.credentials}
          changeCredentials={this.props.changeCredentials}
          closeLoginModal={this.props.closeLoginModal}
          login={this.props.login}
        />
      </div>
    );
  }
}


App.propTypes = propTypes;
