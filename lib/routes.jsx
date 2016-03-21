
Router.configure({
  layoutTemplate: 'Layout'
});

Router.map(function(){
  this.route('home', { path: "/" });

});

var loginRequired = function(pause) {
  (Meteor.user() || Meteor.loggingIn()) ? this.next() : Router.go('login');
};

// Router.onBeforeAction(loginRequired, {only: []});
