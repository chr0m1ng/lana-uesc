class Lana {}
const request = require('request');
const watson_api = require('./watson');
const b4a = require('./b4a');
const bothubs = require('./config/bothubs');
const bothubs_keys = require('./config/keys').bothub_keys;

const lana = new Lana();

const sendFinalMessageToEndPoint = (message, endpoint, user, type='text', markdown=false) => {
    const options = {
        method : 'POST',
        uri : endpoint,
        body : {
            'message' : message,
            'type' : type,
            'markdown' : markdown,
            'chatId' : `${user.id}`
        },
        json : true
    };
    request(options, (err, resp, body) => {
        console.log(body);
    });
};

const createNewUserAndProvideFeedBack = (context, message_body) => {
    const interface = message_body.interface;
    const user = message_body.user;
    const interfaceId = `${user.id}`;
    b4a.newUser(context.username.substring(1), context.password.substring(1), interface, interfaceId, user.name)
            .then(created_user => {
                b4a.setUserContext(interface, interfaceId, {}) //Usuario Criado, vou zerar o context dele no b4a
                    .then(saved_context => {
                        sendFinalMessageToEndPoint('Pronto, seu usuario foi criado com sucesso, já podemos conversar', message_body.messageEndpoint, user);
                    })
                    .catch(set_context_err => {
                        sendFinalMessageToEndPoint('Ops, não estou conseguindo lidar com isso agora... Tente novamente mais tarde', message_body.messageEndpoint, user);
                    });
            })
            .catch(new_user_err => { //Erro ao criar usuario, verificar se foi erro de usuario já existente
                if(new_user_err.code == 141) { //Username já está em uso, precisa jogar usuario para intent Usuario_Registrar_Existente
                    watson_api.sendIntentToWatson('Usuario_Registrar_Existente') //Manda intent de usuario existente pro watson
                        .then(watson_answer => {
                            b4a.setUserContext(interface, interfaceId, watson_answer.context) //Salva novo contexto com erro de registro de usuario e manda mensagem avisando
                                .then(saved_context => {
                                    sendFinalMessageToEndPoint(watson_answer.output.text[0], message_body.messageEndpoint, user);
                                })
                                .catch(set_context_err => {
                                    sendFinalMessageToEndPoint('Ops, não estou conseguindo lidar com isso agora... Tente novamente mais tarde', message_body.messageEndpoint, message_body.user);
                                });
                        })
                        .catch(watson_err => {
                            sendFinalMessageToEndPoint('Ops, não estou conseguindo lidar com isso agora... Tente novamente mais tarde', message_body.messageEndpoint, message_body.user);                
                        });
                }
                else
                    sendFinalMessageToEndPoint('Ops, não estou conseguindo lidar com isso agora... Tente novamente mais tarde', message_body.messageEndpoint, message_body.user);
            });            
};

const handleNewLanaUser = (answer, message_body) => {
    return new Promise(async (resolve, reject) => {
        const context = answer.context;
        const interface = message_body.interface;
        const user = message_body.user;
        const interfaceId = `${user.id}`;
        await createNewUserAndProvideFeedBack(context, message_body); //Mando executar a função de criar novo usuario e sigo sem esperar ela acabar
        b4a.setUserContext(interface, interfaceId, context) //Atualizo o context e retorno o feedBack de espera padrão da lana
            .then(saved_context => {
                resolve(answer.output.text[0]);
            })
            .catch(set_context_err => reject(set_context_err));
    });
};

const authUserAndProvideFeedBack = (context, message_body) => {
    const interface = message_body.interface;
    const user = message_body.user;
    const interfaceId = `${user.id}`;
    b4a.checkUserCredentials(context.username.substring(1), context.password.substring(1))
        .then(logged_user => {
            b4a.setUserProp(logged_user.objectId, interface, interfaceId)
                .then(setted_prop => {
                    b4a.setUserContext(interface, interfaceId, {}) //Usuario Logado, vou zerar o context dele no b4a
                        .then(saved_context => {
                            sendFinalMessageToEndPoint('Pronto, consegui te localizar nos meus contatos... Já podemos conversar', message_body.messageEndpoint, user);
                        })
                        .catch(set_context_err => {
                            sendFinalMessageToEndPoint('Ops, não estou conseguindo lidar com isso agora... Tente novamente mais tarde', message_body.messageEndpoint, user);
                        });
                })
                .catch(set_prop_err => {
                    sendFinalMessageToEndPoint('Ops, não estou conseguindo lidar com isso agora... Tente novamente mais tarde', message_body.messageEndpoint, user);
                });
        })
        .catch(auth_user_err => {
            if(auth_user_err.code == 141) { //Usuario ou senha incorreta
                watson_api.sendIntentToWatson('Usuario_Entrar_Incorreto') //Manda intent de usuario/senha incorreto pro watson
                    .then(watson_answer => {
                        b4a.setUserContext(interface, interfaceId, watson_answer.context) //Salva novo contexto com erro de login de usuario e manda mensagem avisando
                            .then(saved_context => {
                                sendFinalMessageToEndPoint(watson_answer.output.text[0], message_body.messageEndpoint, user);
                            })
                            .catch(set_context_err => {
                                sendFinalMessageToEndPoint('Ops, não estou conseguindo lidar com isso agora... Tente novamente mais tarde', message_body.messageEndpoint, message_body.user);
                            });
                    })
                    .catch(watson_err => {
                        sendFinalMessageToEndPoint('Ops, não estou conseguindo lidar com isso agora... Tente novamente mais tarde', message_body.messageEndpoint, message_body.user);                
                    });
            }
            else
                sendFinalMessageToEndPoint('Ops, não estou conseguindo lidar com isso agora... Tente novamente mais tarde', message_body.messageEndpoint, message_body.user);
        });
};

