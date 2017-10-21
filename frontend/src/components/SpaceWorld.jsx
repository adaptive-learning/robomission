import React, { PropTypes } from 'react';
import GameObject from './GameObject';
import SpaceBackgroundGrid from './SpaceBackgroundGrid';

export default function SpaceWorld({ fields, width }) {
  const { cols, backgrounds, objects } = prepareFields(fields);
  const fieldSize = width / cols;
  // const height = fieldSize * rows;
  const worldStyle = {
    display: 'block',
    position: 'relative',
  };
  return (
    <span className="instructionable-env-space-world" style={worldStyle}>
      <SpaceBackgroundGrid backgroundColors={backgrounds} fieldSize={fieldSize} />
      <span>
        {objects.map((object, index) =>
          <GameObject
            key={index}
            imageId={object.imageId}
            width={fieldSize}
            height={fieldSize}
            position="absolute"
            bottom={object.row * fieldSize}
            left={object.col * fieldSize}
          />
        )}
      </span>
    </span>
  );
}

SpaceWorld.propTypes = {
  fields: PropTypes.array.isRequired,
  width: PropTypes.number,
};


SpaceWorld.defaultProps = {
  width: 280,
};


const IMAGE_TYPES = {
  S: 'spaceship',
  A: 'asteroid',
  M: 'meteoroid',
  D: 'diamond',
  W: 'wormhole',
  X: 'wormhole2',
  Y: 'wormhole3',
  Z: 'wormhole4',
  explosion: 'explosion',
  laser: 'laser',
  'laser-start': 'laser-start',
  'laser-end': 'laser-end',
  'spaceship-broken': 'spaceship-broken',
  'spaceship-out-left': 'spaceship-out-left',
  'spaceship-out-right': 'spaceship-out-right',
  'spaceship-out-top': 'spaceship-out-top',
};


const emptyWorld = {
  rows: 1,
  cols: 1,
  backgrounds: [['k']],
  objects: [],
};


function prepareFields(fields) {
  if (fields == null || fields.length === 0) {
    return emptyWorld;
  }
  const rows = fields.length;
  const cols = fields[0].length;
  const backgrounds = fields.map(row => row.map(field => field[0]));
  const objects = [];
  fields.forEach((row, i) => row.forEach((field, j) => field[1].forEach(object => {
    objects.push({ imageId: IMAGE_TYPES[object], row: rows - i - 1, col: j });
  })));
  return { rows, cols, backgrounds, objects };
}
