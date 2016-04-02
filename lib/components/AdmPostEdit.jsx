AdmPostEdit = React.createClass({
  mixins: [ ReactMeteorData ],

  getMeteorData() {
    Meteor.subscribe('posts');
    return { post: Posts.findOne(this.props.id) };
  },

  render() {
    if (!this.data.post) { return false; }

    const post = this.data.post;
    const returnPath = `/adm/posts/${post._id}`

    return (
      <div className="adm">

        <div className="post-edit col-md-8 col-md-offset-2">
          <a href={returnPath} className="btn btn-default">&laquo; retornar</a>

          <PostForm post={post} />
        </div>

      </div>
    );
  }
});
