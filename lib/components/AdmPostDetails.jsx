AdmPostDetails = React.createClass({
  mixins: [ ReactMeteorData ],

  getMeteorData() {
    Meteor.subscribe('posts');

    return {
      post: Posts.findOne(this.props.id)
    };
  },

  render() {
    if (!this.data.post) { return false; }

    return (
      <h1>ADM POST: {this.data.post.title} </h1>
    );
  }
});
