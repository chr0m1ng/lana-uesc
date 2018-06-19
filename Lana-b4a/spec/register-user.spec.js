const Parse = require('parse/node');
const constants = require('./constants');

Parse.initialize(constants.APPLICATION_ID, constants.JAVASCRIPT_KEY, constants.MASTER_KEY);

Parse.serverURL = constants.SERVER_URL;

let registerUser = require('../cloud/cloud-functions').registerUser(Parse);
let purgeTable = require("./utils/purge-parse-table")(Parse);
let ResponseStub = require("./utils/response-stub");

describe("registerUser", () => {
    beforeEach((done) => {
        /// purge the user, and then proceed
        Promise.all([purgeTable("User")])
            .catch((e) => fail(e))
            .then(() => done());
    });
    it ("Deve rejeitar um request para registar usuario que não contem todos os parametros", (done) => {
        let responseStub = new ResponseStub();
        responseStub.onComplete()
            .then(() => fail("Deve falhar devido aos parametros invalidos"))
            .catch((e) => {})
            .then(() => done());

        registerUser({ params : {}}, responseStub.getStub());
    });
    it ("Deve registrar um usuario", (done) => {
        let responseStub = new ResponseStub();
        let stub = responseStub.getStub();
        registerUser({
            params : {
                name : "John",
                username : "jdoe1",
                password : "SecretCatchphrase1",
                interface : "telegramId",
                interfaceId : "someTelegramIdHere1"
                },
            },
            stub
        );
        responseStub.onComplete()
            .then((resp) => {
                let userQ =  new Parse.Query(Parse.User);
                userQ.equalTo("telegramId", "someTelegramIdHere1");
                return userQ.first({useMasterKey : true});
            })
            .then((user) => {
                expect(user.getUsername()).toBe("jdoe1");
            })
            .catch((e) => {
                console.log(e);
                fail(e);
            })
            .then(() => done());
      });
  });