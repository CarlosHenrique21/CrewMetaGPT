# Markdown to HTML Converter
A web-based application that converts Markdown formatted text into HTML.

## Features
- Convert Markdown titles (H1, H2, H3) to corresponding HTML tags.
- Convert Markdown lists (ordered and unordered) to HTML lists.
- Convert Markdown links to HTML anchor tags.
- Display the converted HTML output in real-time.
- Download the converted HTML as a .html file.
- Reset input and output areas.

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/markdown-to-html-converter.git
   cd markdown-to-html-converter
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the application:
   ```bash
   npm start
   ```

## Usage Example
1. Open the application in your web browser.
2. Enter Markdown text in the input area.
3. Observe the HTML output appear in real-time.
4. Click the 'Download' button to save your HTML output as a .html file.

## Project Structure
```
markdown_to_html_converter/
├── src/
│   ├── components/
│   │   ├── MarkdownInput.jsx    # Component for Markdown input
│   │   ├── HtmlOutput.jsx        # Component for displaying HTML output
│   │   └── PreviewButton.jsx      # Button for triggering the conversion
│   ├── services/
│   │   └── ConverterService.js    # Business logic for input validation and conversion
│   ├── utils/
│   │   └── MarkdownParser.js       # Custom Markdown parsing logic
│   ├── App.jsx                    # Main application component
│   └── index.js                   # Application entry point
├── tests/
│   ├── ConverterService.test.js    # Unit tests for ConverterService
│   ├── MarkdownParser.test.js      # Unit tests for MarkdownParser
│   └── App.test.js                # Unit tests for App component
├── package.json                    # Project metadata and dependencies
└── README.md                       # Project documentation
```

## Testing Instructions
- Run unit tests:
  ```bash
  npm test
  ```
- Ensure at least 80% code coverage.

## Contributing Guidelines
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Create a pull request.

## License
MIT License.