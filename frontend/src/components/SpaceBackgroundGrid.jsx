import React, { PropTypes } from 'react';
import FieldBackground from './FieldBackground';
import spaceBackgroundPath from '../../assets/images/background-space.png';

export default function SpaceBackgroundGrid({ backgroundColors, fieldSize }) {
  const backgroundGridStyle = {
    display: 'table',
    borderCollapse: 'collapse',
    backgroundImage: `url(${spaceBackgroundPath})`,
    backgroundSize: '100% auto',
    backgroundColor: '#112',
  };
  return (
    <span style={backgroundGridStyle} >
      {backgroundColors.map((backgroundsRow, index) =>
        <span style={{ display: 'table-row' }} key={index}>
          {backgroundsRow.map((background, bgIndex) =>
            <FieldBackground key={bgIndex} color={background} size={fieldSize} />
          )}
        </span>
      )}
    </span>
  );
}

SpaceBackgroundGrid.propTypes = {
  backgroundColors: PropTypes.array.isRequired,
  fieldSize: PropTypes.number.isRequired,
};
