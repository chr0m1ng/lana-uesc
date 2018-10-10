class Watson {}
const keys = require('./config/keys');
const watson = require('watson-developer-cloud');
const watson_conversation = new watson.ConversationV1({
    username: keys.watson_username,
    password: keys.watson_password,
    version: keys.watson_version
});

let watsonAPI = new Watson();

watsonAPI.sendMessageToWatson = (message, context, intent = null) => {
    return new Promise((resolve, reject) => { 
        context['timezone'] = 'America/Sao_Paulo';
        if(intent == null) {
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
        }
        else {
            watson_conversation.message({
                workspace_id: keys.watson_workspace_id,
                input: {
                    'text' : message
                },
                'context': context,
                intents : [{
                    "intent" : intent,
                    "confidence" : 1
                }]
            }, (err, res) => {
                if(err)
                    reject('Desculpe, tente novamente mais tarde');
                else
                    resolve(res);
            });
        }
    });
}

watsonAPI.sendIntentToWatson = (intent, context = {}) => {
    return new Promise((resolve, reject) => {
        watson_conversation.message({
            workspace_id: keys.watson_workspace_id,
            intents : [{
                "intent" : intent,
                "confidence" : 1
            }],
            'context' : context
        }, (err, res) => {
            if(err)
                reject(err);
            else
                resolve(res);
        });
    });
}

module.exports = watsonAPI;