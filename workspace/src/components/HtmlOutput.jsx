// src/components/HtmlOutput.jsx

import React from 'react';

/**
 * HtmlOutput component to display converted HTML.
 * @param {object} props - Component props.
 * @param {string} props.html - Converted HTML to display.
 */
const HtmlOutput = ({ html }) => {
    return (
        <div>
            <h2>Converted HTML Output:</h2>
            <div dangerouslySetInnerHTML={{ __html: html }} /> {/* Display HTML output */}
        </div>
    );
};

export default HtmlOutput;
