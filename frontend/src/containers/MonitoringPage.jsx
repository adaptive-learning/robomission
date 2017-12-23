import React from 'react';
import { connect } from 'react-redux';
import MonitoringPageComponent from '../components/MonitoringPage';
import { fetchMetrics } from '../actions/monitoring';
import { getMetrics } from '../selectors/monitoring';


function getProps(state) {
  return {
    metrics: getMetrics(state),
  };
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
      <MonitoringPageComponent
        metrics={this.props.metrics}
      />
    );
  }
}

MonitoringPage = connect(getProps, actionCreators)(MonitoringPage);

export default MonitoringPage;
