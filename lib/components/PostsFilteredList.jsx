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

  render() {
    return (
      <div className="posts col-md-8 col-md-offset-2">

        <h2>POSTS FOR:  {this.state.theme}</h2>

        <ul>
          { this.data.posts.map( post => <li key={post._id}>{post.title}</li> ) }
        </ul>
      </div>
    );
  }
});
