tasks = {
  createUser(opts) {
    if (_.isEmpty(opts.username)) { throw 'username is required' }
    if (_.isEmpty(opts.email))    { throw 'email is required' }
    if (_.isEmpty(opts.password)) { throw 'password is required' }

    if (Meteor.users.find({ 'emails.address': opts.email }).count() === 0) {
        Accounts.createUser({
          username: opts.username,
          email: opts.email,
          password: opts.password,
          profile : {
            roles:['admin'],
            name: opts.username
          }
        });
        console.log("Created user: ", opts.username);
    }
  }
}
