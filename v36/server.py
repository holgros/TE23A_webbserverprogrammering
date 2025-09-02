from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():    # HTML-filen ligger i en mapp med namnet "templates"
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') # filerna servas via din IP-adress i det lokala nätverket