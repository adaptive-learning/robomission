import React from 'react';
import PropTypes from 'prop-types';

export default function Image({ imageId, style, ...otherProps }) {
  // default extension is 'png'
  const name = imageId.includes('.') ? imageId : `${imageId}.png`;
  // eslint-disable-next-line global-require
  const sourcePath = require(`../images/${name}`);
  return (
    <img src={sourcePath} alt={imageId} style={style} {...otherProps} />
  );
}

Image.propTypes = {
  imageId: PropTypes.string.isRequired,
  style: PropTypes.object,
};

Image.defaultProps = {
  style: {},
};
