import React from 'react';

type Props = {
  title?: string;
};

const HeaderBar: React.FC<Props> = ({ title = 'Document Title' }) => {
  return (
    <div className="rp-header">
      <div className="rp-header-filename">{title}</div>
    </div>
  );
};

export default HeaderBar;
