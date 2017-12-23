import React from 'react';
import { connect } from 'react-redux';
import MonitoringPageComponent from '../components/MonitoringPage';


function getProps(state) {
  return {
  };
}

const actionCreators = {
};

class MonitoringPage extends React.Component {
  render() {
    return (
      <MonitoringPageComponent />
    );
  }
}

MonitoringPage = connect(getProps, actionCreators)(MonitoringPage);

export default MonitoringPage;
