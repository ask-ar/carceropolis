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

    const post = this.data.post;
    const markup = {__html: post.content};

    return (
      <div className="adm-post post-details col-md-8 col-md-offset-2">
        <div><a href="/adm">&laquo; retornar</a></div>

        <div className="post">
          <div className="post--title"><h2>{post.title}</h2></div>
          <aside>
            por <span className="post--author">{post.username}</span>
            <span className="post--time">{moment(post.createdAt).format('DD/MM/YYYY HH:MM')}</span>
          </aside>
          <div className="post--content" dangerouslySetInnerHTML={markup} />
        </div>

      </div>
    );
  }
});
