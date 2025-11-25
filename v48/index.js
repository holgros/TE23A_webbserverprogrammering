// Importera express och fileserver (installera med npm först: "npm install").
var express = require("express");
var fs = require("fs");

// Skapa en express-server...
app = express();

// ... som lyssnar på port 8080...
app.listen(8080);
console.log("Servern körs på port 8080.");

// ... och skriver välkommen när man öppnar rotsidan.
app.get("/", function (req, res) {
  res.send("Välkommen till rotsidan!");
});

// Servern läser html-fil när man öppnar sökvägen 'readfile'.
app.get("/readfile", function (req, res) {
  fs.readFile("index.html", function (err, data) {
    data = data.toString();
    res.send(data);
  });
});