const token = require('./credentials').tokenTelegramBot;
const url = require('./credentials').urlTelegramBot;
const urlMessageEndpoint = require('./credentials').urlMessageEndpoint;
const request = require('request-promise');

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

//Any message
lana.on('message', (msg) => {
  lana.sendMessage(msg.chat.id, 'Recebi a mensagem "' + msg.text + '" de: ' + msg.from.first_name + ' ' + msg.from.last_name);
  
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
  console.log("++++++ START OF MESSAGE ++++++\n" + JSON.stringify(msgJson, null, ' ') + "\n------ END OF MESSAGE ------\n");

  fowardMessageToLana(msg);
});

const fowardMessageToLana = async (msg) => {
  let options = {
    method : 'POST',
    uri : 'http://httpbin.org/post',
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

  await request(options)
    .then((parsedBody) => { 
      //Lana will first respond either the final answer or ETA, I also need to log that.
      lana.sendMessage(msg.chat.id, 'Requisição Feita com Sucesso');
    })
    .catch((err) => {
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
      lana.sendMessage(message.chat.id, 'Ops, algo deu errado, tente novamente');
  });
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
    console.log("++++++ START OF MESSAGE ++++++\n" + JSON.stringify(msgJson, null, ' ') + "\n------ END OF MESSAGE ------\n");
    lana.sendMessage(messageBody.chatId, messageBody.message);
    return true;
  }
  else {
    console.log("Unable to Send Message Body in Wrong Format");
    return false;
  }
}

module.exports = lana;