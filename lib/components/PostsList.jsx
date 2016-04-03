PostsList = React.createClass({

  render() {
    return (
      <div className="posts row">
        <a href="/posts/geral" className="col-md-4 col-sm-6 col-xs-12 posts--theme" data-posts-theme="geral">
          <h3>Geral</h3>
        </a>
        <a href="/posts/funcionamento-do-sistema" className="col-md-4 col-sm-6 col-xs-12  posts--theme" data-posts-theme="funcionamento-do-sistema">
          <h3>Funcionamento do Sistema</h3>
        </a>
        <a href="/posts/perfil-populacional" className="col-md-4 col-sm-6 col-xs-12  posts--theme" data-posts-theme="perfil-populacional">
          <h3>Perfil Populacional</h3>
        </a>
        <a href="/posts/politica-criminal" className="col-md-4 col-sm-6 col-xs-12  posts--theme" data-posts-theme="politica-criminal">
          <h3>Política Criminal</h3>
        </a>
        <a href="/posts/sistemas-internacionais" className="col-md-4 col-sm-6 col-xs-12  posts--theme" data-posts-theme="sistemas-internacionais">
          <h3>Sistemas Internacionais</h3>
        </a>
        <a href="/posts/violencia-institucional" className="col-md-4 col-sm-6 col-xs-12  posts--theme" data-posts-theme="violencia-institucional">
          <h3>Violência Institucional</h3>
        </a>
      </div>
    );
  }
});
