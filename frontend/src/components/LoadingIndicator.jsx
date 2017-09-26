import React from 'react';
import RefreshIndicator from 'material-ui/RefreshIndicator';

const wrapperStyle = {
  display: 'inline-block',
  position: 'absolute',
  width: 40,
  height: 40,
  top: 0,
  bottom: 0,
  left: 0,
  right: 0,
  margin: 'auto',
};

const indicatorStyle = {};


export default function LoadingIndicator() {
  return (
    <div style={wrapperStyle}>
      <RefreshIndicator
        size={40}
        left={0}
        top={0}
        status="loading"
        style={indicatorStyle}
      />
    </div>
  );
}
