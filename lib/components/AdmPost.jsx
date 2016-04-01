AdmPost = React.createClass({
  mixins: [ ReactMeteorData ],

  getMeteorData() {
    Meteor.subscribe('posts');

    return {
      posts: Posts.find({}, { sort: { createdAt: -1 } }).fetch()
    };
  },

  renderPost(post) {
    const path = `/adm/posts/${post._id}`;
    return (
      <li key={post._id} className='adm-post--list-item'>
        <a href={path} className='post-title'>{post.title}</a>
        <aside>
          por <span className="post-info">{post.username}</span>
          em  <span className="post-info">{moment(post.createdAt).format('DD/MM/YYYY')}</span>
        </aside>
      </li>
    );
  },

  render() {
    return (
      <div className='adm-post'>
        <PostForm />

        <div className='adm-post--list'>
          <h2>Postagens: </h2>
          <ul>
            { this.data.posts.map(post => { return this.renderPost(post) }) }
          </ul>
        </div>
      </div>
    );
  }
});
