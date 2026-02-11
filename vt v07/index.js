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

// KOPIERAT FRÅN TIDIGARE LEKTIONSEXEMPEL

const COLUMNS = ["firstname", "lastname", "userId", "passwd"]; // ÄNDRA TILL NAMN PÅ KOLUMNER I ER EGEN TABELL

// grundläggande exempel - returnera en databastabell som JSON
app.get("/users", function (req, res) {
  let sql = "SELECT * FROM users"; // ÄNDRA TILL NAMN PÅ ER EGEN TABELL (om den heter något annat än "users")
  let condition = createCondition(req.query); // output t.ex. " WHERE lastname='Rosencrantz'"
  console.log(sql + condition); // t.ex. SELECT * FROM users WHERE lastname="Rosencrantz"
  // skicka query till databasen
  con.query(sql + condition, function (err, result, fields) {
    res.send(result);
  });
});

let createCondition = function (query) {
  // skapar ett WHERE-villkor utifrån query-parametrar
  console.log(query);
  let output = " WHERE ";
  for (let key in query) {
    if (COLUMNS.includes(key)) {
      // om vi har ett kolumnnamn i vårt query
      output += `${key}="${query[key]}" OR `; // t.ex. lastname="Rosencrantz"
    }
  }
  if (output.length == 7) {
    // " WHERE "
    return ""; // om query är tomt eller inte är relevant för vår databastabell - returnera en tom sträng
  } else {
    return output.substring(0, output.length - 4); // ta bort sista " OR "
  }
};

// route-parameter, dvs. filtrera efter ID i URL:en
app.get("/users/:id", function (req, res) {
  // Värdet på id ligger i req.params
  let sql = "SELECT * FROM users WHERE id=" + req.params.id;
  console.log(sql);
  // skicka query till databasen
  con.query(sql, function (err, result, fields) {
    if (result.length > 0) {
      res.send(result);
    } else {
      res.sendStatus(404); // 404=not found
    }
  });
});

// SERVA FRONTEND-APPLIKATION

app.get("/demo", function (req, res) {
  res.sendFile(__dirname + "/frontend-demo.html");
});
