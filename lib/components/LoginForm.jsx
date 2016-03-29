LoginForm = React.createClass({
  handleSubmit(event) {
    event.preventDefault();

    var email = event.target.email.value;
    var password = event.target.password.value;

    Meteor.loginWithPassword(email, password, err => {
      if (err) {
        event.target.password.value = "";
        FlashMessages.sendSuccess("Usuário ou senha incorretos!");

      } else {
        event.target.reset();
        Router.go('home');
      }
    });
  },

  render() {
    return (
      <div id="login" className='row'>
        <form className="login col-md-6 col-md-offset-3" onSubmit={this.handleSubmit}>
          <div className="form-group">
            <input type="email" name="email" className="form-control email" placeholder="E-mail Adress" required />
          </div>
          <div className="form-group">
            <input type="password" name="password" className="form-control password" placeholder="Password" required />
          </div>

          <button className="btn btn-red submit-btn" type="submit" value="Register">ACESSAR</button>
        </form>
      </div>
    );
  }
});
