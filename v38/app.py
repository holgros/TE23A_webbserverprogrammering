from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

FILE_PATH = 'demo.txt'

HTML = '''
<!doctype html>
<title>File Read/Write Demo</title>
<h2>Write to File</h2>
<form method="post" action="/write">
    <textarea name="content" rows="5" cols="40">{{ file_content }}</textarea><br>
    <input type="submit" value="Save">
</form>
<h2>Read from File</h2>
<pre>{{ file_content }}</pre>
'''

@app.route('/', methods=['GET'])
def index():
    content = ''
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as f: #Flaggan 'r' (read) anger att filen ska läsas
            content = f.read()  # .read() läser innehållet i filen
    return render_template_string(HTML, file_content=content)

@app.route('/write', methods=['POST'])
def write():
    content = request.form.get('content', '')
    with open(FILE_PATH, 'w', encoding='utf-8') as f: #Flaggan 'w' (write) anger att filen ska skrivas
        f.write(content)    # .write() skriver innehållet i variabeln content till filen
    return render_template_string(HTML, file_content=content)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
