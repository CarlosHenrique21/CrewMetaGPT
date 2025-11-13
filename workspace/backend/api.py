"""
Flask REST API for Markdown to HTML conversion.
Endpoint: POST /convert
Request body: { "markdown": "string" }
Response body: { "html": "string" }
"""
from flask import Flask, request, jsonify
from converter.parser import MarkdownParser
from converter.sanitizer import sanitize_html

app = Flask(__name__)
parser = MarkdownParser()


@app.route('/convert', methods=['POST'])
def convert_markdown():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON."}), 400

    data = request.get_json()
    markdown_text = data.get('markdown')
    if not isinstance(markdown_text, str):
        return jsonify({"error": "'markdown' field must be a string."}), 400

    try:
        html = parser.parse(markdown_text)
        safe_html = sanitize_html(html)
        return jsonify({"html": safe_html}), 200
    except Exception as e:
        return jsonify({"error": f"Conversion error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
