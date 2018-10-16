const BootBot = require('bootbot');
const request = require('request');
const keys = require('./config/keys');
const bodyParser = require('body-parser');

const bot = new BootBot({
    accessToken: keys.PAGE_ACESS_TOKEN,
    verifyToken: keys.VERIFY_TOKEN,
    appSecret: keys.APP_SECRET
});
bot.app.use(bodyParser.json());

bot.on('message', (payload, chat) => {
    const text = payload.message.text;
    chat.getUserProfile()
        .then(user => {
            const msgJson = {
                interface : 'messenger',
                type : 'incoming',
                message : text,
                from : {
                    name : user.first_name + ' ' + user.last_name,
                    id : user.id,
                    chatId : user.id
                },
                date : new Date()
            };
            console.log(JSON.stringify(msgJson));
            chat.sendAction('mark_seen');
            fowardMessageToLana(text, chat, user);
        });
});
  
const fowardMessageToLana = (text, chat, user) => {
    const options = {
        method : 'POST',
        uri : 'https://lana-api.herokuapp.com/api/message',
        headers : {
            'x-api-key': keys.LANA_API_KEY
        },
        body : {
            interface : 'messenger',
            message : text,
            user : {
                name : `${user.first_name} ${user.last_name}`,
                id : user.id,
                chatId : user.id
            },
            messageEndpoint : keys.URL_MESSAGE_ENDPOINT,
        },
        json : true // Automatically stringifies the body to JSON
    };
  
    request(options, (err, resp, body) => {
        if (!resp || resp.statusCode != 200 || err) {
            const msgJson = {
                interface : 'messenger',
                type : 'outgoing',
                message : text,
                errMessage : err,
                to : {
                    chatId : user.id
                },
                date : new Date()
            };
            console.log(JSON.stringify(msgJson));
            chat.say('Ops, algo deu errado, tente novamente', { typing : true });
        }
        else {
            let msgJson = {
                interface : 'messenger',
                type : 'outgoing',
                message : body.message,
                to : {
                chatId : body.chatId
                },
                date : new Date()
            };
            console.log(JSON.stringify(msgJson));
            let markdown = {};
            if(body.markdown) {
                markdown = {parse_mode: 'Markdown'};
            }
            chat.say(body.message, { typing : true });
        }
    });
};

// LANA'S ENDPOINT
bot.app.post('/' + keys.APP_SECRET + '/sendMessage', (req, res) => {
    sendMessageEndpoint(req.body)
        .then(resp => {
            res.sendStatus(200);
        })
        .catch(err => {
            res.sendStatus(400);
        });
    });
    
const sendMessageEndpoint = (messageBody) => {
    return new Promise((resolve, reject) => {
        if(messageBody.chatId && messageBody.message) {
            let msgJson = {
                interface : 'messenger',
                type : 'outgoing',
                message : messageBody.message,
                to : {
                    chatId : messageBody.chatId
                },
                date : new Date()
            };
            console.log(JSON.stringify(msgJson));
            let markdown = {};
            if(messageBody.markdown) {
                markdown = {parse_mode: 'Markdown'};
            }
            if(messageBody.type == 'image') {
                bot.say(messageBody.chatId, { attachment: 'image', url: messageBody.message })
                    .then(res => {
                        resolve();
                    })
                    .catch(err => {
                        reject(err);
                    });
            }
            else {
                bot.say(messageBody.chatId, messageBody.message)
                    .then(res => {
                        resolve();
                    })
                    .catch(err => {
                        reject(err);
                    });
            }
        }
        else {
            console.log("Unable to Send Message Body in Wrong Format");
            reject();
        }
    });
};

const port = process.env.PORT || 3000;
bot.app.get('/', (req, res) => res.send('Hello World!'));
bot.start(port);