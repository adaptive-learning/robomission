import React from 'react';
import PropTypes from 'prop-types';
import muiThemeable from 'material-ui/styles/muiThemeable';
import { Card, CardTitle, CardText } from 'material-ui/Card';
import {
  LineChart, XAxis, YAxis, Line, Bar, BarChart,
  CartesianGrid, Tooltip } from 'recharts';
import { toTitle } from '../utils/text';
import { theme } from '../theme';


class RotatedAxisTick extends React.Component {
  render () {
    const {x, y, payload} = this.props;
    return (
      <g transform={`translate(${x - 11},${y})`}>
        <text
          x={0} y={0} dy={16}
          textAnchor="end"
          fill="#666"
          transform="rotate(-90)"
        >
          {payload.value}
        </text>
      </g>
    );
  }
}

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
            <Line type="monotone" dataKey="value" stroke={theme.palette.primary2Color} />
          </LineChart>
        </CardText>
      </Card>
    );
  }

  renderTaskMetricPlot(name) {
    const data = getDataForTasksPlot(this.props.metrics, name);
    return (
      <Card style={{ margin: 10 }} key={`tasks-${name}`}>
        <CardTitle title={`${toTitle(name)} for Tasks`} />
        <CardText>
          <BarChart width={1000} height={400} data={data}>
            <CartesianGrid stroke="#ccc" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="name" tick={<RotatedAxisTick />} interval={0} height={200} />
            <YAxis allowDecimals={false} />
            <Tooltip labelStyle={{ color: '#555' }} />
            <Bar dataKey="value" fill={theme.palette.primary2Color} />
          </BarChart>
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

  renderSolvedCountsForTasks() {
    return this.renderTaskMetricPlot('solved-count');
  }

  renderMetrics() {
    return [
      this.renderActiveStudents(),
      this.renderSolvedCount(),
      this.renderSuccessRatio(),
      this.renderSolvingHours(),
      this.renderSolvedCountsForTasks(),
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


function getDataForTasksPlot(metrics, name) {
  const data = metrics
    .filter(metric => metric.name === name && metric.group !== null)
    .map(({ group, value }) => ({ name: group.split('.', 2)[1], value }))
    .sort((a, b) => (b.value - a.value));
  return data;
}


MonitoringPage = muiThemeable()(MonitoringPage);
export default MonitoringPage;
