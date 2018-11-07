const keys = require("./config/keys");
const token = keys.tokenTelegramBot;
const url = keys.urlTelegramBot;
const urlMessageEndpoint = keys.urlMessageEndpoint;
const lana_api_key = keys.lana_api_key;
const request = require("request");

const Bot = require("tgfancy");
let lana;

if (process.env.NODE_ENV === "production") {
  lana = new Bot(token);
  lana.setWebHook(url + "/" + lana.token);
} else {
  lana = new Bot(token, { polling: true });
}

console.log("lana telegram bot server started...");

lana.on("polling_error", error => {
  console.error(error);
});

//Any message
lana.on("message", msg => {
  // lana.sendMessage(msg.chat.id, 'Recebi a mensagem "' + msg.text + '" de: ' + msg.from.first_name + ' ' + msg.from.last_name);
  let msgJson = {
    interface: "telegram",
    type: "incoming",
    message: msg.text,
    from: {
      name: msg.from.first_name + " " + msg.from.last_name,
      username: msg.from.username,
      id: msg.from.id,
      chatId: msg.chat.id
    },
    date: new Date(msg.date * 1000)
  };
  console.log(JSON.stringify(msgJson));

  fowardMessageToLana(msg);
});

const fowardMessageToLana = msg => {
  let options = {
    method: "POST",
    uri: "https://lana-api.herokuapp.com/api/message",
    headers: {
      "x-api-key": lana_api_key
    },
    body: {
      interface: "telegram",
      message: msg.text,
      user: {
        name: `${msg.from.first_name} ${msg.from.last_name}`,
        username: msg.from.username,
        id: msg.from.id,
        chatId: msg.chat.id
      },
      messageEndpoint: urlMessageEndpoint
    },
    json: true // Automatically stringifies the body to JSON
  };

  request(options, (err, resp, body) => {
    if (!resp || resp.statusCode != 200 || err) {
      let msgJson = {
        interface: "telegram",
        type: "outgoing",
        message: msg.text,
        errMessage: err,
        to: {
          chatId: msg.chat.id
        },
        date: new Date()
      };
      console.log(JSON.stringify(msgJson));
      lana.sendMessage(msg.chat.id, "Ops, algo deu errado, tente novamente");
    } else {
      let msgJson = {
        interface: "telegram",
        type: "outgoing",
        message: body.message,
        to: {
          chatId: body.chatId
        },
        date: new Date()
      };
      console.log(JSON.stringify(msgJson));
      let markdown = {};
      if (body.markdown) {
        markdown = { parse_mode: "Markdown" };
      }
      if (body.message != undefined) {
        lana.sendMessage(body.chatId, body.message, markdown);
      } else {
        lana.sendMessage(body.chatId, "Ops, algo deu errado, tente novamente");
      }
    }
  });
};

lana.sendMessageEndpoint = messageBody => {
  return new Promise((resolve, reject) => {
    if (messageBody.chatId != undefined && messageBody.message != undefined) {
      let msgJson = {
        interface: "telegram",
        type: "outgoing",
        message: messageBody.message,
        to: {
          chatId: messageBody.chatId
        },
        date: new Date()
      };
      console.log(JSON.stringify(msgJson));
      let markdown = {};
      if (messageBody.markdown) {
        markdown = { parse_mode: "Markdown" };
      }
      if (messageBody.type == "image") {
        lana
          .sendPhoto(messageBody.chatId, messageBody.message, markdown)
          .then(res => {
            resolve();
          })
          .catch(err => {
            reject(err);
          });
      } else {
        lana
          .sendMessage(messageBody.chatId, messageBody.message, markdown)
          .then(res => {
            resolve();
          })
          .catch(err => {
            reject(err);
          });
      }
    } else {
      console.log("Unable to Send Message Body in Wrong Format");
      reject();
    }
  });
};

module.exports = lana;
