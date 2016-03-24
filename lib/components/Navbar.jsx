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

  render() {
    const navbarCls = `navbar navbar-default navbar-fixed-top ${this.isHome() ? 'home' : ''}`;
    return (
      <div>
        <nav id="nav-menu" className="navmenu navmenu-default navmenu-fixed-left offcanvas" role="navigation">
          <a className="navmenu-brand" href="#">Brand</a>
          <ul className="nav navmenu-nav">
            <li className="active"><a href="#">Home</a></li>

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
});
