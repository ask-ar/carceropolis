PostForm = React.createClass({
  getInitialState() {
    return {title: '', content: '', category: 'post', theme: 'funcionamento-do-sistema'};
  },

  updateState(obj) {
    this.setState(Object.assign({}, this.state, obj));
  },

  componentWillMount() {
    if (this.props.post) { this.updateState(this.props.post); }
  },

  componentDidMount() {
    const editor = this.editor().summernote({height: 300});
    if (this.props.post) {
      editor.summernote('code', this.props.post.content);
    }
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
    const postId = this.props.post ? this.props.post._id : null;
    const post = this.postData(target);

    // update existing post
    if (postId) {
      Meteor.call('posts.update', postId, post, (err, result)=> {
        if (err) { return FlashMessages.sendError(`Erro: ${err.error}`); }

        Router.go('admPost', {id: postId});
        FlashMessages.sendSuccess('Post atualizado com sucesso!');
      });

    // insert new post
    } else {
      Meteor.call('posts.insert', post, (err, result)=> {
        if (err) { return FlashMessages.sendError(`Erro: ${err.error}`); }

        event.target.reset();
        this.clearEditor();
        FlashMessages.sendSuccess('Post adicionado com sucesso!');
      });
    }
  },

  postData(form) {
    var data = _.reduce(form.serializeArray(), function(res, o) {
      res[o.name] = o.value;
      return res;
    }, {});
    data['content'] = this.editorContent();
    return data;
  },

  handleChange(event) {
    const target = $(event.target);
    var obj = {};
    obj[target.attr('name')] = target.val();
    this.updateState(obj);
  },

  render() {
    const post = this.props.post || {};
    const submitLabel = (post._id) ? 'ATUALIZAR' : 'POSTAR';

    return (
      <form className="adm-post--form" onSubmit={this.handleSubmit}>
        <div className="form-group">
          <label className="control-label" htmlFor='title'>Título</label>
          <input type='text' className="form-control" name='title' placeholder="Título do post" value={this.state.title} onChange={this.handleChange} required/>
        </div>
        <div className="form-group">
          <label className="control-label">Conteúdo</label>
          <div id="editor"></div>
        </div>
        <div className="row">
          <div className="form-group col-md-6">
            <label htmlFor="theme">Tema:</label>
            <select className="form-control" name="theme" value={this.state.theme} onChange={this.handleChange}>
              <option value="funcionamento-do-sistema">Funcionamento do Sistema</option>
              <option value="perfil-populacional">Perfil Populacional</option>
              <option value="politica-criminal">Política Criminal</option>
              <option value="sistemas-internacionais">Sistemas Internacionais</option>
              <option value="violencia-institucional">Violência Institucional</option>
            </select>
          </div>
          <div className="form-group col-md-6">
            <label htmlFor="category">Categoria:</label>
            <select className="form-control" name="category" value={this.state.category} onChange={this.handleChange}>
              <option value="post">Post</option>
              <option value="edital">Edital</option>
            </select>
          </div>
        </div>
        <button className="btn btn-red submit-btn" type="submit">{submitLabel}</button>
      </form>
    );
  }
});
