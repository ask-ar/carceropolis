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
  this.route('admPostEdit', { path: '/adm/posts/:id/edit', template: 'AdmPostEdit', data: detailsAction });
  this.route('posts');
  this.route('contact');
  this.route('about');
  this.route('experts');
  this.route('postsFiltered', { path: '/posts/:theme', template: 'postsFiltered', data: function() {
    return { props: JSON.stringify({theme: this.params.theme}) };
  }});
  this.route('postDetails', { path: '/post/:id', template: 'postDetails', data: detailsAction });
});


Router.onBeforeAction(loginRequired, {only: ['adm', 'admPost']});
