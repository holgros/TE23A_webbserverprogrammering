const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Servera statiska filer
app.use(express.static('public'));

// Håll koll på spelare och frågor
let players = {};
let currentQuestion = null;
let answers = [];

io.on('connection', (socket) => {
    console.log('Ny anslutning: ' + socket.id);

    // När en spelare ansluter
    socket.on('join', (playerName) => {
        players[socket.id] = {
            name: playerName,
            score: 0
        };
        
        socket.emit('welcome', `Välkommen ${playerName}!`);
        io.emit('playersUpdate', players);
    });

    // När en spelare svarar
    socket.on('answer', (data) => {
        const isCorrect = data.answer === currentQuestion.correct;
        
        if (isCorrect) {
            players[socket.id].score += 10;
        }
        
        answers.push({
            playerId: socket.id,
            playerName: players[socket.id].name,
            answer: data.answer,
            correct: isCorrect
        });
        
        io.emit('answerUpdate', answers);
        io.emit('playersUpdate', players);
    });

    // När läraren skickar en fråga
    socket.on('newQuestion', (question) => {
        currentQuestion = question;
        answers = []; // Rensa tidigare svar
        
        io.emit('question', question);
    });

    // När någon kopplar ifrån
    socket.on('disconnect', () => {
        delete players[socket.id];
        io.emit('playersUpdate', players);
    });
});

server.listen(80, () => {
    console.log('Servern körs på http://localhost');
});