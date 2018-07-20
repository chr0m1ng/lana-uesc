const lana = require('./lana');
// const b4a = require('./b4a');
const watson = require('./watson');

// b4a.newUser('gabrieldsa', '12345', 'telegram', '100772324', 'Gabriel')
//     .then(res => console.log(res))
//     .catch(err => console.log(err));

watson.sendIntentToWatson('Usuario_Registrar_Existente')
    .then(resp => console.log(resp))
    .catch(err => console.log(err));