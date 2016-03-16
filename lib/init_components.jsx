_glob = this;

if (Meteor.isClient) {
  Meteor.startup(function(){
    for (var property in Template) {
      const tpl = Template[property];

      if ( Blaze.isTemplate(tpl) ) {
        tpl.onRendered( ()=> {
          $(document).find('[data-react-component]').each(function(i, container) {

            var component = $(container).data('react-component');
            var props = $(container).data('react-props') || {};
            ReactDOM.render(React.createElement(_glob[component], props), container);
          });

        });
      }
    }
  });
}
