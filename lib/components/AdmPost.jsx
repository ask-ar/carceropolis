AdmPost = React.createClass({
  handleSubmit(event) {
    event.preventDefault();
    console.log('handleSubmit');
  },

  renderForm() {
    return (
      <form className="adm-post--form" onSubmit={this.handleSubmit}>
        <div className="form-group">
          <div id="editor"></div>
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
    return this.editor.summernote('code');
  },

  render() {
    return (
      <div className='adm-post'>
        <h1>Postagens</h1>

        {this.renderForm()}
      </div>
    );
  }
});
