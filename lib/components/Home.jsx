Home = React.createClass({
  render() {
    const msg = 'Welcome HOME' + (Meteor.user() ? `, ${Meteor.user().username}` : '');
    return (
      <div className="home">
        {msg} !
      </div>
    );
  }
});
