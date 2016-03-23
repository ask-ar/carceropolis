_glob = this;

if (Meteor.isClient) {
  var initialize = function() {
    $(document).find('[data-react-component]').each(function(i, container) {

      var component = $(container).data('react-component');
      var props = $(container).data('react-props') || {};
      ReactDOM.render(React.createElement(_glob[component], props), container);
    });
  };

  Meteor.startup(function(){
    for (var property in Template) {
      const tpl = Template[property];

      if (Blaze.isTemplate(tpl)) tpl.onRendered( initialize );
    }
  });
}
