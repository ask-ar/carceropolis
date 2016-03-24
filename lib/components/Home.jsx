Home = React.createClass({
  mixins: [ ReactMeteorData ],

  getMeteorData() {
    return {
      user: Meteor.user()
    };
  },

  render() {
    const msg = 'Welcome HOME' + (this.data.user ? `, ${this.data.user.username}` : '');
    return (
      <div className="home">
        {msg} !
      </div>
    );
  }
});
