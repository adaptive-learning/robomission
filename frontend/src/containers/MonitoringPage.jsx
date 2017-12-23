import React from 'react';
import { connect } from 'react-redux';
import muiThemeable from 'material-ui/styles/muiThemeable';
import MonitoringPageComponent from '../components/MonitoringPage';


function getProps(state) {
  return {
  };
}

const actionCreators = {
};

class MonitoringPage extends React.Component {
  render() {
    // TODO: move styling to a component
    const longPageContentStyle = {
      maxWidth: 1200,
      margin: '20px auto',
      backgroundColor: this.props.muiTheme.palette.canvasColor,
    };
    return (
      <div style={longPageContentStyle}>
        <MonitoringPageComponent />
      </div>
    );
  }
}

MonitoringPage = muiThemeable()(MonitoringPage);
MonitoringPage = connect(getProps, actionCreators)(MonitoringPage);

export default MonitoringPage;
