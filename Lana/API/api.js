const express = require('express');
const packageInfo = require('../package.json');
const bodyParser = require('body-parser');
const keys = require('./config/keys');

const app = express();
app.use(bodyParser.json());

app.get('/', (req, res) => {
  res.send('Para usar e autenticar fazer post request em /api/message e passar x-api-key na header');
});

// const server = app.listen(5000, () => {
const server = app.listen(process.env.PORT, () => {
  const host = server.address().address;
  const port = server.address().port;

  console.log('Web server started at http://%s:%s', host, port);
});

const authAPI = (key) => {
  if(key == keys.master_key)
    return true;
  else
    return false;
}

module.exports = (lana) => {
  app.post('/api/message', (req, res) => {
    if(authAPI(req.get('x-api-key'))) {
      lana.recvMessage(req.body)
        .then(respFromLana => {
          res.statusCode = 200;
          res.send(respFromLana);
        })
        .catch(err => {
          res.statusCode = 500;
          res.send('Desculpe, tente novamente mais tarde');
        });
    }
    else {
      console.error('AUTH FAILED');
      res.statusCode = 401;
      res.send('API_KEY invalida');
    }
  })
};