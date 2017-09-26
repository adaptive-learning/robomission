import React, { PropTypes } from 'react';
import { FormattedMessage } from 'react-intl';

export default function Text({ id }) {
  return (
    <FormattedMessage id={id} />
  );
}


Text.propTypes = {
  id: PropTypes.string.isRequired,
};
