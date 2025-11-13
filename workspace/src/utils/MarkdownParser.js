// src/utils/MarkdownParser.js

/**
 * MarkdownParser class to convert Markdown text to HTML.
 */
class MarkdownParser {
    /**
     * Converts Markdown text to HTML.
     * @param {string} markdown - The Markdown text to convert.
     * @returns {string} - The converted HTML.
     */
    convert(markdown) {
        // Convert Markdown titles to HTML headers
        const html = markdown
            .split('\n')
            .map(line => {
                if (/^# (.+)/.test(line)) {
                    return `<h1>${line.replace(/^# (.+)/, '$1')}</h1>`;
                } else if (/^## (.+)/.test(line)) {
                    return `<h2>${line.replace(/^## (.+)/, '$1')}</h2>`;
                } else if (/^### (.+)/.test(line)) {
                    return `<h3>${line.replace(/^### (.+)/, '$1')}</h3>`;
                } else if (/^\* (.+)/.test(line)) {
                    return `<li>${line.replace(/^\* (.+)/, '$1')}</li>`;
                } else if (/^\d+\. (.+)/.test(line)) {
                    return `<li>${line.replace(/^\d+\. (.+)/, '$1')}</li>`;
                }
                return line; // Return the line unchanged if it doesn't match any pattern
            })
            .join('\n');
        
        // Wrap the list items in <ul> tags if there are any
        return `<ul>${html}</ul>`;
    }
}

export default MarkdownParser;
