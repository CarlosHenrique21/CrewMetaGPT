// src/App.jsx

import React, { useState } from 'react';
import ConverterService from './services/ConverterService';
import MarkdownInput from './components/MarkdownInput';
import HtmlOutput from './components/HtmlOutput';
import PreviewButton from './components/PreviewButton';

/**
 * Main application component for the Markdown to HTML Converter.
 */
const App = () => {
    const [markdown, setMarkdown] = useState(''); // State to hold markdown input
    const [htmlOutput, setHtmlOutput] = useState(''); // State to hold converted HTML
    const converterService = new ConverterService(); // Instantiate the converter service

    /**
     * Handles the conversion of Markdown to HTML.
     */
    const handleConvert = () => {
        try {
            const html = converterService.convert(markdown); // Convert markdown to HTML
            setHtmlOutput(html); // Update state with converted HTML
        } catch (error) {
            alert(error.message); // Alert user in case of error
        }
    };

    return (
        <div>
            <h1>Markdown to HTML Converter</h1>
            <MarkdownInput markdown={markdown} setMarkdown={setMarkdown} />
            <PreviewButton onClick={handleConvert} />
            <HtmlOutput html={htmlOutput} />
        </div>
    );
};

export default App;
