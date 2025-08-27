from flask import Flask, request

app = Flask(__name__)

# Example of a simple GET route that returns a few lines of HTML code
@app.route('/')
def home():
    return '''
            <p>Välkommen till Flask Routing! Testa följande router:</p>
            <ul>
            <li>/user/[username]</li>
            <li>/search?q=[query]</li>
            <li>/form</li>
            </ul>
            '''

# Example of GET route with URL parameters. For example http://127.0.0.1:5000/user/holger
@app.route('/user/<username>')
def show_user_profile(username):
    return f'User: {username}'

# Example of GET route with query parameters. For example http://127.0.0.1:5000/search?q=flask
@app.route('/search')
def search():
    # request.args contains information from the query string
    query = request.args.get('q', '')
    return f'Search query: {query}'

# GET route that displays a simple form POSTing to the /submit route
@app.route('/form')
def form():
    return '''
        <form action="/submit" method="post">
            <label for="data">Enter something:</label>
            <input type="text" id="data" name="data"><br>
            <input type="checkbox" id="checkbox" name="checkbox"><label for="checkbox">Check this</label> <br>
            <input type="submit" value="Submit">
        </form>
    '''

# Example of a simple POST route that handles POST requests to /submit
@app.route('/submit', methods=['POST'])
def submit():
    # request.form is a dictionary-like object containing form data
    data = request.form.get('data', '')  #form data is captured here using the name attribute of the input
    checkbox = request.form.get('checkbox', False)
    return f'Skickat via POST: {data}, Checkbox: {checkbox}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')