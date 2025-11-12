#!/usr/bin/env node

/**
 * CLI tool for Markdown to HTML conversion.
 *
 * Usage:
 *   node cli/index.js [input.md] [output.html]
 *   - If no input file is provided, reads from stdin.
 *   - If output file is omitted, prints to stdout.
 */

const fs = require('fs');
const path = require('path');
const markdownIt = require('markdown-it');
const { JSDOM } = require('jsdom');

const md = new markdownIt({
    html: false, // Disable HTML tags in source
    linkify: true,
    typographer: true
});

// Simple sanitizer using DOMPurify with jsdom
function sanitizeHtml(dirty) {
    const window = new JSDOM('').window;
    const DOMPurify = require('dompurify')(window);
    return DOMPurify.sanitize(dirty, {USE_PROFILES: {html: true}});
}

function printUsage() {
    console.log('Usage: node cli/index.js [input.md] [output.html]');
    console.log('  If no input.md is provided, reads from stdin.');
    console.log('  If no output.html is provided, prints to stdout.');
}

async function main() {
    const args = process.argv.slice(2);
    let input = '';

    if (args.includes('-h') || args.includes('--help')) {
        printUsage();
        process.exit(0);
    }

    if (args.length === 0) {
        // read from stdin
        input = await new Promise((resolve, reject) => {
            let data = '';
            process.stdin.setEncoding('utf8');
            process.stdin.on('data', chunk => data += chunk);
            process.stdin.on('end', () => resolve(data));
            process.stdin.on('error', err => reject(err));
        });
    } else {
        // read from file
        const inputPath = args[0];
        try {
            input = fs.readFileSync(inputPath, 'utf8');
        } catch (err) {
            console.error(`Error reading input file: ${err.message}`);
            process.exit(1);
        }
    }

    try {
        let html = md.render(input);
        html = sanitizeHtml(html);

        if (args.length > 1) {
            const outputPath = args[1];
            fs.writeFileSync(outputPath, html, 'utf8');
        } else {
            console.log(html);
        }
    } catch (err) {
        console.error(`Error during conversion: ${err.message}`);
        process.exit(1);
    }
}

main();
