import React from 'react';
import PropTypes from 'prop-types';
import { Card, CardTitle, CardText } from 'material-ui/Card';


export default function MonitoringPage({ metrics }) {
  return (
    <div>
      <Card style={{ margin: 10 }}>
        <CardTitle
          title="Active Users"
        />
        <CardText>
          TBA
        </CardText>
      </Card>
    </div>
  );
}

MonitoringPage.propTypes = {
  metrics: PropTypes.object,
};

MonitoringPage.defaultProps = {
};
