import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import { FormattedMessage } from 'react-intl';
import Avatar from 'material-ui/Avatar';
import { Card, CardHeader, CardText } from 'material-ui/Card';
import { GridList, GridTile } from 'material-ui/GridList';
import TaskName from './TaskName';
import Rating from './Rating';
import { theme } from '../theme';
import { translate } from '../localization';
import { flatten } from '../utils/arrays';


export default function TaskTable({ urlBase, missions, recommendation }) {
  return (
    <div style={{paddingBottom: 10}}>
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
  const tasks = flatten(mission.phases.map(phase => phase.tasks));
  const isRecommended = recommendation.mission === mission.id
  let badgeTextColor = theme.palette.canvasColor;
  let badgeBackgroundColor = theme.palette.disabledColor;
  if (isRecommended) {
    badgeTextColor = theme.palette.accent2Color;
  } else if (mission.level < recommendation.levels[0]) {
    // TODO: Use explicit student.mission/phase info instead of recommendation.
    badgeBackgroundColor = theme.palette.successColor;
  }
  return (
    <Card
      style={{ margin: 10 }}
      initiallyExpanded={isRecommended}
    >
      <CardHeader
        avatar={
          <Avatar
            color={badgeTextColor}
            backgroundColor={badgeBackgroundColor}
          >
            L{mission.level}
          </Avatar>}
        title={`${translate(`ps.story.${mission.id}`)}`}
        titleStyle={{
          fontSize: 20 }}
          //color: isRecommended ? theme.palette.accent2Color : null}}
        subtitle={<FormattedMessage id={`ps.${mission.id}`} />}
        subtitleStyle={{ fontSize: 16 }}
        subtitle={<FormattedMessage id={`ps.${mission.id}`} />}
        actAsExpander={true}
        showExpandableButton={true}
      />
      <CardText
        expandable={true}
      >
        <div style={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'space-around',
          //borderStyle: 'solid',
          //borderWidth: 1,
          //borderColor: '#535353',
        }}>
          <GridList
            cellHeight={120}
            rows={1}
            // Hack to determine number of columns. TODO: unhack (also make it
            // respond to screen size changes.
            cols={Math.min(5, Math.ceil(window.innerWidth / 250))}
            style={{
              width: '100%',
            }}
          >
            {tasks.map(task => (
              <TaskTile
                key={task.id}
                urlBase={urlBase}
                task={task}
                recommendation={recommendation}
              />))}
          </GridList>
        </div>
      </CardText>
    </Card>
  );
}


MissionOverview.propTypes = {
  mission: PropTypes.object.isRequired,
  urlBase: PropTypes.string,
  recommendation: PropTypes.object.isRequired,
};


function TaskTile({ task, urlBase, recommendation }) {
  let background = '#888';
  if (task.id === recommendation.task) {
    background = theme.palette.accent2Color;
  } else if (task.solved) {
    background = theme.palette.successColor;
  } else if (task.problemSet === recommendation.phase) {
    background = '#ddd';
  }

  let subtitle = '';
  if (task.id === recommendation.task) {
    subtitle = translate('recommended');
  } else {
    // TODO: Add explicit branch for task.solved/unsolved
    subtitle = formatSolvingTime(task.time);
  };

  return (
    <Link key={task.id} to={`${urlBase}${task.id}`}>
      <GridTile
        title={<TaskName taskId={task.id} />}
        subtitle={subtitle}
      >
        <div
          style={{
            backgroundColor: background,
            //width: 250,
            height: '100%',
            padding: '15px 10px',
          }}
        >
          <Rating value={task.solved ? task.levels[1] : 0} max={task.levels[1]} />
        </div>
      </GridTile>
    </Link>
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
