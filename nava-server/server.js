
const path = require('path')
const {spawn} = require('child_process')
const express = require('express')
const app = express()
const http = require("http")
const WebSocket = require("ws")
const server = http.createServer(app);
const wss = new WebSocket.Server({server});

function runScript() {
  return spawn('python', [
    "-u",
    path.join(__dirname, 'script.py')
  ]);
}


app.use('/public', express.static(path.join(__dirname, 'public')))
//may need to also be change to /public, TBD YUP needed to do it
app.get('/public', function (req, res) {
  res.sendFile(path.join(__dirname, 'index.html'))
})
//if running into problems, try making this '/public' instead 


function runScriptInWebsocket(id, ws) {
  const child = runScript("foobar")
  child.stdout.on('data', (data) => {
    ws.send(`${id}:${data}`);
  });
  child.stderr.on('data', (data) => {
    ws.send(`${id}:error:\n${data}`);
  });
  child.stderr.on('close', () => {
    ws.send(`${id}:done`);
  });
}

let id = 1
wss.on('connection', (ws) => {
  const thisId = id++;
  ws.on('message', (message) => {
    ws.send(`You sent -> ${message}`);
    if ("run" === message) {
      runScriptInWebsocket(thisId, ws)
    }
  });
  ws.send('Connection with WebSocket server initialized');
});

server.listen(8080, () => console.log('Server running on port 8080 public'))