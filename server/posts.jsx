Meteor.methods({
  'posts.insert'(post) {
    if (! Meteor.userId()) { throw new Meteor.Error('not-authorized'); }

    var data = Object.assign({}, post, {
      createdAt: new Date(),
      owner: Meteor.userId(),
      username: Meteor.user().username,
    });
    Posts.insert(data);
  },

  'posts.remove'(id) {
    Posts.remove(id);
  },

  'posts.update'(id, params) {
    Posts.update(id, { $set: params });
  },
});
