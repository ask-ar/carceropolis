# TODO

- [x] auth
    - [x] login
    - [x] logout
    - [x] access control

- [ ] admin
    - [x] add post
    - [ ] invite new user

- [x] layout
    - [x] nav bar
    - [x] side menu

- [x] home page
    - [x] background video
    - [x] logo

- [ ] Dados
    - [ ] list?
    - [ ] filtros
    - [ ] mapa
    - [ ] search

- [x] Publicações
    - [x] list temas
    - [x] view tema
    - [x] view post

- [ ] mapa
    - [ ] todo brasil
    - [ ] por estado

- [ ] filtros
    - [ ] período
    - [ ] gênero
    - [ ] estado

- [ ] search

- [ ] share

- [ ] fale conosco
- [ ] sobre nós
- [ ] banco de especialistas

# Tecnologias:

- Meteor + react + bootstrap (com Scss)
- Do meteor usamos pouco. Essencialmente o iron-router, irá renderizar templates dummy, os quais têm uma div com o attributo `data-react-component` (que indica a classe do component do react a ser chamada) e as vezes `data-react-props` com um json serializado contendo propriedades iniciais. Ou seja:

```
// routes.jsx
this.route('bla');


// templates/bla.html
<template name="bla">
  <div data-react-component="BlaPage" data-react-props='{"num": 42}'></div>
</template>

// components/BlaPage.jsx
BlaPage = React.createClass({
    render() {
      return <h1>Hello! The num is {this.props.num}</h1>
    }
});
```

- Para integração do react + meteor eu recomendo:

    - https://www.meteor.com/tutorials/react/creating-an-app
    - http://react-in-meteor.readthedocs.org/en/latest/


- Para unir o esquema de reactive-data do Meteor com o React, segue o padrão:

```
var HelloUser = React.createClass({
  mixins: [ReactMeteorData], // incluir esse mixin

  getMeteorData() {
    // se estiver usando publish/subscribe é aqui q vc faz o subscribe
    return {
      currentUser: Meteor.user()  // dado disponibilizado em this.data.currentUser
    };
  },

  render() {
    // qdo this.data atualizar a view atualiza apropriadamente
    return <span>Hello {this.data.currentUser.username}!</span>;
  }
});

```

- Para os components do React, usamos components simples. Somente um `React.createClass` expondo um método `render`.

- sempre bom conhecer o lifecycle dos components: https://facebook.github.io/react/docs/component-specs.html


# Tarefas e Sugestões

### Users

 - por enqto para adicionar um usuário no sistema fazemos via task (definida em tasks.jsx). ie: basta enter em `meteor shell` e rodar `createUser({username: ‘username’, email: ‘email@email.com’, password: ‘12345pass’})`
- futuramente, a sugestão é: na interface administrativa (`/adm`) um admin, pode convidar outro. Ou seja, entra um endereço de email, irá disparar um mail com link (contendo token de verificação) para um form no qual o convidado vai cadastrar seu username e senha.

### Navbar

- infelizmente o menu acabou ganhando complexidade. Talvez seja uma boa refatora-lo.
- Temos uma layout base em `templates/layout.html`, la o component de `Navbar` e incluido em todos os templates que usamos no sistema.
- esse component renderiza duas nabvars distintas `menuLarge` e `menuSmall`, eles são os menus em desktop e mobile respectivamente.
- temos tbm uma função chamada `renderSubmenu` que recebe um element (um jsx renderizado) e substitui no placeholder apropriado
- temos tbm o `NavbarActions` que são as ações de contexto (como filtros, busca, etc). Por enqto esse components está meio tosco, pq só é usado uma vez (não deu tempo de fazer uma abstração melhor). Ele só tem um whitelist de rotas que ele renderiza esses botões de "açoes", mas futuramente essas ações deverão mudar tbm. Então fica ao critério de como fazer isso melhor

- Se quiser mudar a forma como o navbar e layout funciona, fique a vontade. Uma sugestão seria renderizar o component de Navbar dentro dos components de página mesmo, passado por parametros as actions ou submenu (em vez de verificar a rota)

### EventBus

- o arquivo `init_components.jsx` tem o código de inicialização dos components. Possui tbm um mediator de eventos global, para vc conversar entre components (fazer um pubsub).
- Uma sugestão seria usá-lo para a parte de busca para interligar o NavbarActions (emitir um `mediator.publish('search', 'search term')`) com a listagem (`mediator.subscribe` atualiza o state que faz o meteorData atualizar o `find()` e re-renderizar a lista)

### Busca

- https://www.okgrow.com/posts/guide-to-full-text-search-in-meteor

### Dados

- importação de planilha pode seguir o mesmo esquema de tasks `createUser`
- acho que os widgets de apresentação podem ser pequenas classes de component do React e vc pode somente monta-los dinâmicamente com `ReactDOM.createElemente(MyWidget, targetEL, dataProps)`
- para a parte de mapa eu recomendo bastante o mapbox: https://atmospherejs.com/pauloborges/mapbox  (no dashboard-da-saude tem uma integração dele se quiser usar de exemplo)
