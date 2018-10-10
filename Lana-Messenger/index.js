'use strict'

const express = require('express');
const request = require('request');
const bodyParser = require('body-parser');
const keys = require('./constants');

const app = express();
app.use(bodyParser.json());

app.get('/', (req, res) => res.send('hello world!'));

const sendText = (sender, text) => {

  request({
    url: 'https://graph.facebook.com/v2.6/me/messages',
    qs: {access_token: keys.PAGE_ACESS_TOKEN},
    method: 'POST',
    json: {
      recipient: {id: sender},
      message: {
        text: text
      }
    }
  }, (error, response, body) => {
    if (error) {
      console.log('Error sending message: ', error);
    } else if (response.body.error) {
      console.log('Error: ', response.body.error);
    }
  });
}

const sendAttachment = (sender, attachmentUrl, attachmentType) => {
  // type can be: image, video, audio or file

  request({
    url: 'https://graph.facebook.com/v2.6/me/messages',
    qs: {access_token: keys.PAGE_ACESS_TOKEN},
    method: 'POST',
    json: {
      recipient: {
        id: sender
      },
      message: {
        attachment: {
          type: attachmentType,
          payload: {
            url: attachmentUrl,
            is_reusable: true
          }
        }
      }
    }
  }, (error, response, body) => {
    if (error) {
      console.log('Error sending message: ', error);
    } else if (response.body.error) {
      console.log('Error: ', response.body.error);
    }
  });
}

// Adds support for GET requests to our webhook
app.get('/webhook', (req, res) => {
  
  // Your verify token. Should be a random string.
  let VERIFY_TOKEN = keys.VERIFY_TOKEN;
    
  // Parse the query params
  let mode = req.query['hub.mode'];
  let token = req.query['hub.verify_token'];
  let challenge = req.query['hub.challenge'];
    
  // Checks if a token and mode is in the query string of the request
  if (mode && token) {
  
    // Checks the mode and token sent is correct
    if (mode === 'subscribe' && token === VERIFY_TOKEN) {
      
      // Responds with the challenge token from the request
      console.log('WEBHOOK_VERIFIED');
      res.status(200).send(challenge);
    
    } else {
      // Responds with '403 Forbidden' if verify tokens do not match
      res.sendStatus(403);      
    }
  }
});

// Creates the endpoint for our webhook 
app.post('/webhook', (req, res) => {
  let body = req.body;

  // Checks this is an event from a page subscription
  if (body.object === 'page') {

    // Iterates over each entry - there may be multiple if batched
    body.entry.forEach(function(entry) {

      // Gets the message. entry.messaging is an array, but 
      // will only ever contain one message, so we get index 0
      let webhookEvent = entry.messaging[0];

      let senderID = webhookEvent.sender.id;
      let messageText = webhookEvent.message.text;

      // Here goes your call back, you can make some function that process
      // the text before you send a response to the user. I just sent the 
      // same text back to the user.
      sendText(senderID, messageText);
    });

    // Returns a '200 OK' response to all requests
    res.status(200).send('EVENT_RECEIVED');
  } else {
    // Returns a '404 Not Found' if event is not from a page subscription
    res.sendStatus(404);
  }

});

// The 'process.env.PORT' is necessary if you want to use some services as Heroku
const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Example app listening on port ${port}!`));
