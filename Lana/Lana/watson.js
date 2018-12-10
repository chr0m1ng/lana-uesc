class Watson {}
const keys = require("./config/keys");
const AssistantV1 = require("watson-developer-cloud/assistant/v1");
const watson_assistant = new AssistantV1({
  username: keys.watson_username,
  password: keys.watson_password,
  url: "https://gateway.watsonplatform.net/assistant/api/",
  version: keys.watson_version
});

let watsonAPI = new Watson();

watsonAPI.sendMessageToWatson = (message, context, intent = null) => {
  return new Promise((resolve, reject) => {
    context["timezone"] = "America/Sao_Paulo";
    if (intent == null) {
      watson_assistant.message(
        {
          workspace_id: keys.watson_workspace_id,
          input: {
            text: message
          },
          context: context
        },
        (err, res) => {
          if (err) reject(err);
          else resolve(res);
        }
      );
    } else {
      watson_assistant.message(
        {
          workspace_id: keys.watson_workspace_id,
          input: {
            text: message
          },
          context: context,
          intents: [
            {
              intent: intent,
              confidence: 1
            }
          ]
        },
        (err, res) => {
          if (err) {
            reject(err);
          } else {
            resolve(res);
          }
        }
      );
    }
  });
};

watsonAPI.sendIntentToWatson = (intent, context = {}) => {
  return new Promise((resolve, reject) => {
    watson_assistant.message(
      {
        workspace_id: keys.watson_workspace_id,
        intents: [
          {
            intent: intent,
            confidence: 1
          }
        ],
        context: context
      },
      (err, res) => {
        if (err) reject(err);
        else resolve(res);
      }
    );
  });
};

module.exports = watsonAPI;
