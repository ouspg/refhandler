import React from 'react';

export type SourceItem = {
  id: string | number;
  type: string;
  title: string;
  matchedWords: number;
  percent?: number;
};

type Props = {
  items?: SourceItem[];
};

const SourcesList: React.FC<Props> = ({ items = [] }) => {
  return (
    <div className="rp-sources">
      <h4>Detections</h4>
      <ul>
        {items.map((item) => (
          <li key={item.id} className="rp-source-item">
            <div className="rp-source-title">{item.title}</div>
            <div className="rp-source-meta">
              {item.type} — {item.matchedWords} matched words
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SourcesList;
