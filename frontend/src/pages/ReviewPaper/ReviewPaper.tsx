import React from 'react';
import { useParams } from 'react-router-dom';
import HeaderBar from './HeaderBar';
import PdfViewer from './PdfViewer';
import StatisticsCard from './StatisticsCard';
import SourcesList from './SourcesList';
import { mockHeader, mockPdf, mockStatistics, mockSources } from './mockData';
import './ReviewPaper.css';

const ReviewPaper: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  return (
    <div className="rp-container">
      <HeaderBar title={mockHeader.title} />

      <div className="rp-main">
        <div className="rp-pdf">
          <PdfViewer
            pages={mockPdf.pages}
            words={mockPdf.words}
            imageSrc="/samplePdf.png"
          />
        </div>

        <aside className="rp-sidebar">
          <StatisticsCard
            overall={mockStatistics.overall}
            groups={mockStatistics.groups}
          />
          <SourcesList items={mockSources} />
        </aside>
      </div>

      <div style={{ marginTop: 8, fontSize: 12, color: '#666' }}>
        Paper ID: {id ?? 'unknown'}
      </div>
    </div>
  );
};

export default ReviewPaper;
