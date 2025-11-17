import React from 'react';

type Props = {
  pages?: number;
  words?: number;
  imageSrc?: string;
};

const PdfViewer: React.FC<Props> = ({ pages = 0, words = 0, imageSrc }) => {
  return (
    <div className="rp-pdfviewer">
      {imageSrc ? (
        <img className="rp-pdf-image" src={imageSrc} alt="Document preview" />
      ) : (
        <div className="rp-pdf-placeholder">PDF viewer placeholder</div>
      )}

      <div className="rp-pdf-meta">
        {pages} pages — {words} words
      </div>
    </div>
  );
};

export default PdfViewer;
