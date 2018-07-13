class Back4app {}
const Parse = require('parse/node');
const keys = require('./config/keys');
Parse.initialize(keys.b4a_application_id, keys.b4a_js_key, keys.b4a_master_key);
Parse.serverURL = keys.b4a_server_url;
let b4a = new Back4app();

b4a.getUserContext = (interface, interfaceId) => {
    return new Promise ((resolve, reject) => Parse.Cloud.run('getContextByInterfaceId', {
        'interface' : interface,
        'interfaceId' : interfaceId})
        .then(resp => {
            resolve(resp.message);
        })
        .catch(err => {
            reject(err);
        })
    );
};

b4a.setUserContext = (interface, interfaceId, context) => {
    return new Promise ((resolve, reject) => Parse.Cloud.run('setContext', {
        'interface' : interface,
        'interfaceId' : interfaceId,
        'context' : context})
        .then(resp => {
            resolve(resp.message);
        })
        .catch(err => {
            reject(err);
        })
    );
};

b4a.getUser = (interface, interfaceId) => {
    return new Promise((resolve, reject) => 
        Parse.Cloud.run('getUserByField', {
            'field' : interface,
            'value' : interfaceId})
            .then(resp => {
                resolve(resp.message);
            })
            .catch(err => {
                reject(err);
            })
    );
};

b4a.setUserProp = (userId, propName, propValue) => {
    return new Promise((resolve, reject) => 
        Parse.Cloud.run('getUserByField', {
            'userId' : userId,
            'field' : propName,
            'value' : propValue})
            .then(resp => {
                resolve(resp.message);
            })
            .catch(err => {
                reject(err);
            })
    );
};

b4a.newUser = (username, password, interface, interfaceId, name) => {
    return new Promise((resolve, reject) => 
        Parse.Cloud.run('registerUser', {
            'username' : username,
            'password' : password,
            'interface' : interface,
            'interfaceId' : interfaceId,
            'name' : name})
            .then(resp => {
                resolve(resp.message);
            })
            .catch(err => {
                reject(err);
            })
    );
};

b4a.checkUserCredentials = (username, password) => {
    return new Promise((resolve, reject) => 
        Parse.Cloud.run('loginUser', {
            'username' : username,
            'password' : password})
            .then(resp => {
                resolve(resp.message);
            })
            .catch(err => {
                reject(err);
            })
    );
};


module.exports = b4a;