import json
import os
import watson_developer_cloud

conversation = watson_developer_cloud.ConversationV1(
    username=os.environ['watson_USERNAME'],
    password=os.environ['watson_PASSWORD'],
    version='2018-02-16'
)

response = conversation.message(
    workspace_id=os.environ['watson_LANA_WORKSPACE_ID'],
    input={
        'text': ''
    }
)
print(json.dumps(response, indent=2))

mycontext = response['context']

response = conversation.message(
    workspace_id=os.environ['watson_LANA_WORKSPACE_ID'],
    input={
        'text': 'sim'
    },
    context=mycontext
)

print(json.dumps(response, indent=2))
