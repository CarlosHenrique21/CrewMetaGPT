import React from 'react';

interface ToolbarProps {
  htmlContent: string;
}

const Toolbar: React.FC<ToolbarProps> = ({ htmlContent }) => {
  // Function to trigger download of HTML file
  const handleExport = () => {
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'output.html';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="toolbar" style={{ margin: '1rem 0' }}>
      <button onClick={handleExport} aria-label="Exportar HTML gerado">Exportar HTML</button>
      {/* Placeholder for future language switching feature */}
      {/* <button disabled>Trocar Idioma (em breve)</button> */}
    </div>
  );
};

export default Toolbar;
