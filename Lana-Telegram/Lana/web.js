const express = require('express');
const packageInfo = require('./package.json');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

app.get('/', (req, res) => {
  res.json({ version: packageInfo.version });
});

const server = app.listen(process.env.PORT, () => {
  const host = server.address().address;
  const port = server.address().port;

  console.log('Web server started at http://%s:%s', host, port);
});

module.exports = (lana) => {
  app.post('//' + lana.token, (req, res) => {
    lana.processUpdate(req.body);
    res.sendStatus(200);
  }),
  app.post('/' + lana.token + '/sendMessage', (req, res) => {
    lana.sendMessageEndpoint(req.body)
      .then(resp => {
        res.sendStatus(200);
      })
      .catch(err => {
        res.sendStatus(400);
      });
  })
};