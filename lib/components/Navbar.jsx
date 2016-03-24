Navbar = React.createClass({
  mixins: [ ReactMeteorData ],

  getMeteorData() {
    return {
      user: Meteor.user()
    };
  },

  isHome() {
    return Router.current().route.getName() === 'home';
  },

  loggedIn() {
    return !!this.data.user;
  },

  handleLogout(event) {
    event.preventDefault();
    this.hideMenu();
    Meteor.logout(() => { Router.go('home') });
  },

  handleLogin(event) {
    this.hideMenu();
  },

  hideMenu() {
    $("#nav-menu").offcanvas('hide');
  },

  menuSmall() {
    const navbarCls = `navbar navbar-default navbar-fixed-top ${this.isHome() ? 'home' : ''}`;
    return (
      <div className='hidden-md hidden-lg cp-menu-small'>
        <nav id="nav-menu" className="navmenu navmenu-default navmenu-fixed-left offcanvas" role="navigation">
          <h2 className="navmenu-brand">MENU</h2>
          <ul className="nav navmenu-nav">
            <hr />
            <li><a href="#">DADOS</a></li>
            <li><a href="#">PUBLICAÇÕES</a></li>

            <hr />
            <li><a href="#">Banco de Especialistas</a></li>
            <li><a href="#">Fale Conosco</a></li>
            <li><a href="#">Sobre Nós</a></li>

            <hr />
            { this.loggedIn() ? <li><a href="/adm">Admin</a></li> : false }
            { this.loggedIn() ? <li><a href="#" onClick={this.handleLogout}>Logout</a></li> : false }

            { !this.loggedIn() ? <li><a href="/login" onClick={this.handleLogin}>Login</a></li> : false }
          </ul>
        </nav>
        <div className={navbarCls} >
          <a href="#" className="menu-icon" data-toggle="offcanvas" data-target="#nav-menu" data-canvas="body"><i className="glyphicon glyphicon-menu-hamburger"></i></a>
        </div>
      </div>
    );
  },

  menuLarge() {
    return (
      <div className='hidden-xs hidden-sm cp-menu-large'>
        <nav className="navbar navbar-default navbar-fixed-top" role="navigation">
          <a href="/" className="navbar-brand">Carceropólis</a>
          <ul className="nav navbar-nav">
            <li><a href="#">DADOS</a></li>
            <li><a href="#">PUBLICAÇÕES</a></li>

            <li><a href="#">BANCO DE ESPECIALISTAS</a></li>
            <li><a href="#">FALE CONOSCO</a></li>
            <li><a href="#">SOBRE NÓS</a></li>
          </ul>
          <ul className="nav navbar-nav navbar-right navbar-actions">
            { this.loggedIn() ? <li><a href="/adm">Admin</a></li> : false }
            { this.loggedIn() ? <li><a href="#" onClick={this.handleLogout}>Logout</a></li> : false }

            { !this.loggedIn() ? <li><a href="/login" onClick={this.handleLogin}>Login</a></li> : false }
          </ul>
        </nav>
      </div>
    );
  },

  render() {
    return (
      <div>
        {this.menuSmall()}
        {this.menuLarge()}
      </div>
    );
  },
});
