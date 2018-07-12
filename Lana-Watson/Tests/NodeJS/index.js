const watson = require('watson-developer-cloud');

const conversation = new watson.ConversationV1({
  username: process.env.watson_USERNAME,
  password: process.env.watson_PASSWORD,
  version: '2018-02-16'
});

let oldContext;

conversation.message({
    workspace_id: process.env.watson_LANA_WORKSPACE_ID,
    input: {'text': ''}
  }, (err, response) => {
    if (err)
      console.error;
    else {
      console.log(JSON.stringify(response, null, 2));
      oldContext = response.context;
      conversation.message({
        workspace_id: process.env.watson_LANA_WORKSPACE_ID,
        input: {
          'text': 'sim'
        },
        context: oldContext
        }, (err, response) => {
          if (err)
            console.error;
          else {
            console.log(JSON.stringify(response, null, 2));
            oldContext = response.context;
            console.log(JSON.stringify(oldContext, null, 2));
          }
        }
      );
    }
  }
);
