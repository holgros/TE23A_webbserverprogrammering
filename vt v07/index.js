let express = require("express"); // INSTALLERA MED "npm install express" I KOMMANDOTOLKEN
let app = express();
app.listen(3000);
console.log("Servern körs på port 3000");

app.get("/", function (req, res) {
  res.sendFile(__dirname + "/dokumentation.html");
});

const mysql = require("mysql"); // INSTALLERA MED "npm install mysql" I KOMMANDOTOLKEN
con = mysql.createConnection({
  host: "localhost", // databas-serverns IP-adress
  user: "root", // standardanvändarnamn för XAMPP
  password: "", // standardlösenord för XAMPP
  database: "webbserverprogrammering", // ÄNDRA TILL NAMN PÅ ER EGEN DATABAS
});

app.use(express.json());

app.post("/users", function (req, res) {
  //data ligger i req.body. Kontrollera att det är korrekt.
  if (isValidUserData(req.body)) {
    //skriv till databas

    /* SÅRBAR KOD FRÅN FÖRRA VECKAN - SE UPP FÖR FARLIG INPUT!
    let sql = `INSERT INTO users (firstname, lastname, userId, passwd)
    VALUES ('${req.body.firstname}', 
    '${req.body.lastname}',
    '${req.body.userId}',
    '${req.body.passwd}');`;
    console.log(sql);
    */
    
    // Ett s.k. prepared statement skyddar lite bättre mot farlig input
    let sql = "INSERT INTO users (firstname, lastname, userId, passwd) VALUES (?, ?, ?, ?)";  // OBS: frågetecken/placeholders
    let input = [req.body.firstname, req.body.lastname, req.body.userId, req.body.passwd];    // varje element motsvarar ett frågetecken
    con.query(sql, input, function (err, result, fields) {  // OBS: argumentet input
      if (err) {
        console.log(err);
        res.status(500).send("Fel i databasanropet!");
        throw err;
      }
      // kod för att hantera retur av data
      console.log(result);
      let output = {
        id: result.insertId,
        firstname: req.body.firstname,
        lastname: req.body.lastname,
        userId: req.body.userId,
        passwd: req.body.passwd,
      };
      res.json(output);
    });
  } else {
    res.status(422).send("userId required!"); // eller annat meddelande enligt nedan
  }
});

// funktion för att kontrollera att användardata finns
function isValidUserData(body) {
  return body && body.userId; // returnerar true ifall data är OK, false ifall något av attributen är undefined
  /* andra möjligheter (anpassa efter era egna behov):
        - kolla att firstname, lastname och passwd är textsträngar (snarare än tal, fält osv.)
        - kolla att userId är en textsträng med rätt format (fyra bokstäver motsvarande första två i fornamn + efternamn)
        - kolla att passwd uppfyller vanliga kriterier (minimilängd, innehåller olika typer av tecken osv.)
        - (kolla att userId inte redan är upptaget - eventuellt bättre att kolla detta i samband med att man skriver till databasen genom att göra denna kolumn till key i databastabellen)
    Returnera gärna ett felmeddelande istället för bara false ifall det finns ett fel, så att användaren kan göra rätt vid nästa försök
    */
}
