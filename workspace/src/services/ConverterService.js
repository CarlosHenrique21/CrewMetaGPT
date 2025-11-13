// src/services/ConverterService.js

import MarkdownParser from '../utils/MarkdownParser';

/**
 * ConverterService class to validate input and convert Markdown to HTML.
 */
class ConverterService {
    private markdownParser: MarkdownParser;

    constructor() {
        this.markdownParser = new MarkdownParser(); // Initialize the Markdown parser
    }

    /**
     * Validates the Markdown input.
     * @param {string} input - The Markdown input to validate.
     * @returns {boolean} - True if valid, false otherwise.
     */
    validateInput(input: string): boolean {
        // Check if input is not empty
        return input.trim() !== '';
    }

    /**
     * Converts Markdown input to HTML.
     * @param {string} markdown - The Markdown text to convert.
     * @returns {string} - The converted HTML or an error message.
     */
    convert(markdown: string): string {
        if (!this.validateInput(markdown)) {
            throw new Error("Input cannot be empty"); // Throw an error for invalid input
        }
        return this.markdownParser.convert(markdown); // Convert valid Markdown input
    }
}

export default ConverterService;
