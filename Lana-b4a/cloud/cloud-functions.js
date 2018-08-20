const destroyAllSessions = (Parse) => {
  let query = new Parse.Query(Parse.Session);

  query.find({
    success: (results) => {
      for (let session of results) {
        session.destroy({useMasterKey: true});
      }
      return true;
    },
    error: (error) => {
      return false;
    },
    useMasterKey: true
  });
};

module.exports.echo = (Parse) => { 
  return (request, response) => {
    response.success({ code: 200, message: request.params.string });
  };
};

module.exports.getUserByField = (Parse) => { 
  return (request, response) => {
    let userQuery = new Parse.Query(Parse.User);
    userQuery.equalTo(request.params.field, request.params.value);
    userQuery.first({
      success: (user) => {
        if(user != undefined) {
          response.success({ code: 200, message: user });
        }
        else
          response.error(404, "Usuario não encontrado");
      },
      error: (err) => {
        response.error(err);
      }
    });
  };
};

module.exports.setUserField = (Parse) => {
  return (request, response) => {
    let userQuery = new Parse.Query(Parse.User);
    userQuery.equalTo("objectId", request.params.userId);
    userQuery.first()
      .then(userToUpdate => {
        if(userToUpdate !== undefined) {
          userToUpdate.set(request.params.field, request.params.value);
          userToUpdate.save(null, {useMasterKey:true})
            .then(userToUpdate => {
              response.success({ code: 200, message: userToUpdate });
            })
            .catch(err => {
              response.error(err);
            });
        }
        else
          response.error(404, "Usuario não encontrado");
      })
      .catch(err => {
        response.error(err);
      });
  };
};

module.exports.unsetUserField = (Parse) => {
  return (request, response) => {
    let userQuery = new Parse.Query(Parse.User);
    userQuery.equalTo("objectId", request.params.userId);
    userQuery.first()
      .then(userToUpdate => {
        if(userToUpdate !== undefined) {
          userToUpdate.unset(request.params.field);
          userToUpdate.save(null, {useMasterKey:true})
            .then(userToUpdate => {
              response.success({ code: 200, message: userToUpdate });
            })
            .catch(err => {
              response.error(err);
            });
        }
        else
          response.error(404, "Usuario não encontrado");
      })
      .catch(err => {
        response.error(err);
      });
  };
};

module.exports.registerUser = (Parse) => {
  return (request, response) => {
    if(request.params.username == undefined ||
      request.params.password == undefined ||
      request.params.interface == undefined ||
      request.params.interfaceId == undefined ||
      request.params.name == undefined) {
        response.error(400, "Usuario precisa de username, password, interface, interfaceId e name");
    }
    let user = new Parse.User();
    user.set("username", request.params.username);
    user.set("password", request.params.password);
    user.set(request.params.interface, request.params.interfaceId);
    user.set("name", request.params.name);

    user.signUp(null)
      .then((newUser) => {
        destroyAllSessions(Parse);
        response.success({ code: 200, message: newUser });
      })
      .catch((err) => response.error(err));
  };
};

module.exports.loginUser = (Parse) => {
  return (request, response) => {
  Parse.User.logIn(request.params.username, request.params.password)
    .then((user) => {
      destroyAllSessions(Parse);
      response.success({ code: 200, message: user.toJSON() });
    })
    .catch((err) => response.error(err));
  };
};

module.exports.setContext = (Parse) => {
  return (request, response) => {
    if(request.params.interface == undefined ||
      request.params.interfaceId == undefined ||
      request.params.context == undefined) {
        response.error(400, "Precisa de interface, interfaceId e Context");
    }
    let Context = Parse.Object.extend('Context');
    let contextQuery = new Parse.Query(Context);
    let myContext = new Context();
    contextQuery.equalTo(request.params.interface, request.params.interfaceId);
    contextQuery.first()
      .then(contextToUpdate => {
        if(contextToUpdate != undefined)
          myContext = contextToUpdate;
        else
          myContext.set(request.params.interface, request.params.interfaceId);

        myContext.set("context", request.params.context);
        
        myContext.save(null)
          .then(newContext => {
            response.success({code: 200, message: newContext});
          })
          .catch(err => {
            response.error(err);
          });
      })
      .catch(err => {
        response.error(err);
    });
  };
};

module.exports.getContextByInterfaceId = (Parse) => {
  return (request, response) => {
  let Context = Parse.Object.extend('Context');
  let contextQuery = new Parse.Query(Context);
  contextQuery.equalTo(request.params.interface, request.params.interfaceId);
  contextQuery.first()
    .then(contextToFind => {
      if(contextToFind != undefined)
        response.success({code: 200, message: contextToFind.toJSON()});
      else
        response.error(404, "Context não encontrado");
    })
    .catch(err => {
      response.error(err);
    });
  };
};