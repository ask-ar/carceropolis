Meteor.startup(function(){
	process.env.MAIL_URL = 'smtp://email:password@smtp.gmail.com:587/'
});
