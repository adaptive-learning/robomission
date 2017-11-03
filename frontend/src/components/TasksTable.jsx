import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import { FormattedMessage } from 'react-intl';
import { Card, CardTitle, CardText } from 'material-ui/Card';
import { GridList, GridTile } from 'material-ui/GridList';
import TaskName from './TaskName';
import { theme } from '../theme';
import { translate } from '../localization';


export default function TaskTable({ urlBase, tasksInCategories, recommendation }) {
  return (
    <div>
      { tasksInCategories.map(({ category, tasks }) =>
        <CategoryTasks
          key={category.id}
          urlBase={urlBase}
          category={category}
          tasks={tasks}
          recommendation={recommendation}
        />)
      }
    </div>
  );
}

TaskTable.propTypes = {
  urlBase: PropTypes.string,
  tasksInCategories: PropTypes.array.isRequired,
  recommendation: PropTypes.object.isRequired,
};

TaskTable.defaultProps = {
  urlBase: '/task/',
};


function CategoryTasks({ category, tasks, urlBase, recommendation }) {
  if (tasks.length === 0) {
    return null;
  }

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

  return (
    <Card style={{ margin: 10 }}>
      <CardTitle
        title={<FormattedMessage id={`category.${category.id}`} />}
        subtitle={`Level ${category.level}`}
      />
      <CardText>
        <GridList
          cellHeight={120}
          cols={Math.min(5, Math.floor(window.innerWidth / 300))}
          style={{
            display: 'flex',
            flexWrap: 'wrap',
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
                    width: '100%',
                    height: '100%',
                  }}
                />
              </GridTile>
            </Link>
          ))}
        </GridList>
      </CardText>
    </Card>
  );
}


CategoryTasks.propTypes = {
  category: PropTypes.object.isRequired,
  tasks: PropTypes.array.isRequired,
  urlBase: PropTypes.string,
  recommendation: PropTypes.object.isRequired,
};


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
