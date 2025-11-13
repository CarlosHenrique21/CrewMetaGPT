import React from 'react';

interface OutputAreaProps {
  html: string;
}

const OutputArea: React.FC<OutputAreaProps> = ({ html }) => {
  return (
    <div className="output-area" style={{ border: '1px solid #ccc', padding: '1rem', marginTop: '1rem', overflowY: 'auto', height: '350px' }}>
      <h2>Visualização HTML</h2>
      {/* Render sanitized HTML output */}
      <div dangerouslySetInnerHTML={{ __html: html }} />
    </div>
  );
};

export default OutputArea;
