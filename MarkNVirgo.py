
from flask import Flask, request, render_template_string
import requests
import json

app = Flask(__name__)

# Replace with your actual API key
API_KEY = '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'


@app.route('/', methods=['GET', 'POST'])
def index():
    question = ""
    response = ""
    if request.method == 'POST':
        question = request.form['question']
        response = send_question_to_claude(API_KEY, question)
    return render_template_string(HTML_TEMPLATE, question=question, response=response)


def send_question_to_claude(api_key, question):
    url = 'https://api.anthropic.com/v1/messages'
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json',
        'anthropic-version': '2023-06-01'
    }
    data = {
        'model': 'claude-3-5-sonnet-20240620',
        'max_tokens': 1024,
        'messages': [
            {'role': 'user', 'content': question}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
        # Print the entire response for debugging
        print("Full API Response:", json.dumps(result, indent=2))

        # Check for content in the response
        if 'content' in result:
            if isinstance(result['content'], list) and len(result['content']) > 0:
                return result['content'][0].get('text', "No text content found.")
            elif isinstance(result['content'], str):
                return result['content']

        # If content is not directly accessible, try to navigate through the response structure
        elif 'messages' in result and len(result['messages']) > 0:
            content = result['messages'][0].get('content', [])
            if isinstance(content, list) and len(content) > 0:
                return content[0].get('text', "No text content found.")
            elif isinstance(content, str):
                return content

        return "Unable to extract response content. Please check the API response structure."
    else:
        return f"Error: {response.status_code} - {response.text}"






HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ask Claude 3.5 Sonnet</title>
</head>
<body>
    <h1>Ask a Question to Claude 3.5 Sonnet</h1>
    <form method="post">
        <label for="question">Enter your question:</label>
        <input type="text" id="question" name="question" required>
        <button type="submit">Send</button>
    </form>
    {% if question %}
        <h2>Question:</h2>
        <p>{{ question }}</p>
        <h2>Response:</h2>
        <p>{{ response }}</p>
    {% endif %}
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)