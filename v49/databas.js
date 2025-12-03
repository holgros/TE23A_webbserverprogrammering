// koppla upp till databas, https://www.w3schools.com/nodejs/nodejs_mysql.asp
let mysql = require("mysql"); // installera med kommandot "npm install" som vanligt
let dbConfig = {
  host: "localhost", // IP-adress till databas-servern
  user: "root", // standard-användarnamn till XAMPPs databas
  password: "", // standardlösenord
  database: "webbserverprogrammering", // ÄNDRA TILL NAMN PÅ DIN DATABAS
};

// Demonstration av hur man läser från databas och skriver till konsol
let con = mysql.createConnection(dbConfig);
con.connect(function (err) {
  if (err) throw err; // felhantering
  console.log("Uppkopplad till databas!");
  // skicka query, https://www.w3schools.com/nodejs/nodejs_mysql_select.asp
  con.query("SELECT * FROM users", function (err, result, fields) {
    if (err) throw err; // felhantering
    console.log(result); // skriv ut innehållet i databasen till kommandotolken
    // hantera enstaka objekt och attribut, t.ex.:
    console.log(result[0]); // skriver ut första raden (objektet) i tabellen
    console.log(result[0].email); // skriver ut attributet "email" (förutsatt att detta finns - ändra om din tabell ser annorlunda ut)
  });
  // stäng uppkopplingen, kan vara önskvärt ifall man inte vill tvångsavsluta programmet i konsolen
  con.end(function (err) {
    if (err) throw err; // felhantering
    console.log("Stänger uppkopplingen.");
  });
});

// Skriv ut databastabellens innehåll på en webbsida
// Börja med att starta webbservern och definiera en route (som vi gjort flera gånger tidigare)
const express = require("express");
const app = express();
app.listen(3000);
console.log("Webbservern körs på port 3000.");
app.get("/", function (req, res) {
  // skicka query till databasen - kopiera samma kod som ovan
  con = mysql.createConnection(dbConfig);
  con.connect(function (err) {
    if (err) throw err;
    console.log("Uppkopplad till databas!");
    con.query("SELECT * FROM users", function (err, result, fields) {
      if (err) throw err;
      // skriv ut
      let output = skrivUtHtml(result, res);
      res.send(output);
    });
  });
});

// funktion som returnerar enkel HTML-kod med tabellens innehåll
let skrivUtHtml = function (result) {
  let output = "";
  for (let user of result) {
    // loopa igenom varje rad i databastabellen
    for (let key in user) {
      // loopa igenom varje kolumn i raden
      output += `${key}: ${user[key]}, `;
    }
    output += "<br>";
  }
  return output;
};