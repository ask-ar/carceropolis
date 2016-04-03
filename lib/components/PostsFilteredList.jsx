PostsFilteredList = React.createClass({
  mixins: [ ReactMeteorData ],

  getMeteorData() {
    Meteor.subscribe('posts');
    var params = {};
    if (this.props.theme !== 'geral') { params.theme = this.props.theme }

    return { posts: Posts.find(params).fetch() };
  },

  render() {
    return (
      <div className="posts col-md-8 col-md-offset-2">

        <h2>POSTS FOR:  {this.props.theme}</h2>

        <ul>
          { this.data.posts.map( post => <li key={post._id}>{post.title}</li> ) }
        </ul>
      </div>
    );
  }
});
