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
from flask import Flask, render_template, request
import mysql.connector

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
@app.route('/write')
def write_form():
    return render_template('write.html')

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