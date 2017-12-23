import React from 'react';
import PropTypes from 'prop-types';
import muiThemeable from 'material-ui/styles/muiThemeable';
import { Card, CardTitle, CardText } from 'material-ui/Card';


class MonitoringPage extends React.Component {

  renderActiveUsers() {
    return (
      <Card style={{ margin: 10 }}>
        <CardTitle
          title="Active Users"
        />
        <CardText>
          TBA
        </CardText>
      </Card>
    );
  }

  render() {
    const { metrics, muiTheme } = this.props;
    // TODO: factor out longPageStyle (used in other pages as well)
    const longPageContentStyle = {
      maxWidth: 1200,
      margin: '20px auto',
      backgroundColor: muiTheme.palette.canvasColor,
    };
    return (
      <div style={longPageContentStyle}>
        {this.renderActiveUsers()}
      </div>
    );
  }
}

MonitoringPage.propTypes = {
  metrics: PropTypes.object,
};

MonitoringPage.defaultProps = {
};

MonitoringPage = muiThemeable()(MonitoringPage);
export default MonitoringPage;
