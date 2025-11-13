import React from 'react';
import DOMPurify from 'dompurify';

/**
 * HtmlViewer - safe render HTML content
 * Props:
 *  - html: string (HTML content to display)
 */

const HtmlViewer = ({ html }) => {
  const cleanHtml = DOMPurify.sanitize(html || '');

  return (
    <div
      aria-label="Visualizador HTML"
      style={{ border: '1px solid #ccc', padding: '1rem', minHeight: '300px', overflowY: 'auto', backgroundColor: '#fafafa' }}
      dangerouslySetInnerHTML={{ __html: cleanHtml }}
    />
  );
};

export default HtmlViewer;
