AdmPost = React.createClass({
  mixins: [ ReactMeteorData ],

  getMeteorData() {
    Meteor.subscribe('posts');

    return {
      posts: Posts.find({}, { sort: { createdAt: -1 } }).fetch()
    };
  },


  renderForm() {
    return (
      <form className="adm-post--form" onSubmit={this.handleSubmit}>
        <div className="form-group">
          <div id="editor"></div>
        </div>
        <div className="row">
          <div className="form-group col-md-6">
            <label htmlFor="theme">Tema:</label>
            <select className="form-control" name="theme">
              <option value="funcionamento-do-sistema">Funcionamento do Sistema</option>
              <option value="perfil-populacional">Perfil Populacional</option>
              <option value="politica-criminal">Política Criminal</option>
              <option value="sistemas-internacionais">Sistemas Internacionais</option>
              <option value="violencia-institucional">Violência Institucional</option>
            </select>
          </div>
          <div className="form-group col-md-6">
            <label htmlFor="category">Categoria:</label>
            <select className="form-control" name="category">
              <option value="post">Post</option>
              <option value="edital">Edital</option>
            </select>
          </div>
        </div>
        <button className="btn btn-red submit-btn" type="submit">POSTAR</button>
      </form>
    );
  },

  componentDidMount() {
    this.editor().summernote({height: 200});
  },

  editor() {
    return $('#editor')
  },

  editorContent() {
    return this.editor().summernote('code');
  },

  clearEditor() {
    this.editor().summernote('code', '');
  },

  handleSubmit(event) {
    event.preventDefault();

    const target = $(event.target);
    const post = this.postData(target);

    Meteor.call('posts.insert', post, (err, result)=> {
      if (err) { return FlashMessages.sendError(`Erro: ${err.error}`); }

      event.target.reset();
      this.clearEditor();
      FlashMessages.sendSuccess('Post adicionado com sucesso!');
    });
  },

  postData(form) {
    var data = _.reduce(form.serializeArray(), function(res, o) {
      res[o.name] = o.value;
      return res;
    }, {});
    data['content'] = this.editorContent();
    return data;
  },

  posts() {
    Posts.find({}).fetch();
    return (
      <ul>
        {this.data.posts.map(post => <li key={post._id}>{post.content}</li>)}
      </ul>
    );
  },

  render() {
    return (
      <div className='adm-post'>
        {this.renderForm()}
        {this.posts()}
      </div>
    );
  }
});
