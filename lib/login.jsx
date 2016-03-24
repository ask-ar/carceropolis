if (Meteor.isClient) {

  Template.login.events({
    "submit .login": event => {
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
    }
  });
}
