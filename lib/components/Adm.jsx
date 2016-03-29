Adm = React.createClass({
  render() {
    return (
      <div className="adm col-md-8 col-md-offset-2">
        <ul className="nav nav-tabs" role="tablist">
          <li role="post" className="active"><a href="#post" aria-controls="post" role="tab" data-toggle="tab">Postagens</a></li>
          <li role="user" className=""><a href="#user" aria-controls="user" role="tab" data-toggle="tab">Usuários</a></li>
        </ul>


        <div className="tab-content">
          <div role="tabpanel" className="tab-pane active" id="post">
            <AdmPost />
          </div>

          <div role="tabpanel" className="tab-pane" id="user">
            <h1>User</h1>
          </div>

        </div>
      </div>
    );
  }
});
