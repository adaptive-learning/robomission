import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import { FormattedMessage } from 'react-intl';
import { Scrollbars } from 'react-custom-scrollbars';
import { Card, CardTitle, CardHeader, CardText } from 'material-ui/Card';
import { GridList, GridTile } from 'material-ui/GridList';
import TaskName from './TaskName';
import Skillometer from './Skillometer';
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
    <Card
      style={{ margin: 10 }}
      initiallyExpanded={recommendation.mission === mission.id}
    >
      <CardHeader
        avatar={<Skillometer skill={mission.skill} text={`${mission.order}`}/>}
        title={`${translate(`mission.${mission.id}`)}`}
        titleStyle={{ fontSize: 20 }}
        subtitle={<FormattedMessage id={`chunk.${mission.chunk}`} />}
        subtitleStyle={{ fontSize: 16 }}
        actAsExpander={true}
        showExpandableButton={true}
      />
      <CardText
        expandable={true}
      >
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
    if (phase.id === recommendation.phase) {
      return theme.palette.primary3Color;
    }
    return '#888';
  };

  const getSubtitle = task => {
    if (task.id === recommendation.task) {
      return translate('recommended');
    }
    return formatSolvingTime(task.time);
  };

  const sorted = tasks => {
    // 1: solved, 2: recommended, 3: other tasks
    const compareTasks = (a, b) => {
      const keyA = [!a.solved, a.id !== recommendation.task, a.id];
      const keyB = [!b.solved, b.id !== recommendation.task, b.id];
      return keyA > keyB ? 1 : -1;
    };
    return tasks.sort(compareTasks);
  }

  const tasks = sorted(phase.tasks);
  // TODO: Nicer scrollbars.
  return (
      <div style={{
        margin: 7,
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-around',
        borderStyle: 'solid',
        borderWidth: 1,
        borderColor: '#535353',
      }}>
        <span style={{
          marginLeft: 10,
          marginRight: 10,
          marginTop: 40,
          display: 'inline-block'
        }}>
          <Skillometer skill={phase.skill} text={`${phase.index}`} />
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
