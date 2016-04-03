_glob = this;

if (Meteor.isClient) {
  // Event bus for using pub/sub. You should always use this mediator
  // to communicate between components
  mediator = {
    obj: $({}),

    publish: function (channel, data) {
      this.obj.trigger(channel, data);
    },

    subscribe: function (channel, fn) {
      this.obj.bind(channel, fn);
    },

    unsubscribe: function (channel, fn) {
      this.obj.unbind(channel, fn);
    }
  };
  
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