const handleLoginUser = (answer, message_body) => {
    return new Promise(async (resolve, reject) => {
        const context = answer.context;
        const interface = message_body.interface;
        const user = message_body.user;
        const interfaceId = `${user.id}`;
        await authUserAndProvideFeedBack(context, message_body); //Mando executar a função de logar usuario e sigo sem esperar ela acabar
        b4a.setUserContext(interface, interfaceId, context) //Atualizo o context e retorno o feedBack de espera padrão da lana
            .then(saved_context => {
                resolve(answer.output.text[0]);
            })
            .catch(set_context_err => reject(set_context_err));
    });
};

const handleNewUserInfo = (answer, message_body) => {
    return new Promise(((resolve, reject) => {
        const context = answer.context;
        const interface = message_body.interface;
        const user = message_body.user;
        const interfaceId = `${user.id}`;
        b4a.getUser(interface, interfaceId)
            .then(lana_user => {
                context.new_user_info.forEach(info => {
                    b4a.setUserProp(lana_user.id, info, context[info])
                        .then(setted_prop => {
                            const disgress = () => {
                                return new Promise((resolve, reject) => {
                                    //Vou zerar coisas do context
                                    context.go_back = null;
                                    context.intent = null;
                                    context.new_user_info = null; //Removo new_user_info pois já foi resolvido
                                    watson_api.sendIntentToWatson(context.disgress_from, context)
                                        .then(watson_answer => {
                                            handleWatsonAnswer(watson_answer, message_body)
                                                .then(lana_message => resolve(lana_message))
                                                .catch(lana_err => reject(lana_err));
                                        })
                                        .catch(watson_err => reject(watson_err));
                                });
                            };

                            const just_save = () => {
                                b4a.setUserContext(interface, interfaceId, context) //Atualizo o context e retorno o feedBack de espera padrão da lana
                                    .then(saved_context => {
                                        resolve(answer.output.text[0]);
                                    })
                                    .catch(set_context_err => reject(set_context_err));
                            };
                            const result = context.go_back == true ? disgress() : just_save(); //Deve voltar para um intent especifico ou somente salvar
                            resolve(result);
                        })
                        .catch(set_prop_err => reject(set_prop_err));
                });
            })
            .catch(get_user_err => reject(get_user_err));
    }));
};

const handleLocateUserInfo = (answer, message_body) => {
    return new Promise((resolve, reject) => {
        const interface = message_body.interface;
        const user = message_body.user;
        const interfaceId = `${user.id}`;
        b4a.getUser(interface, interfaceId) //Vou buscar o usuario no b4a
        .then(lana_user => {
            answer.context.needs.forEach(info => { //Vou verificar tudo que preciso buscar do usuario, caso já tenha no b4a eu seto no context
                if(lana_user.get(info) != null) 
                    answer.context[info] = lana_user.get(info);
            });
            //Apos setar informações no context eu replico a mensagem ao watson com o novo context
            watson_api.sendMessageToWatson(message_body.message, answer.context) //Mensagem reenviada junto ao context modificado
                .then(watson_answer => {
                    if(watson_answer.context.search_info_first != null) //Mesmo com novo context ainda necessita de outras informações que não estão no b4a
                        watson_answer.context.search_info_first = false; //Caso não achou as infos no b4a então não precisa buscar de novo
                    handleWatsonAnswer(watson_answer, message_body) //Vou voltar a tentar resolver a mensagem, desta vez não entrará aqui novamente
                        .then(lana_message => resolve(lana_message))
                        .catch(lana_err => reject(lana_err));
                })
                .catch(watson_err => reject(watson_err));
        })
        .catch(get_user_err => reject(get_user_err));
    });
};

