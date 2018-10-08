# Adding new BOT
To add a brand new bot on Lana your bot must be indexed in one BotHub that obey Lana's request-response pattern. You can create a new BotHub or use one that already exists, like:
- BotHub UESC

## BotHub Request-Response IDL

BotHub UESC keep the same pattern as Lana for bots requests and responses and my advice is to do the same in case you need to create other BotHubs. 

### Requests Pattern
Lana will send requests to the BotHub with the following pattern:

```json
{
    "service" : "serviceName", 
    "params" : {
        "paramName" : "paramValue",
        "otherName" : "otherValue"
    }
}
```

The BotHub will forward the request to the bot that will resolve the service. Params are not always needed, as you can see on the examples bellow.

#### Examples:

Request to BotHub UESC for current schedule from Sagres:
```json
{
    "service" : "Sagres_Listar_Horarios_Corrente", 
    "params" : {
        "sagres_username" : "lana",
        "sagres_password" : "1234"
    }
}
```

Request to BotHub UESC for latests news on UESC:
```json
{
    "service" : "UESC_Listar_Noticias_Recentes"
}
```

### Response Pattern

The BotHub will receive some response from one Bot and will return to Lana the final message of a service with the following patterns:

- If the service was executed with no erros and the message don't have any markdown style:
```json
{
    "response" : "message",
    "type" : "type_of_message_like_text_or_image"
}
```

- If the service was executed with no errors and the message HAVE markdown style:
```json
{
    "response" : "message with markdown",
    "type" : "text",
    "markdown" : true
}
```

- if an error occurred while running the service by some wrong input information:
```json
{
    "response" : "message",
    "type" : "text",
    "inputError" : true,
    "inputs" : [
        {"param" : "name", "value" : "value"},
        {"param" : "other name", "value" : "other value"}
    ]
}
```

#### Examples:
Image as response and no errors:
```json
{
    "response" : "https://goo.gl/ohjpt7",
    "type" : "image"
}
```

Message as response and no errors:
```json
{
    "response" : "The answer is 42",
    "type" : "text"
}
```

Internal error, inputs are fine:
```json
{
    "response" : "Ops... Think I might be broken",
    "type" : "text"
}
```

Message with markdown:
```json
{
    "response" : "You should read the [documentation](https://en.wikipedia.org/wiki/RTFM).",
    "type" : "text",
    "markdown" : true
}
```

Input error, like wrong username or password:
```json
{
    "response" : "Looks like someone doesn't know the password anymore...",
    "type" : "text",
    "inputError" : true,
    "inputs" : [
        {"param" : "sagres_username", "value" : "lana"},
        {"param" : "sagres_password", "value" : "1234"}
    ]
}
```

# That's all folks!