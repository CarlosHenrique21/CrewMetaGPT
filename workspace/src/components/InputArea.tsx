import React, { ChangeEvent } from 'react';

interface InputAreaProps {
  markdown: string;
  setMarkdown: (value: string) => void;
}

const InputArea: React.FC<InputAreaProps> = ({ markdown, setMarkdown }) => {

  // Handle text input change
  const handleTextChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setMarkdown(e.target.value);
  };

  // Handle file upload (only .md or .markdown files expected)
  const handleFileUpload = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.name.match(/\.md$|\.markdown$/i)) {
        alert('Por favor, insira um arquivo Markdown válido (.md ou .markdown).');
        return;
      }
      const reader = new FileReader();
      reader.onload = () => {
        const text = reader.result;
        if (typeof text === 'string') {
          setMarkdown(text);
        }
      };
      reader.onerror = () => {
        alert('Erro ao ler o arquivo. Tente novamente.');
      };
      reader.readAsText(file);
    }
  };

  return (
    <div className="input-area">
      <label htmlFor="markdown-textarea">Markdown de Entrada:</label>
      <textarea
        id="markdown-textarea"
        value={markdown}
        onChange={handleTextChange}
        rows={15}
        style={{ width: '100%', fontFamily: 'monospace', fontSize: '1rem' }}
        placeholder="Cole seu Markdown aqui ou carregue um arquivo"
      />
      <input
        type="file"
        accept=".md,.markdown"
        onChange={handleFileUpload}
        aria-label="Upload de arquivo Markdown"
      />
    </div>
  );
};

export default InputArea;
