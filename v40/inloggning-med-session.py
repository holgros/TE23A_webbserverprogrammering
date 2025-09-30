from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'hemligtextsträngsomingenkangissa'  # Används för sessionshantering

# användardata - endast ett exempel, i verkligheten kanske vi läser in detta från fil/databas
elev = {'username': 'kalle', 'password': 'anka', 'email': 'kalle.anka@skola.taby.se'}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # kontrollera att inloggningsuppgifter stämmer
        if request.form['name'] == elev['username'] and request.form['password'] == elev['password']:
            session['user'] = request.form['name'] # Så här sätter man värde på en sessionsvariabel.
        else:
            session.clear()
        return redirect(url_for('login'))
    
    # Det här returneras om GET-anrop görs
    return f'''
        <form method="post">
            Username: <input type="text" name="name" value=""><br>
            Password: <input type="password" name="password" value="">
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/login')
def login():
    if session:
        return f'''
        <p>Du är inloggad som {str(session['user'])}.</p>
        <p><a href="/annansida">Gå vidare</a></p>
        <p><a href="/logout">Logga ut</a></p>
        '''
    else:
        return f'''
            <p>Inloggning misslyckades. <a href="/">Försök igen!</a></p>
        '''

@app.route('/annansida')
def annansida():
    if session:
        return f'''
            <p>Här finns en sida med information som handlar specifikt om eleven {elev['username']}. Du kan t.ex. se elevens mailadress: {elev['email']}.</p>
            <p><a href="/login">Tillbaka till startsidan</a></p>
        '''
    else:
        return f'''
            <p>Du är inte inloggad. <a href="/">Logga in!</a></p>
        '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')