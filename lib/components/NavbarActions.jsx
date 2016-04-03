NavbarActions = React.createClass({
  shouldShowActions() {
    const acceptedRoutes = [ 'postsFiltered' ];
    return (acceptedRoutes.indexOf( Router.current().route.getName() ) > -1)
  },

  changeContext(action, event) {
    event.preventDefault();
    mediator.publish('navbar:action', {action: action});
  },

  render() {
    if (this.shouldShowActions()) {
      return (
        <span className="context-actions top-line">
          <a href="#" onClick={this.changeContext.bind(this, 'filter')}><i className="glyphicon glyphicon-filter"></i></a>
          <a href="#" onClick={this.changeContext.bind(this, 'search')}><i className="glyphicon glyphicon-search"></i></a>
        </span>
      );

    } else {
      return false;
    }
  }
});
