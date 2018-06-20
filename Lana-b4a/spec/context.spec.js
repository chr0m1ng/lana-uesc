const Parse = require('parse/node');
const constants = require('./constants');
const cloud_functions = require('../cloud/cloud-functions');
Parse.initialize(constants.APPLICATION_ID, constants.JAVASCRIPT_KEY, constants.MASTER_KEY);

Parse.serverURL = constants.SERVER_URL;

let setContext = cloud_functions.setContext(Parse);
let getContextByInterfaceId = cloud_functions.getContextByInterfaceId(Parse);
let purgeTable = require("./utils/purge-parse-table")(Parse);
let ResponseStub = require("./utils/response-stub");

jasmine.DEFAULT_TIMEOUT_INTERVAL = 10000;

describe("setContext", () => {
    beforeEach(done => {
        /// purge the user, and then proceed
        Promise.all([purgeTable("Context")])
            .catch((e) => fail(e))
            .then(() => done());
    });
    
    it ("Deve rejeitar um request para registar Context que não contem todos os parametros", done => {
        let responseStub = new ResponseStub();
        setContext({params : {}}, responseStub.getStub());

        responseStub.onComplete()
            .then(() => fail("Deve falhar devido aos parametros invalidos"))
            .catch(e => {})
            .then(() => done());
    });
    
    it("Deve registrar um novo Context", done => {
        let responseStub = new ResponseStub();
        setContext({
            params : {
                interface : "telegramId",
                interfaceId : "666",
                intents : ["int1, int2"],
                entities : {ent1 : "1", ent2 : "2"}
            }
        }, responseStub.getStub());

        responseStub.onComplete()
            .then(resp => {
                let contextQ = new Parse.Query(new Parse.Object.extend('Context'));
                contextQ.equalTo("objectId", resp.message.id);
                contextQ.first()
                    .then(context => {
                        expect(context.get("telegramId")).toBe("666");
                    })
                    .catch(e => {
                        console.log(e);
                        fail(e);
                    })
                    .then(() => done());
            })
            .catch(e => {
                console.log(e);
                fail(e);
            })
            .then(() => done());
    });

    it ("Deve alterar um Context já existente", done => {
        let responseStub = new ResponseStub();

        setContext({
            params : {
                interface : "telegramId",
                interfaceId : "333",
                intents : ["int1"]
            }
        }, responseStub.getStub());

        responseStub.onComplete()
            .then(resp => {
                let otherResponseStub = new ResponseStub();
                
                setContext({
                    params : {
                        interface : "telegramId",
                        interfaceId : "333",
                        intents : [],
                        entities : {val1 : "1"}
                    }
                }, otherResponseStub.getStub());

                otherResponseStub.onComplete()
                    .then(otherResp => {
                        expect(otherResp.message.get("telegramId")).toBe("333");
                        expect(otherResp.message.get("intents")).not.toEqual(["int1"]);
                        expect(otherResp.message.get("intents")).toEqual([]);
                        expect(otherResp.message.get("entities")).toEqual({val1 : "1"});
                    })
                    .catch(e => {
                        console.log(e);
                        fail(e);
                    })
                    .then(() => done());
            })
            .catch(e => {
                console.log(e);
                fail(e);
            })
            .then(() => done());
    });
});

describe("getContextByInterfaceId", () => {
    beforeAll(done => {
        /// purge the user, and then proceed
        Promise.all([purgeTable("Context")])
            .catch((e) => fail(e))
            .then(() => done());
    });
    
    it("Deve falhar ao procurar um Context com o interfaceId inexistente", done => {
        let responseStub = new ResponseStub();
        responseStub.onComplete()
            .then(() => fail("Deve falhar devido a interfaceId inexistente"))
            .catch((e) => {})
            .then(() => done());
        
        getContextByInterfaceId({params : {}}, responseStub.getStub());

    });

    if("Deve obter Context pedido", done => {
        let responseStub = new ResponseStub();

        setContext({
            params : {
                interface : "telegramId",
                interfaceId : "111",
                intents : ["int1", "int2", "int3"],
                entities : {ent1 : "1", ent2 : "2"}
            }
        }, responseStub.getStub());

        responseStub.onComplete()
            .then(resp => {
                let otherResponseStub = new ResponseStub();

                getContextByInterfaceId({
                    params : {
                        interface : "telegramId",
                        interfaceId : "111"
                    }
                }, otherResponseStub.getStub());

                otherResponseStub.onComplete()
                    .then(otherResp => {
                        expect(otherResp.id).toBe(resp.id);
                    })
                    .catch(e => {
                        console.log(e);
                        fail(e);
                    })
                    .then(() => done());
            })
            .catch(e => {
                console.log(e);
                fail(e);
            })
            .then(() => done());
    });
});