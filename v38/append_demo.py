from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

APPEND_FILE = 'append_demo.txt'

HTML = '''
<!doctype html>
<title>Append File Demo</title>
<h2>Append to File</h2>
<form method="post" action="/append">
    <input type="text" name="line" size="40" placeholder="Enter text to append">
    <input type="submit" value="Append">
</form>
<h2>File Contents</h2>
<pre>{{ file_content }}</pre>
'''

@app.route('/', methods=['GET'])
def append_demo():
    content = ''
    if os.path.exists(APPEND_FILE):
        with open(APPEND_FILE, 'r', encoding='utf-8') as f: #Flaggan 'r' (read) anger att filen ska läsas
            content = f.read()
    return render_template_string(HTML, file_content=content)

@app.route('/append', methods=['POST'])
def append():
    line = request.form.get('line', '')
    if line:
        with open(APPEND_FILE, 'a', encoding='utf-8') as f: #Flaggan 'a' (append) anger att filen ska skrivas till i slutet
            f.write(line + '\n')
    # Läs tillbaka hela filen för att visa uppdaterat innehåll
    with open(APPEND_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    return render_template_string(HTML, file_content=content)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
