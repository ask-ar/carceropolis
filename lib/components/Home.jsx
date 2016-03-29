Home = React.createClass({
  mixins: [ ReactMeteorData ],

  getMeteorData() {
    return {
      user: Meteor.user()
    };
  },

  render() {
    return (
      <div className="home">
        <div className="home--video">
          <video autoPlay loop muted poster="/presidio.jpg" className="home--bgvid">
            <source src="/ff.webm" type="video/webm" />
          </video>
        </div>
        <div className="home--content col-md-6 col-md-offset-3">
          <div className="home--brand">Carcerópolis</div>
          <p className="home--teaser">
            Single-origin coffee put a bird on it craft beer YOLO, Portland hella deep v Schlitz. Tumblr Bushwick post-ironic Thundercats. Vinyl 90's keytar, literally cardigan Williamsburg YOLO squid pickled Etsy salvia lo-fi locavore. Meh leggings retro
narwhal Neutra
          </p>
          <div className="home--links">
            <a className="btn btn-red btn-large" href="/dados">DADOS</a>
            <a className="btn btn-red btn-large" href="/posts">PUBLICAÇÕES</a>
          </div>
        </div>
      </div>
    );
  }
});
