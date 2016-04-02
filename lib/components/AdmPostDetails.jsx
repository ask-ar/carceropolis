AdmPostDetails = React.createClass({
  mixins: [ ReactMeteorData ],

  getMeteorData() {
    Meteor.subscribe('posts');

    return {
      post: Posts.findOne(this.props.id)
    };
  },

  componentDidMount() {
    // const titleImg = $(this.data.post.content).find('img').first();
    // $('.post--title img').attr('src', titleImg.attr('src'));
  },

  render() {
    if (!this.data.post) { return false; }

    const post = this.data.post;
    const markup = {__html: post.content};

    return (
      <div className="adm">
        <div><a href="/adm">&laquo; retornar</a></div>

        <div className="post col-md-6 col-md-offset-3">
          <div className="post--header"></div>
          <div className="post--title"><h2>{post.title}</h2></div>
          <aside>
            por <span className="post--author">{post.username}</span>
          em <span className="post--time">{moment(post.createdAt).format('DD/MM/YYYY HH:MM')}</span>
          </aside>
          <div className="post--content" dangerouslySetInnerHTML={markup} />
        </div>

      </div>
    );
  }
});
