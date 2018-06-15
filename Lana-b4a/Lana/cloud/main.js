Parse.Cloud.define("echo", (request, response) => {
  response.success({ code: 200, message: request.params.string });
});

const destroyAllSessions = () => {
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

Parse.Cloud.define("getUserByField", (request, response) => {
  let userQuery = new Parse.Query(Parse.User);
  userQuery.equalTo(request.params.field, request.params.value);
  userQuery.first({
    success: (user) => {
      if(user != undefined)
        response.success({ code: 200, message: user.toJSON() });
      else
        response.error(404, "Usuario não encontrado");
    },
    error: (err) => {
      response.error(404, "Usuario não encontrado");
    }
  });
});


Parse.Cloud.define("setUserField", (request, response) => {
  let userQuery = new Parse.Query(Parse.User);
  userQuery.equalTo("objectId", request.params.userId);
  userQuery.first()
    .then(userToUpdate => {
      if(userToUpdate !== undefined) {
        userToUpdate.set(request.params.field, request.params.value);
        userToUpdate.save(null, {useMasterKey:true})
        .then(userToUpdate => {
          response.success({ code: 200, message: userToUpdate.toJSON() });
        })
        .catch((err) => {
          response.error(500, "Erro ao modificar Usuario");
        });
      }
      else
        response.error(404, "Usuario não encontrado");
    })
    .catch((err) => {
      response.error(404, "Usuario não encontrado");
    });
});


Parse.Cloud.define("registerUser", (request, response) => {
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
      destroyAllSessions();
      response.success({ code: 200, message: newUser });
    })
    .catch((newUser, err) => response.error(409, "Usuario já existente"));
});

Parse.Cloud.define("loginUser", (request, response) => {
  Parse.User.logIn(request.params.username, request.params.password)
    .then((user) => {
      destroyAllSessions();
      response.success({ code: 200, message: user.toJSON() });
    })
    .catch((user, err) => response.error(401, "Usuario/Senha Incorreta"));
});
