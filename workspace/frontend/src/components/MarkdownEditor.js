import React from 'react';

/**
 * MarkdownEditor - controlled textarea input component for markdown text
 * Props:
 *  - value: string (markdown text)
 *  - onChange: function(event) callback
 */

const MarkdownEditor = ({ value, onChange }) => {
  return (
    <textarea
      value={value}
      onChange={onChange}
      placeholder="Insira seu texto Markdown aqui..."
      style={{ width: '100%', height: '300px', fontFamily: 'monospace', fontSize: '1rem' }}
      aria-label="Editor Markdown"
    />
  );
};

export default MarkdownEditor;
