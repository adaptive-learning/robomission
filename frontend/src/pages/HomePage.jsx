import React from 'react';
import { connect } from 'react-redux';
//import HomeContainer from '../containers/HomeContainer';


function getProps(state, props) {
  return {};
}

class HomePage extends React.Component {
  render() {
    return (
      <h1>home page</h1>
    );
    /*
    return (
      <HomeContainer />
    );
    */
  }
}

HomePage = connect(getProps)(HomePage);

export default HomePage;
