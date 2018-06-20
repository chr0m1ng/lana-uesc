const Parse = require('parse/node');
const constants = require('./constants');
const cloud_functions = require('../cloud/cloud-functions');
Parse.initialize(constants.APPLICATION_ID, constants.JAVASCRIPT_KEY, constants.MASTER_KEY);

Parse.serverURL = constants.SERVER_URL;

let registerUser = cloud_functions.registerUser(Parse);
let loginUser = cloud_functions.loginUser(Parse);
let getUserByField = cloud_functions.getUserByField(Parse);
let setUserField = cloud_functions.setUserField(Parse);
let purgeTable = require("./utils/purge-parse-table")(Parse);
let ResponseStub = require("./utils/response-stub");

jasmine.DEFAULT_TIMEOUT_INTERVAL = 10000;

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
        registerUser({
            params : {
                name : "John",
                username : "jdoe1",
                password : "SecretCatchphrase1",
                interface : "telegramId",
                interfaceId : "someTelegramIdHere1"
                }
            },
            responseStub.getStub()
        );
        responseStub.onComplete()
            .then((resp) => {
                let userQ =  new Parse.Query(Parse.User);
                userQ.equalTo("telegramId", "someTelegramIdHere1");
                userQ.first({useMasterKey : true})
                    .then(user => expect(user.getUsername()).toBe("jdoe1"))
                    .catch((e) => {
                        console.log(e);
                        fail(e);
                    })
                    .then(() => done());
            })
            .catch((e) => {
                console.log(e);
                fail(e);
            })
            .then(() => done());
    });
});

describe("loginUser", () => {
    beforeEach((done) => {
        /// purge the user, and then proceed
        Promise.all([purgeTable("User")])
            .catch((e) => fail(e))
            .then(() => done());
    });
    it ("Deve aceitar login", (done) => {
        let responseStub = new ResponseStub();
        registerUser({
            params : {
                name : "John",
                username : "jdoe2",
                password : "123",
                interface : "telegramId",
                interfaceId : "someTelegramIdHere2"
                }
            },
            responseStub.getStub()
        );
        responseStub.onComplete()
            .then((resp) => {
                let otherResponseStub = new ResponseStub();
                loginUser({
                    params : {
                        username : "jdoe2",
                        password : "123"
                    }
                }, otherResponseStub.getStub());
                otherResponseStub.onComplete()
                    .then((resp) => {
                        expect(resp.code).toBe(200);
                    })
                    .catch((e) => {
                        console.log(e);
                        fail(e);
                    })
                    .then(() => done());
            })
            .catch((e) => {
                console.log(e);
                fail(e);
            })
            .then(() => done());
    });
    it ("Deve rejeitar um request para logar usuario com username/password incorreta", (done) => {
        let responseStub = new ResponseStub();
        responseStub.onComplete()
            .then(() => fail("Deve falhar devido aos parametros invalidos"))
            .catch((e) => {})
            .then(() => done());

        loginUser({ 
            params : {
                username : "jdoe1",
                password : "any"
            }
        }, responseStub.getStub());
    });
});

describe("getUserByField", () => {
    beforeEach((done) => {
        /// purge the user, and then proceed
        Promise.all([purgeTable("User")])
            .catch((e) => fail(e))
            .then(() => done());
    });
    it ("Deve falhar ao procurar um usuario com o campo/valor inexistente", (done) => {
        let responseStub = new ResponseStub();
        responseStub.onComplete()
            .then(() => fail("Deve falhar devido a campo e valor inexistente"))
            .catch((e) => {})
            .then(() => done());

        getUserByField({ 
            params : {
                field : "telegramId",
                value : "any"
            }
        }, responseStub.getStub());
    });
    it ("Deve retornar usuario com o campo e valor informado", (done) => {
        let responseStub = new ResponseStub();
        registerUser({
            params : {
                name : "John",
                username : "jdoe3",
                password : "123",
                interface : "telegramId",
                interfaceId : "111"
                }
        }, responseStub.getStub());
        responseStub.onComplete()
            .then((resp) => {
                let otherResponseStub = new ResponseStub();
                getUserByField({
                    params : {
                        field : "telegramId",
                        value : "111"
                    }
                }, otherResponseStub.getStub());
                otherResponseStub.onComplete()
                    .then((otherResp) => {
                        expect(otherResp.message.getUsername()).toBe("jdoe3");
                    })
                    .catch((e) => {
                        console.log(e);
                        fail(e);
                    })
                    .then(() => done());
            })
            .catch((e) => {
                console.log(e);
                fail(e);
            })
            .then(() => done());
    });
});

describe("setUserField", () => {
    beforeEach((done) => {
        /// purge the user, and then proceed
        Promise.all([purgeTable("User")])
            .catch((e) => fail(e))
            .then(() => done());
    });
    it ("Deve falhar ao procurar um usuario com o id inexistente", (done) => {
        let responseStub = new ResponseStub();
        responseStub.onComplete()
            .then(() => fail("Deve falhar devido a id inexistente"))
            .catch((e) => {})
            .then(() => done());

        setUserField({ 
            params : {
                userId : "inexistent",
                field : "telegramId",
                value : "any"
            }
        }, responseStub.getStub());
    });
    it ("Deve retornar usuario com o campo e valor modificado", (done) => {
        let responseStub = new ResponseStub();
        registerUser({
            params : {
                name : "John",
                username : "jdoe4",
                password : "123",
                interface : "telegramId",
                interfaceId : "222"
            }
        }, responseStub.getStub());
        responseStub.onComplete()
            .then((resp) => {
                let otherResponseStub = new ResponseStub();
                setUserField({
                    params : {
                        userId : resp.message.id,
                        field : "telegramId",
                        value : "333"
                    }
                }, otherResponseStub.getStub());
                otherResponseStub.onComplete()
                    .then((respUser) => {
                        expect(respUser.message.get("telegramId")).toBe("333");
                    })
                    .catch((e) => {
                        console.log(e);
                        fail(e);
                    })
                    .then(() => done());
            })
            .catch((e) => {
                console.log(e);
                fail(e);
            })
            .then(() => done());
    });
});