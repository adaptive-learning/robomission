import React from 'react';
import PropTypes from 'prop-types';
import muiThemeable from 'material-ui/styles/muiThemeable';
import { Card, CardTitle, CardText } from 'material-ui/Card';
import { LineChart, XAxis, YAxis, Line } from 'recharts';
import { toTitle } from '../utils/text';


class MonitoringPage extends React.Component {
  renderMetricPlot(name) {
    const data = getDataForPlot(this.props.metrics, name);
    return (
      <Card style={{ margin: 10 }} key={name}>
        <CardTitle title={toTitle(name)} />
        <CardText>
          <LineChart width={500} height={300} data={data}>
            <XAxis dataKey="time"/>
            <YAxis/>
            <Line type="monotone" dataKey="value" stroke="#8884d8" />
          </LineChart>
        </CardText>
      </Card>
    );
  }

  renderActiveStudents() {
    return this.renderMetricPlot('active-students');
  }

  renderSolvedCount() {
    return this.renderMetricPlot('solved-count');
  }

  renderSuccessRatio() {
    return this.renderMetricPlot('success-ratio');
  }

  renderSolvingHours() {
    return this.renderMetricPlot('solving-hours');
  }

  renderMetrics() {
    return [
      this.renderActiveStudents(),
      this.renderSolvedCount(),
      this.renderSuccessRatio(),
      this.renderSolvingHours(),
    ];
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
        {metrics && this.renderMetrics()}
      </div>
    );
  }
}

MonitoringPage.propTypes = {
  metrics: PropTypes.array,
};

MonitoringPage.defaultProps = {
};


/**
 * Extract values for given metric name and group and return it in the format
 * required by the recharts library.
 */
function getDataForPlot(metrics, name, group = null) {
  const data = metrics
    .filter(metric => metric.name === name && metric.group === group)
    .map(({ time, value }) => ({ time, value }));  // select only these 2 fields
  return data;
}


MonitoringPage = muiThemeable()(MonitoringPage);
export default MonitoringPage;
