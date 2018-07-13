class Lana {}
const keys = require('./config/keys');
const watsonAPI = require('./watson');
let lana = new Lana();

lana.recvMessage = (messageBody) => {
    return new Promise((resolve, reject) => {
        watsonAPI.sendMessageToWatson(messageBody.message, {})
            .then(watson_answer => {
                let msgJson = {
                    message : watson_answer.output.text[0],
                    chatId : messageBody.user.chatId
                  };
                resolve(msgJson);
            })
            .catch(err => reject(console.error));
    });
}

module.exports = lana;