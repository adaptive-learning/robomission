import React from 'react';
import { connect } from 'react-redux';
import MonitoringPageComponent from '../components/MonitoringPage';
import { fetchMetrics } from '../actions/monitoring';


function getProps(state) {
  return {};
}

const actionCreators = {
  fetchMetrics: fetchMetrics.request,
};

class MonitoringPage extends React.Component {
  componentDidMount() {
    this.props.fetchMetrics();
  }

  render() {
    return (
      <MonitoringPageComponent />
    );
  }
}

MonitoringPage = connect(getProps, actionCreators)(MonitoringPage);

export default MonitoringPage;
