var token = require('./credentials').tokenTelegramBot;

var Bot = require('node-telegram-bot-api');
var bot;

console.log(token);

if(process.env.NODE_ENV === 'production') {
  bot = new Bot(token);
  bot.setWebHook('https://test-for-lana.herokuapp.com/' + bot.token);
}
else {
  bot = new Bot(token, { polling: true });
}

console.log('bot server started...');

// hello command
bot.onText(/^\/say_hello (.+)$/, function (msg, match) {
  var name = match[1];
  bot.sendMessage(msg.chat.id, 'Hello ' + name + '!').then(function () {
    // reply sent!
  });
});

// sum command
bot.onText(/^\/sum((\s+\d+)+)$/, function (msg, match) {
  var result = 0;
  match[1].trim().split(/\s+/).forEach(function (i) {
    result += (+i || 0);
  })
  bot.sendMessage(msg.chat.id, result).then(function () {
    // reply sent!
  });
});

module.exports = bot;