from flask import Flask, request, render_template_string
import json
import os

app = Flask(__name__)

JSON_FILE = 'data.json'

HTML = '''
<!doctype html>
<title>JSON File Demo</title>
<h2>Write JSON to File</h2>
<form method="post" action="/write-json">
    <textarea name="json_content" rows="10" cols="50">{{ json_content }}</textarea><br>
    <input type="submit" value="Save JSON">
</form>
<h2>Read JSON from File</h2>
<pre>{{ json_content }}</pre>
'''

@app.route('/', methods=['GET'])
def json_demo():
    content = ''
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                content = json.dumps(data, indent=4)
            except Exception as e:
                content = f'Error reading JSON: {e}'
    return render_template_string(HTML, json_content=content)

@app.route('/write-json', methods=['POST'])
def write_json():
    raw_content = request.form.get('json_content', '')
    try:
        data = json.loads(raw_content)
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        content = json.dumps(data, indent=4)
    except Exception as e:
        content = f'Invalid JSON: {e}'
    return render_template_string(HTML, json_content=content)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
