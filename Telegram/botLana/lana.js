const token = require('./credentials').tokenTelegramBot;

const Bot = require('node-telegram-bot-api');
let lana;

console.log(token);

if(process.env.NODE_ENV === 'production') {
  lana = new Bot(token);
  lana.setWebHook('https://lana-telegram-bot.herokuapp.com/' + lana.token);
}
else {
  lana = new Bot(token, { polling: true });
}

console.log('lana telegram bot server started...');

//Any message
lana.on('message', (msg) => {
  lana.sendMessage(msg.chat.id, 'Recebi a mensagem "' + msg.text + '" de: ' + msg.from.first_name + ' ' + msg.from.last_name);
  
  let msgJson = {
    "from" : {
      "first_name" : msg.from.first_name,
      "last_name" : msg.from.last_name,
      "username" : msg.from.username
    },
    "date" : new Date(msg.date * 1000),
    "message" : msg.text
  };
  
  console.log("++++++ START OF MESSAGE ++++++\n" + JSON.stringify(msgJson, null, ' ') + "\n------ END OF MESSAGE ------\n");
});

module.exports = lana;