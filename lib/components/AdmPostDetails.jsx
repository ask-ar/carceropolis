AdmPostDetails = React.createClass({
  mixins: [ ReactMeteorData ],

  getMeteorData() {
    Meteor.subscribe('posts');

    return {
      post: Posts.findOne(this.props.id)
    };
  },

  handleDelete(event) {
    event.preventDefault();

    if( window.confirm('A exclusão deste Post não poderá ser desfeita. \nVocê deseja realmente remover esse item?') ) {
      Meteor.call('posts.remove', this.props.id);
      Router.go('/adm');
    }
  },

  render() {
    if (!this.data.post) { return false; }

    const post = this.data.post;
    const markup = {__html: post.content};

    // get the first image to be the post header background
    const titleImg = $(this.data.post.content).find('img').first();
    var headerStyle = {};
    if (titleImg.length > 0 ) {
      headerStyle['backgroundImage'] = "url('" + titleImg.attr("src") + "')";
    }

    const editPath = `/adm/posts/${post._id}/edit`

    return (
      <div className="adm">
        <div className="post-details-actions col-md-8 col-md-offset-2">
          <a href="/adm" className="btn btn-default">&laquo; retornar</a>
          <button className="btn btn-action btn-red" onClick={this.handleDelete}><i className="glyphicon glyphicon-trash"></i></button>
          <a href={editPath} className="btn btn-action btn-primary">Editar</a>
        </div>

        <div className="post col-md-8 col-md-offset-2">
          <div className="post--header" style={headerStyle}></div>
          <div className="post--title"><h2>{post.title}</h2></div>
          <aside>
            por <span className="post--author">{post.username}</span>
            em <span className="post--time">{moment(post.createdAt).format('DD/MM/YYYY HH:MM')}</span>
          <span className="post--theme">{lodash.startCase(post.theme)}</span>
          </aside>
          <div className="post--content" dangerouslySetInnerHTML={markup} />
        </div>

      </div>
    );
  }
});
