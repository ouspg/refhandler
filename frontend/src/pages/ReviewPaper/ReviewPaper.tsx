import React from 'react';
import { useParams } from 'react-router-dom';

const ReviewPaper: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  return (
    <div>
      <h1>Review paper page</h1>
      <p>Paper ID: {id ?? 'unknown'}</p>
    </div>
  );
};

export default ReviewPaper;
