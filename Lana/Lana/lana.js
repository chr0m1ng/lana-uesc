class Lana {}
const watson_api = require('./watson');
const b4a = require('./b4a');
let lana = new Lana();

const handleWatsonAnswer = answer => {
    return new Promise((resolve, reject) => {
        resolve('message handled');
    });
};

const handleMessage = message_body => {
    return new Promise((resolve, reject) => {
        const interface = message_body.interface;
        const message = `${message_body.message}`;
        const user = message_body.user;
        const interfaceId = `${user.id}`;
        b4a.getUserContext(interface, interfaceId)
            .then(user_context => { //Context existente
                watson_api.sendMessageToWatson(message, user_context) //Manda a mensagem com o context anterior que o watson sabe oq fazer
                    .then(watson_answer => {
                        handleWatsonAnswer(watson_answer)
                            .then(lana_message => {
                                const msgJson = {
                                    message : lana_message,
                                    chatId : interfaceId
                                };
                                resolve(msgJson); //A lana cuidou do que deveria ser feito, basta mandar a mensagem de volta para o usuario
                            })
                            .catch(lana_err => reject(lana_err)); //Erro com a Lana
                    })
                    .catch(watson_err => reject(watson_err)); //Erro com o watson
            })
            .catch(context_err => { //Context não existe, usuario existente?
                if(context_err.code == 404) {
                    b4a.getUser(interface, interfaceId)
                        .then(user => { //Usuario existente porem sem context (como??), melhor salvar novo context e seguir normalmente
                            watson_api.sendMessageToWatson(message, {}) //Mensagem sem contexto anterior...
                                .then(watson_answer => {
                                    handleWatsonAnswer(watson_answer)
                                        .then(lana_message => {
                                            const msgJson = {
                                                message : lana_message,
                                                chatId : interfaceId
                                            };
                                            resolve(msgJson); //A lana cuidou do que deveria ser feito, basta mandar a mensagem de volta para o usuario
                                        })
                                        .catch(lana_err => reject(lana_err)); //Erro com a Lana
                                })
                                .catch(watson_err => reject(watson_err)); //Erro com o watson
                        })
                        .catch(user_err => { //Novo Usuario
                            watson_api.sendMessageToWatson('', {}) //Watson deve responder mensagem para novo usuario
                                .then(watson_answer => {
                                    b4a.setUserContext(interface, interfaceId, watson_answer.context)
                                        .then(savedContext => { //Salvou o context no b4a
                                            const msgJson = {
                                                message : watson_answer.output.text[0],
                                                chatId : interfaceId
                                            };
                                            resolve(msgJson); //Novo usuario nunca mandou mensagem nenhuma, só enviar resposta de volta e salvar estado
                                        })
                                        .catch(set_context_err => reject(set_context_err)); //Erro com o b4a
                                })
                                .catch(watson_err => reject(watson_err)); //Erro com o watson
                        });
                }
            });
    });
};

lana.recvMessage = message_body => {
    return new Promise((resolve, reject) => {
        handleMessage(message_body)
            .then(lana_message => resolve(lana_message)) //Tudo ok com a lana
            .catch(lana_err => reject(lana_err)); //Erro ao tratar mensagem
    });
}

module.exports = lana;