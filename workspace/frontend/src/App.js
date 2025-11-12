import React, { useState, useEffect } from 'react';
import MarkdownEditor from './components/MarkdownEditor';
import HtmlViewer from './components/HtmlViewer';
import MarkdownIt from 'markdown-it';
import DOMPurify from 'dompurify';

const mdParser = new MarkdownIt({ html: false, linkify: true, typographer: true });

const App = () => {
  const [markdown, setMarkdown] = useState('');
  const [html, setHtml] = useState('');

  useEffect(() => {
    const rendered = mdParser.render(markdown);
    const clean = DOMPurify.sanitize(rendered);
    setHtml(clean);
  }, [markdown]);

  const handleChange = (e) => {
    setMarkdown(e.target.value);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(html)
      .then(() => alert('HTML copiado para a área de transferência!'))
      .catch(() => alert('Falha ao copiar o HTML.'));
  };

  const handleExport = () => {
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'converted.html';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ maxWidth: '960px', margin: '1rem auto', fontFamily: 'Arial, sans-serif' }}>
      <h1>Conversor Markdown para HTML</h1>
      <div style={{ display: 'flex', gap: '1rem' }}>
        <div style={{ flex: 1 }}>
          <h2>Editor Markdown</h2>
          <MarkdownEditor value={markdown} onChange={handleChange} />
        </div>
        <div style={{ flex: 1 }}>
          <h2>Visualizador HTML</h2>
          <HtmlViewer html={html} />
          <div style={{ marginTop: '1rem' }}>
            <button onClick={handleCopy} style={{ marginRight: '0.5rem' }}>Copiar HTML</button>
            <button onClick={handleExport}>Exportar HTML</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
