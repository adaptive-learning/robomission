import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import { FormattedMessage } from 'react-intl';
import Avatar from 'material-ui/Avatar';
import { Card, CardTitle, CardText } from 'material-ui/Card';
import { GridList, GridTile } from 'material-ui/GridList';
import TaskName from './TaskName';
import { theme } from '../theme';
import { translate } from '../localization';


export default function TaskTable({ urlBase, missions, recommendation }) {
  return (
    <div>
      { missions.map(mission =>
        <MissionOverview
          key={mission.id}
          urlBase={urlBase}
          mission={mission}
          recommendation={recommendation}
        />)
      }
    </div>
  );
}

TaskTable.propTypes = {
  urlBase: PropTypes.string,
  missions: PropTypes.array.isRequired,
  recommendation: PropTypes.object.isRequired,
};

TaskTable.defaultProps = {
  urlBase: '/task/',
};


function MissionOverview({ mission, urlBase, recommendation }) {
  return (
    <Card style={{ margin: 10 }}>
      <CardTitle
        title={`${mission.order}. ${translate(`mission.${mission.id}`)}`}
        subtitle={<FormattedMessage id={`chunk.${mission.chunk}`} />}
      />
      <CardText>
      {mission.phases.map(phase => (
        <Phase
          key={phase.id}
          urlBase={urlBase}
          phase={phase}
          recommendation={recommendation}
        />))}
      </CardText>
    </Card>
  );
}


MissionOverview.propTypes = {
  mission: PropTypes.object.isRequired,
  urlBase: PropTypes.string,
  recommendation: PropTypes.object.isRequired,
};


function Phase({ phase, urlBase, recommendation }) {
  const chooseBackgroundColor = task => {
    if (task.id === recommendation.task) {
      return theme.palette.accent2Color;
    }
    if (task.solved) {
      return theme.palette.successColor;
    }
    return theme.palette.primary3Color;
  };

  const getSubtitle = task => {
    if (task.id === recommendation.task) {
      return translate('recommended');
    }
    return formatSolvingTime(task.time);
  };

  const { tasks } = phase;
  return (
    <div style={{
      margin: 7,
      display: 'flex',
      flexWrap: 'wrap',
      justifyContent: 'space-around',
    }}>
      <span style={{
        marginRight: 10,
        marginTop: 40,
        display: 'inline-block'
      }}>
        <Avatar>
          {phase.index}
        </Avatar>
      </span>
      <GridList
        cellHeight={120}
        rows={1}
        cols={window.innerWidth / 250}
        style={{
          width: '100%',
          display: 'flex',
          flexWrap: 'nowrap',
          overflowX: 'auto',
          flex: 1,
        }}
      >
        {tasks.map((task) => (
          <Link key={task.id} to={`${urlBase}${task.id}`}>
            <GridTile
              title={<TaskName taskId={task.id} />}
              subtitle={getSubtitle(task)}
            >
              <div
                style={{
                  backgroundColor: chooseBackgroundColor(task),
                  width: 250,
                  height: '100%',
                }}
              />
            </GridTile>
          </Link>
        ))}
      </GridList>
    </div>
  );
}


function formatSolvingTime(time) {
  // assumes time as a number of seconds
  if (time == null) {
    return translate('not tackled');
  }
  const minutes = Math.floor(time / 60);
  const seconds = time % 60;
  const paddedSeconds = ('0' + seconds).slice(-2);
  return `${minutes}:${paddedSeconds}`;
}
