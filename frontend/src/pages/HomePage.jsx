import React from 'react';
import { connect } from 'react-redux';
import HomeContainer from '../containers/HomeContainer';


function getProps(state, props) {
  return {};
}

@connect(getProps, {})
export default class HomePage extends React.Component {
  render() {
    return (
      <HomeContainer />
    );
  }
}
