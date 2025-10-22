"""
Innan du kör koden, skapa en tabell med följande kommando:
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Autoinkrementerande primärnyckel
    fornamn VARCHAR(50) NOT NULL,       -- Förnamn, max 50 tecken
    efternamn VARCHAR(100) NOT NULL,    -- Efternamn, max 100 tecken
    klass VARCHAR(5) NOT NULL         -- Klass, max 5 tecken
);
Alternativt får du anpassa nedanstående anrop så att de fungerar för din tabell
"""
from flask import Flask, redirect, render_template, request, url_for
import mysql.connector  # installera med "pip install mysql-connector-python" i kommandotolken, ifall du inte redan gjort detta

app = Flask(__name__)

# startsida
@app.route('/')
def home():
    return render_template('home.html')

# läs från databas
@app.route('/read')
def read():
    db = get_connection()
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM students")
    students = mycursor.fetchall()
    return render_template('read.html', students=students)

# skriv till databas
@app.route('/write', methods=['GET', 'POST'])
def write_form():
    if request.method == 'GET':
        return render_template('write.html')
    else: # POST
        fornamn = request.form.get('fornamn', '')
        efternamn = request.form.get('efternamn', '')
        klass = request.form.get('klass', '')
        db = get_connection()
        mycursor = db.cursor()
        sql = "INSERT INTO students (fornamn, efternamn, klass) VALUES (%s, %s, %s)"
        val = (fornamn, efternamn, klass)
        mycursor.execute(sql, val)
        db.commit()
        return redirect(url_for('confirm'))

# visa bekräftelse
@app.route('/confirm')
def confirm():
    return render_template("confirm.html")

# skapa databasuppkoppling
def get_connection(host="localhost", user="root", password=""):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database="webbserverprogrammering"  # byt namn om din databas heter något annat
    )
    return mydb

# starta webbservern
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')