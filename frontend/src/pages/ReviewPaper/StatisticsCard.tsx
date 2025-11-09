import React from 'react';

type Group = {
  label: string;
  percent: number;
};

type Props = {
  overall?: number;
  groups?: Group[];
};

const StatisticsCard: React.FC<Props> = ({ overall = 0, groups = [] }) => {
  return (
    <div className="rp-statcard">
      <h3>Overall Statistics</h3>
      <div className="rp-stat-overall">{overall}%</div>
      <ul className="rp-stat-groups">
        {groups.map((g, i) => (
          <li key={i}>
            <span className="rp-stat-item">
              {g.label}: {g.percent}%
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StatisticsCard;
