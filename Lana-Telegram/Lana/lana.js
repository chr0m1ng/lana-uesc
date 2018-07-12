const keys = require('./config/keys');
const token = keys.tokenTelegramBot;
const url = keys.urlTelegramBot;
const urlMessageEndpoint = keys.urlMessageEndpoint;
const lana_api_key = keys.lana_api_key;
const request = require('request');

const Bot = require('node-telegram-bot-api');
let lana;

if(process.env.NODE_ENV === 'production') {
  lana = new Bot(token);
  lana.setWebHook(url + '/' + lana.token);
}
else {
  lana = new Bot(token, { polling: true });
}

console.log('lana telegram bot server started...');

lana.on('polling_error', (error) => {
  console.error(error);
})

//Any message
lana.on('message', (msg) => {
  // lana.sendMessage(msg.chat.id, 'Recebi a mensagem "' + msg.text + '" de: ' + msg.from.first_name + ' ' + msg.from.last_name);
  let msgJson = {
    interface : 'telegram',
    type : 'incoming',
    message : msg.text,
    from : {
      name : msg.from.first_name + ' ' + msg.from.last_name,
      username : msg.from.username,
      id : msg.from.id,
      chatId : msg.chat.id
    },
    date : new Date(msg.date * 1000)
  };
  console.log(JSON.stringify(msgJson));

  fowardMessageToLana(msg);
});

const fowardMessageToLana = (msg) => {
  let options = {
    method : 'POST',
    uri : 'https://lana-api.herokuapp.com/api/message',
    headers : {
      'x-api-key': lana_api_key
    },
    body : {
      interface : 'telegram',
      message : msg.text,
      user : {
        name : msg.from.first_name + " " + msg.from.last_name,
        username : msg.from.username,
        id : msg.from.id,
        chatId : msg.chat.id
      },
      messageEndpoint : urlMessageEndpoint,
    },
    json : true // Automatically stringifies the body to JSON
  };

  request(options, (err, resp, body) => {
    if (err) {
      let msgJson = {
        interface : 'telegram',
        type : 'outgoing',
        message : msg.text,
        errMessage : err,
        to : {
          chatId : msg.chat.id
        },
        date : new Date()
      };
      console.log(JSON.stringify(msgJson));
      lana.sendMessage(msg.chat.id, 'Ops, algo deu errado, tente novamente');
    }
    else {
      let msgJson = {
        interface : 'telegram',
        type : 'outgoing',
        message : body.message,
        to : {
          chatId : body.chatId
        },
        date : new Date()
      };
      console.log(JSON.stringify(msgJson));
      lana.sendMessage(body.chatId, body.message, {parse_mode: 'Markdown'});
    }
  });

  // request(options)
  //   .then((parsedBody) => { 
  //     //Lana will first respond either the final answer or ETA
  //     let msgJson = {
  //       interface : 'telegram',
  //       type : 'outgoing',
  //       message : messageBody.message,
  //       to : {
  //         chatId : messageBody.chatId
  //       },
  //       date : new Date()
  //     };
  //     console.log(JSON.stringify(msgJson));
  //     lana.sendMessage(msg.chat.id, messageBody.message, {parse_mode: 'Markdown'});
  //   })
  //   .catch(err => {
  //     let msgJson = {
  //       interface : 'telegram',
  //       type : 'outgoing',
  //       message : msg.text,
  //       errMessage : err,
  //       to : {
  //         chatId : msg.chat.id
  //       },
  //       date : new Date()
  //     };
  //     console.log(JSON.stringify(msgJson));
  //     lana.sendMessage(msg.chat.id, 'Ops, algo deu errado, tente novamente');
  // });
}

lana.sendMessageEndpoint = (messageBody) => {
  if(messageBody.chatId && messageBody.message) {
    let msgJson = {
      interface : 'telegram',
      type : 'outgoing',
      message : messageBody.message,
      to : {
        chatId : messageBody.chatId
      },
      date : new Date()
    };
    console.log(JSON.stringify(msgJson));
    if(messageBody.parse_mode)
      lana.sendMessage(messageBody.chatId, messageBody.message, {parse_mode: messageBody.parse_mode});
    else
      lana.sendMessage(messageBody.chatId, messageBody.message, {parse_mode});
    return true;
  }
  else {
    console.log("Unable to Send Message Body in Wrong Format");
    return false;
  }
}

module.exports = lana;