var loginRequired = function(pause) {
  (Meteor.user() || Meteor.loggingIn()) ? this.next() : Router.go('login');
};

var detailsAction = function() {
  return { props: JSON.stringify({id: this.params.id}) }
};

Router.configure({
  layoutTemplate: 'Layout'
});

Router.map(function(){
  this.route('home', { path: "/" });
  this.route('login');
  this.route('adm');
  this.route('admPost', { path: '/adm/posts/:id', template: 'AdmPost', data: detailsAction });
});


Router.onBeforeAction(loginRequired, {only: ['adm', 'admPost']});
