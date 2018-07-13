class Watson {}
const keys = require('./config/keys');
const watson = require('watson-developer-cloud');
const watson_conversation = new watson.ConversationV1({
    username: keys.watson_username,
    password: keys.watson_password,
    version: keys.watson_version
});

let watsonAPI = new Watson();

watsonAPI.sendMessageToWatson = (message, context) => {
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

module.exports = watsonAPI;