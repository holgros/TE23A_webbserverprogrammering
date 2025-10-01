from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'hemligtextsträngsomingenkangissa'  # Används för sessionshantering

# användardata - endast ett exempel, i verkligheten kanske vi läser in detta från fil/databas
elever = [
    {'username': 'kalle', 'password': 'anka', 'email': 'kalle.anka@skola.taby.se'},
    {'username': 'alexander', 'password': 'lukas', 'email': 'alexander.lukas@skola.taby.se'}
          ]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # kontrollera att inloggningsuppgifter stämmer
        logged_in = False
        for elev in elever:
            if request.form['name'] == elev['username'] and request.form['password'] == elev['password']:
                logged_in = True
                session['user'] = elev
                break
        if not logged_in: # om hela loopen har gått utan att någon matchning hittats
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
        <p>Du är inloggad som {session['user']['username']}.</p>
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
            <p>Här finns en sida med information som handlar specifikt om eleven {session['user']['username']}. Du kan t.ex. se elevens mailadress: {session['user']['email']}.</p>
            <p>
                Du kan även skriva något här:
                    <form method="post" action="/append">
                        <input type="text" name="line" size="40" placeholder="Skriv något">
                        <input type="submit" value="Spara">
                    </form>
            </p>
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

@app.route('/append', methods=['POST'])
def append():
    if not session: # om man inte är inloggad
        return f'''
            <p>Du är inte inloggad. <a href="/">Logga in!</a></p>
        '''
    line = f'{session['user']['username']} skrev: {request.form.get('line', '')}'
    with open('meddelanden.txt', 'a', encoding='utf-8') as f:
        f.write(line + '\n')
    return redirect('/annansida')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')