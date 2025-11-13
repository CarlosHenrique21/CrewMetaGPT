// src/components/MarkdownInput.jsx

import React from 'react';

/**
 * MarkdownInput component for user input.
 * @param {object} props - Component props.
 * @param {string} props.markdown - Current Markdown input.
 * @param {function} props.setMarkdown - Function to update Markdown input.
 */
const MarkdownInput = ({ markdown, setMarkdown }) => {
    return (
        <textarea
            rows="10"
            cols="50"
            value={markdown}
            onChange={(e) => setMarkdown(e.target.value)} // Update Markdown input on change
            placeholder="Enter your Markdown text here..."
        />
    );
};

export default MarkdownInput;
