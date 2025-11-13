// src/components/PreviewButton.jsx

import React from 'react';

/**
 * PreviewButton component to trigger conversion.
 * @param {object} props - Component props.
 * @param {function} props.onClick - Function to call on button click.
 */
const PreviewButton = ({ onClick }) => {
    return (
        <button onClick={onClick}>Convert to HTML</button> // Button to trigger conversion
    );
};

export default PreviewButton;
