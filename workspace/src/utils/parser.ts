import {marked} from 'marked';
import DOMPurify from 'dompurify';

/**
 * Function to convert Markdown text to sanitized HTML string.
 * @param markdown - input Markdown string
 * @returns sanitized HTML string
 */
export function parseMarkdownToHtml(markdown: string): string {
  // Use marked to parse markdown to HTML
  const rawHtml = marked.parse(markdown, { 
    headerIds: false,
    mangle: false,
  });

  // Sanitize the generated HTML to prevent XSS
  const cleanHtml = DOMPurify.sanitize(rawHtml, { 
    ALLOWED_TAGS: ['h1','h2','h3','ul','ol','li','a','p','strong','em','code','pre'],
    ALLOWED_ATTR: ['href', 'title', 'target', 'rel'],
  });

  return cleanHtml;
}
