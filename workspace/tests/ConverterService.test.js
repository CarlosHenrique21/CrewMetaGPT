// tests/ConverterService.test.js

import ConverterService from '../src/services/ConverterService';

describe('ConverterService', () => {
    let converterService;

    beforeEach(() => {
        converterService = new ConverterService(); // Instantiate the service before each test
    });

    test('should convert valid Markdown to HTML', () => {
        const markdown = '# Title\n* Item 1\n* Item 2';
        const expectedHtml = '<ul><h1>Title</h1><li>Item 1</li><li>Item 2</li></ul>';
        expect(converterService.convert(markdown)).toBe(expectedHtml);
    });

    test('should throw an error for empty input', () => {
        expect(() => converterService.convert('')).toThrow('Input cannot be empty');
    });
});
