Posts = new Mongo.Collection('posts');

if (Meteor.isServer) {
  Meteor.publish('posts', function() {
    return Posts.find();
  });
}

Posts.all = function() {
  return Posts.find({}).fetch();
}
