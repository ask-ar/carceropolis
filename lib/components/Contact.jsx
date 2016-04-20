Contact = React.createClass({
  handleSubmit(event) {
    event.preventDefault();

    var email = event.target.email.value;
    var subject = event.target.subject.value;
    var message = event.target.message.value;

    Meteor.call('sendEmail', 'email@email.com', email, subject, message, err => {
      if (err) {
        FlashMessages.sendSuccess("Houve algum erro, tente novamente.");
      } else {
        Router.go('home');
        FlashMessages.sendSuccess("Mensagem enviada com sucesso!");
      }
    });
  },
  render() {
    return (
      <div className="contact">
        <div className="row">
          <div className="col-md-8 col-md-offset-2 col-sm-12 col-xs-12">
            Contato
          </div>
        </div>
        <div className="row background-img">
          <div className="col-md-6 col-sm-12 col-xs-12 center-block float-none">
            <p>Hella narwhal Cosby sweater McSweeneys, salvia kitsch before they sold out High Life.</p>
            <br/>
            <p>CONECTAS DIREITOS HUMANOS<br/>CAIXA POSTAL: 62633 – CEP 01214-970.<br/>SÃO PAULO/SP - BRASIL</p>
            <br/>
            <br/>
            <p>Ou mande uma mensagem:</p>
            <br/>
            <form onSubmit={this.handleSubmit}>
              <div className="form-group">
                <input type="name" className="form-control" id="inputName" placeholder="Seu nome*" required/>
              </div>
              <div className="form-group">
                <input type="email" className="form-control" id="inputEmail" placeholder="Email*" required/>
              </div>
              <div className="form-group">
                <input type="subject" className="form-control" id="inputSubject" placeholder="Assunto*" required/>
              </div>
              <div className="form-group">
                <textarea className="form-control" rows="3" placeholder="Escreva sua mensagem*" required></textarea>
              </div>
              <button type="submit" className="btn btn-red btn-large pull-right" type="submit">ENVIAR</button> 
            </form>
          </div>
        </div>
      </div>
    );
  }
});