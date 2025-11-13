import React, { useState, useEffect } from 'react';
import InputArea from './components/InputArea';
import OutputArea from './components/OutputArea';
import Toolbar from './components/Toolbar';
import { parseMarkdownToHtml } from './utils/parser';

const App: React.FC = () => {
  // State holding Markdown input text
  const [markdown, setMarkdown] = useState<string>('');
  // State holding sanitized HTML output
  const [html, setHtml] = useState<string>('');

  useEffect(() => {
    try {
      // Parse and sanitize Markdown when input changes
      const parsed = parseMarkdownToHtml(markdown);
      setHtml(parsed);
    } catch (error) {
      // Basic error handling: show error in output
      setHtml('<p><strong>Erro na conversão do Markdown.</strong></p>');
      console.error('Erro ao converter Markdown para HTML:', error);
    }
  }, [markdown]);

  return (
    <div style={{ maxWidth: '900px', margin: 'auto', padding: '1rem' }}>
      <h1>Conversor Markdown para HTML</h1>
      <Toolbar htmlContent={html} />
      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        <div style={{ flex: 1, minWidth: '300px' }}>
          <InputArea markdown={markdown} setMarkdown={setMarkdown} />
        </div>
        <div style={{ flex: 1, minWidth: '300px' }}>
          <OutputArea html={html} />
        </div>
      </div>
    </div>
  );
};

export default App;
