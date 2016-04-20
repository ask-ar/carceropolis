Posts = new Mongo.Collection('posts');
// posts :
//   - title
//   - content
//   - category
//   - theme
//   - owner
//   - createdAt

if (Meteor.isServer) {
  Meteor.publish('posts', function() {
    return Posts.find();
  });
}

Posts.all = function() {
  return Posts.find({}).fetch();
}
