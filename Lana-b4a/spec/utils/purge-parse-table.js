/**
 * Removes all rows from the Parse Database
 * @param  {string} tablename the name of the parse table to be purged
 * @return {Promise}  promise to destroy each item  in the table
 */
module.exports = (Parse) => {
    return (tablename) => {
      let tableQuery;
      if (tablename === "User")
        tableQuery = new Parse.Query(Parse.User);
      else tableQuery = new Parse.Query(tablename);
      return tableQuery.find({useMasterKey : true}).then((items) => {
        let destroyQueue = [];
        for (let item of items) {
          destroyQueue.push(item.destroy({useMasterKey : true}));
        }
        return Promise.all(destroyQueue).catch((e) => {console.log("Error destroying: " + e.message)});
      });
    }
};