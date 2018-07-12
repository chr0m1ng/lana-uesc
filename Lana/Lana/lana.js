class Lana {}
const keys = require('./config/keys');
const watson = require('watson-developer-cloud');
const watson_conversation = new watson.ConversationV1({
    username: keys.watson_username,
    password: keys.watson_password,
    version: keys.watson_version
  });
let lana = new Lana();

const sendMessageToWatson = (message, context) => {
    return new Promise((resolve, reject) => { 
        watson_conversation.message({
            workspace_id: keys.watson_workspace_id,
            input: {
                'text' : message
            },
            'context': context
        }, (err, res) => {
            if(err)
                reject('Desculpe, tente novamente mais tarde');
            else
                resolve(res);
        });
    });
}

lana.recvMessage = (messageBody) => {
    return new Promise((resolve, reject) => {
        sendMessageToWatson(messageBody.message, {})
            .then(watson_answer => {
                resolve(watson_answer.output.text[0]);
            })
            .catch(err => reject(console.error));
    });
}

module.exports = lana;