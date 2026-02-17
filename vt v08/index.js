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

app.put("/users/:id", function (req, res) {
  //kod här för att hantera anrop…
  // kolla först att all data som ska finnas finns i request-body
  // i ett PUT-anrop måste hela "raden" finnas med, alltså alla attribut för en användare!
  if (!(req.body && req.body.firstname && req.body.lastname && req.body.userId && req.body.passwd)) {
    // om data saknas i body
    res.sendStatus(400);
    return;
  }
  let sql = `UPDATE users 
        SET firstname = ?, lastname = ?, userId = ?, passwd = ?
        WHERE id = ?`; // De tre frågetecknen ersätts i query-anropet nedan av värden från req-objektet med data från klienten

  con.query(
    sql,
    [req.body.firstname, req.body.lastname, req.body.userId, req.body.passwd, req.params.id],
    function (err, result) {
      if (err) {
        throw err;
        //kod här för felhantering, skicka felmeddelande osv.
      } else {
        // meddela klienten att request har processats OK
        res.sendStatus(200);
      }
    }
  );
});
