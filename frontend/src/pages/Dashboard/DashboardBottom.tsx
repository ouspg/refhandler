import React from 'react';
import './DashboardBottom.css';

const RecentPapers: React.FC = () => {
  const papers = [
    {
      id: 'p1',
      title: 'Machine Learning Thesis 2024.pdf',
      size: '2.4 MB',
      citations: 67,
      timeAgo: '2 hours ago',
    },
    {
      id: 'p2',
      title: 'Climate Change Research.pdf',
      size: '1.8 MB',
      citations: 89,
      timeAgo: '5 hours ago',
    },
    {
      id: 'p3',
      title: 'Quantum Computing Paper.pdf',
      size: '1.2 MB',
      citations: 45,
      timeAgo: '1 day ago',
    },
    {
      id: 'p4',
      title: 'Neuroscience Study.pdf',
      size: '892 KB',
      citations: 34,
      timeAgo: '2 days ago',
    },
  ];

  return (
    <div className="dashboard-top-container">
      <h3>Recent Papers</h3>
      <div className="file-list">
        {papers.map((p) => (
          <div key={p.id} className="file-item">
            <div className="item-icon" aria-hidden>
              {/* simple document icon */}
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z"
                  stroke="#0b5fff"
                  strokeWidth="1.2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M14 2v6h6"
                  stroke="#0b5fff"
                  strokeWidth="1.2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div className="file-name">{p.title}</div>
              <div className="meta-line">
                {p.size} • {p.citations} citations • {p.timeAgo}
              </div>
            </div>

            <div className="paper-actions">
              <button
                className="icon-button"
                aria-label={`view-${p.id}`}
                title="View"
              >
                {/* eye icon */}
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"
                    stroke="#374151"
                    strokeWidth="1.2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <circle
                    cx="12"
                    cy="12"
                    r="3"
                    stroke="#374151"
                    strokeWidth="1.2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </button>
              <button
                className="icon-button"
                aria-label={`download-${p.id}`}
                title="Download"
              >
                {/* download icon */}
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"
                    stroke="#374151"
                    strokeWidth="1.2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M7 10l5 5 5-5"
                    stroke="#374151"
                    strokeWidth="1.2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M12 15V3"
                    stroke="#374151"
                    strokeWidth="1.2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </button>
              <button
                className="icon-button"
                aria-label={`more-${p.id}`}
                title="More"
              >
                {/* kebab */}
                <svg
                  width="12"
                  height="12"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <circle cx="12" cy="5" r="1.5" fill="#374151" />
                  <circle cx="12" cy="12" r="1.5" fill="#374151" />
                  <circle cx="12" cy="19" r="1.5" fill="#374151" />
                </svg>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const FrequentlyCited: React.FC = () => {
  const sources = [
    {
      id: 's1',
      title: 'Chen, L. & Wang, Y. (2023). Quantum Computing Applications',
      count: 8,
      journal: 'Physical Review Letters',
      trending: false,
    },
    {
      id: 's2',
      title: 'Brown, A. (2021). Neural Network Architectures',
      count: 7,
      journal: 'IEEE Transactions',
      trending: false,
    },
    {
      id: 's3',
      title: 'Davis, R. et al. (2023). Ethical AI Frameworks',
      count: 6,
      journal: 'AI & Society',
      trending: true,
    },
  ];

  return (
    <div className="dashboard-right">
      <h3>Frequently Cited Sources</h3>
      <ul style={{ listStyle: 'none', padding: 0, marginTop: 8 }}>
        {sources.map((s) => (
          <li
            key={s.id}
            style={{
              padding: '12px 0',
              borderBottom: '1px solid #f3f4f6',
              display: 'flex',
              gap: 12,
              alignItems: 'center',
            }}
          >
            <div className="item-icon" aria-hidden>
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M4 19.5A2 2 0 0 1 6 18h12a2 2 0 0 1 2 1.5V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v13.5z"
                  stroke="#0b5fff"
                  strokeWidth="1.2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M8 6h8"
                  stroke="#0b5fff"
                  strokeWidth="1.2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontSize: 14, fontWeight: 600 }}>{s.title}</div>
              <div style={{ color: '#9ca3af', fontSize: 13, marginTop: 6 }}>
                {s.journal || 'Unknown source'}
              </div>
              <div style={{ marginTop: 8 }}>
                <span className="source-badge">Used in {s.count} papers</span>
                {s.trending ? (
                  <span
                    style={{ marginLeft: 8, color: '#0b5fff', fontSize: 13 }}
                  >
                    ↗ Trending
                  </span>
                ) : null}
              </div>
            </div>
            <div style={{ marginLeft: '8px' }}>
              <button
                className="icon-button"
                aria-label={`view-source-${s.id}`}
                title="View source"
              >
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"
                    stroke="#374151"
                    strokeWidth="1.2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <circle
                    cx="12"
                    cy="12"
                    r="3"
                    stroke="#374151"
                    strokeWidth="1.2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

const DashboardBottom: React.FC = () => (
  <div className="dashboard-bottom" style={{ display: 'flex', gap: 16 }}>
    <div className="dashboard-left-column">
      <RecentPapers />
    </div>
    <div className="dashboard-right-column">
      <FrequentlyCited />
    </div>
  </div>
);

export default DashboardBottom;
