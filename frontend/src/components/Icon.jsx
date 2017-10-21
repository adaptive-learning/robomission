import React, { PropTypes } from 'react';
import Image from './Image';

export default function Icon({ name, style }) {
  const iconStyle = {
    height: '1em',
    position: 'relative',
    top: '0.1em',
    ...style,
  };

  return (
    <Image imageId={`icon-${name}.svg`} style={iconStyle} />
  );
}

Icon.propTypes = {
  name: PropTypes.string.isRequired,
  style: PropTypes.object,
};

Icon.defaultProps = {
  style: {},
};
