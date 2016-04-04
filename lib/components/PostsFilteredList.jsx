PostsFilteredList = React.createClass({
  mixins: [ ReactMeteorData ],

  componentWillMount() {
    this.setState({theme: this.props.theme, category: 'geral'})
  },

  getMeteorData() {
    Meteor.subscribe('posts');
    var params = {};
    if (this.state && this.state.theme !== 'geral') { params.theme = this.state.theme }
    if (this.state && this.state.category !== 'geral') { params.category = this.state.category }

    return { posts: Posts.find(params).fetch() };
  },

  componentDidMount() {
    mediator.subscribe('navbar:action', (evt, obj)=> {
      console.log('onAction', obj);
    })
    renderSubmenu(this.submenu());
  },

  componentDidUpdate() {
    renderSubmenu(this.submenu());
  },

  changeCategory(category, event) {
    event.preventDefault();
    this.setState(Object.assign({}, this.state, {category: category}));
  },

  submenu() {
    const categoryCls = (category)=> {
      const activeCls = (this.state.category === category) ? 'active': '';
      return `col-md-4 col-sm-4 col-xs-4 ${activeCls}`;
    }
    return (
      <ul className="posts-submenu col-md-4 col-md-offset-4 col-sm-6 col-sm-offset-3 col-xs-8 col-xs-offset-2">
        <li className={categoryCls('geral')}  onClick={this.changeCategory.bind(this, 'geral')}><a href="#">Geral</a></li>
        <li className={categoryCls('post')}   onClick={this.changeCategory.bind(this, 'post')}><a href="#">Artigos</a></li>
        <li className={categoryCls('edital')} onClick={this.changeCategory.bind(this, 'edital')}><a href="#">Editais</a></li>
      </ul>
    );
  },

  postPath(post) {
    return `/post/${post._id}`;
  },

  render() {
    const post = this.data.posts[0] || {};

    // get the first image to be the post header background
    const titleImg = $(post.content).find('img').first();
    var headerStyle = {};
    if (titleImg.length > 0 ) {
      headerStyle['backgroundImage'] = "url('" + titleImg.attr("src") + "')";
    }

    return (
      <div className="posts filtered-posts col-md-8 col-md-offset-2 col-sm-12 col-xs-12">

        <div className="posts--breadcrumbs">{`Publicações / ${lodash.startCase(this.state.theme)} / ${lodash.startCase(this.state.category)}`}</div>

        {
          (this.data.posts.length == 0) ? (
            <h2 className="posts--list__empty">Não há postagens para esse tema.</h2>

          ) : (
            <ul className="posts--list">
              <li className="posts--item">
                <a href={this.postPath(post)} className="post--header" style={headerStyle}></a>
                <a href={this.postPath(post)} className="post--title"><h2>{post.title}</h2></a>
                <aside>
                  por <span className="post--author">{post.username}</span>
                  em <span className="post--time">{moment(post.createdAt).format('DD/MM/YYYY HH:MM')}</span>
                </aside>
                <div className="post--teaser">
                  { $(post.content).text().substring(0, 200) }
                  ... <a href={this.postPath(post)}>[Leia mais &raquo;]</a>
                </div>
              </li>

              <hr />
              { this.data.posts.slice(2).map( post => <li key={post._id}>{post.title}</li> ) }
            </ul>
          )
        }
      </div>
    );
  }
});
