// tests/MarkdownParser.test.js

import MarkdownParser from '../src/utils/MarkdownParser';

describe('MarkdownParser', () => {
    let markdownParser;

    beforeEach(() => {
        markdownParser = new MarkdownParser(); // Instantiate the parser before each test
    });

    test('should convert H1 to HTML', () => {
        const markdown = '# Title';
        const expectedHtml = '<h1>Title</h1>';
        expect(markdownParser.convert(markdown)).toBe(expectedHtml);
    });

    test('should convert unordered list to HTML', () => {
        const markdown = '* Item 1\n* Item 2';
        const expectedHtml = '<ul><li>Item 1</li><li>Item 2</li></ul>';
        expect(markdownParser.convert(markdown)).toBe(expectedHtml);
    });

    test('should convert ordered list to HTML', () => {
        const markdown = '1. Item 1\n2. Item 2';
        const expectedHtml = '<ul><li>Item 1</li><li>Item 2</li></ul>';
        expect(markdownParser.convert(markdown)).toBe(expectedHtml);
    });
});