const startServiceAndProvideFeedback = (bothub, service, params, endpoint, user, interface) => {
    const options = {
        method : 'POST',
        uri : bothubs[bothub],
        headers : {
            'x-api-key': bothubs_keys[bothub]
        },
        body : {
            'service' : service,
            'params' : params
        },
        json : true
    };
    request(options, (err, resp, body) => {
        if (!resp || resp.statusCode != 200 || err) { //Erro ao executar serviço
            const bothub_err = {
                'bothub' : bothub,
                'service' : service,
                'params' : params,
                'user' : user,
                'body' : body
            };
            console.error(JSON.stringify(bothub_err, null, ' '));
            sendFinalMessageToEndPoint('Ops, não estou conseguindo lidar com isso agora... Tente novamente mais tarde', endpoint, user);
        }
        else {
            if(body.inputError == true) {
                const interfaceId = `${user.id}`;
                b4a.getUser(interface, interfaceId)
                    .then(lana_user => {
                        body.inputs.forEach(info => {
                            b4a.unsetUserProp(lana_user.id, info.param)
                                .catch(err => {
                                    sendFinalMessageToEndPoint('Ops, não estou conseguindo lidar com isso agora... Tente novamente mais tarde', endpoint, user);
                                });
                        });
                    })
                    .catch(err => {
                        sendFinalMessageToEndPoint('Ops, não estou conseguindo lidar com isso agora... Tente novamente mais tarde', endpoint, user);
                    });
            }
            sendFinalMessageToEndPoint(body.response, endpoint, user, body.type); //Retorna resposta do serviço ao usuario
        }
    });
};

const handleService = (answer, message_body) => {
    return new Promise(async (resolve, reject) => {
        const interface = message_body.interface;
        const user = message_body.user;
        const interfaceId = `${user.id}`;
        const endpoint = message_body.messageEndpoint;
        const context = answer.context;
        let params = {};
        context.needs.forEach(info => { //Salvo os parametros necessarios em params para passar pro bothub executar o servico
            params[info] = context[info];
            context[info] = null; //Zero os parametros para não interferir em proximos serviços
        });
        startServiceAndProvideFeedback(context.bothub, context.intent, params, endpoint, user, interface); //Mando iniciar o servico e sigo em frente sem esperar acabar
        context.bothub = null; //Zera pedido de serviço pra não refazer chamadas
        context.intent = null;
        b4a.setUserContext(interface, interfaceId, context) //Atualizo o context e retorno o feedBack de espera padrão da lana
            .then(saved_context => {
                resolve(answer.output.text[0]);
            })
            .catch(set_context_err => reject(set_context_err));
    });
};

const handleWatsonAnswer = (answer, message_body) => {
    return new Promise((resolve, reject) => {
        const interface = message_body.interface;
        const user = message_body.user;
        const interfaceId = `${user.id}`;
        //Aqui teremos alguns tratamentos especiais
        if(answer.context.intent == 'Usuario_Registrar') { //Novo usuario da lana
            handleNewLanaUser(answer, message_body)
                .then(lana_message => resolve(lana_message))
                .catch(lana_err => reject(lana_err));
        }
        else if(answer.context.intent == 'Usuario_Entrar') { //Usuario antigo logando na lana
            handleLoginUser(answer, message_body)
                .then(lana_message => resolve(lana_message))
                .catch(lana_err => reject(lana_err));
        }
        else if(answer.context.new_user_info != null) { //Salvar uma informação do usuario
            handleNewUserInfo(answer, message_body)
                .then(lana_message => resolve(lana_message))
                .catch(lana_err => reject(lana_err));
        }
        else if(answer.context.search_info_first == true) { //Buscar por informações do usuario para realizar um serviço
            handleLocateUserInfo(answer, message_body)
                .then(lana_message => resolve(lana_message))
                .catch(lana_err => reject(lana_err));
        }
        else if(answer.context.bothub != null) { //Precisa chamar serviço de algum botHUB
            handleService(answer, message_body)
                .then(lana_message => resolve(lana_message))
                .catch(lana_err => reject(lana_err));
        }
        else { //Qualquer outro
            b4a.setUserContext(interface, interfaceId, answer.context)
                .then(saved_context => {
                    resolve(answer.output.text[0]);
                })
                .catch(set_context_err => reject(set_context_err));
        }
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
                        handleWatsonAnswer(watson_answer, message_body)
                            .then(lana_message => {
                                const msg_json = {
                                    message : lana_message,
                                    chatId : interfaceId
                                };
                                resolve(msg_json); //A lana cuidou do que deveria ser feito, basta mandar a mensagem de volta para o usuario
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
                                    handleWatsonAnswer(watson_answer, message_body)
                                        .then(lana_message => {
                                            const msg_json = {
                                                message : lana_message,
                                                chatId : interfaceId
                                            };
                                            resolve(msg_json); //A lana cuidou do que deveria ser feito, basta mandar a mensagem de volta para o usuario
                                        })
                                        .catch(lana_err => reject(lana_err)); //Erro com a Lana
                                })
                                .catch(watson_err => reject(watson_err)); //Erro com o watson
                        })
                        .catch(user_err => { //Novo Usuario
                            watson_api.sendMessageToWatson('', {}) //Watson deve responder mensagem para novo usuario
                                .then(watson_answer => {
                                    b4a.setUserContext(interface, interfaceId, watson_answer.context)
                                        .then(saved_context => { //Salvou o context no b4a
                                            const msg_json = {
                                                message : watson_answer.output.text[0],
                                                chatId : interfaceId
                                            };
                                            resolve(msg_json); //Novo usuario nunca mandou mensagem nenhuma, só enviar resposta de volta e salvar estado
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