import React, { PropTypes } from 'react';

export default function Image({ imageId, style, ...otherProps }) {
  // default extension is 'png'
  const name = imageId.includes('.') ? imageId : `${imageId}.png`;
  // eslint-disable-next-line global-require
  const sourcePath = require(`../../assets/images/${name}`);
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
