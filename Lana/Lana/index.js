const lana = require('./lana');
const b4a = require('./b4a');

b4a.getUser('telegram', '666')
    .then(res => console.log(res))
    .catch(err => console.log(err.code));