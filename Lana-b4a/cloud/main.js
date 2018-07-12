const cloudFunctions = require('./cloud-functions');

Parse.Cloud.define("echo", cloudFunctions.echo(Parse));

Parse.Cloud.define("getUserByField", cloudFunctions.getUserByField(Parse));

Parse.Cloud.define("setUserField", cloudFunctions.setUserField(Parse));

Parse.Cloud.define("registerUser", cloudFunctions.registerUser(Parse));

Parse.Cloud.define("loginUser", cloudFunctions.loginUser(Parse));

Parse.Cloud.define("setContext", cloudFunctions.setContext(Parse));

Parse.Cloud.define("getContextByInterfaceId", cloudFunctions.getContextByInterfaceId(Parse));