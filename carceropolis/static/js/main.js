jQuery(function ($) {

  //sidebar mobile menu
  $("#menu-toggle").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
  });

  //#main-slider
  $(function () {
    $('#main-slider.carousel').carousel({
      interval: 8000
    });
  });

  $('.centered').each(function (e) {
    $(this).css('margin-top', ($('#main-slider').height() - $(this).height()) / 2);
  });

  $(window).resize(function () {
    $('.centered').each(function (e) {
      $(this).css('margin-top', ($('#main-slider').height() - $(this).height()) / 2);
    });
  });

  //portfolio
  $(window).load(function () {
    $portfolio_selectors = $('.portfolio-filter >li>a');
    if ($portfolio_selectors != 'undefined') {
      $portfolio = $('.portfolio-items');
      $portfolio.isotope({
        itemSelector: 'li',
        layoutMode: 'masonry'
      });
      $portfolio_selectors.on('click', function () {
        $portfolio_selectors.removeClass('active');
        $(this).addClass('active');
        var selector = $(this).attr('data-filter');
        $portfolio.isotope({ filter: selector });
        return false;
      });
    }
  });

  //contact form
  var form = $('.contact-form');
  form.submit(function () {
    $this = $(this);
    $.post($(this).attr('action'), function (data) {
      $this.prev().text(data.message).fadeIn().delay(3000).fadeOut();
    }, 'json');
    return false;
  });

  //goto top
  $('.gototop').click(function (event) {
    event.preventDefault();
    $('html, body').animate({
      scrollTop: $("body").offset().top
    }, 500);
  });

  //Pretty Photo
  $("a[rel^='prettyPhoto']").prettyPhoto({
    social_tools: false
  });

  $(window).on('hashchange', function () {
    check_modals();
  });

  $(window).ready(function () {
    check_modals();
  })

  // Pagina de dados
  $('.dados-gerais').addClass('animated fadeInDownBig')

  // Animação Scroll com AOS
  AOS.init()

  // Scrollspy do bootstrap 

  $('body').scrollspy({ target: '#navbarlateral' })

  // Scroll em determinada section

$("#arrow").click(function() {

    let idAtual = $(this).attr('href').replace('#','')

    let clicado = $(':target').attr('id')

    //verifica se tem algum target na url
    if(idAtual == clicado ){


        //verifica se não é o ultimo
        if($('#'+idAtual).next().length){

            let idProximo = $('#'+idAtual).next().attr('id')

            console.log(idProximo)

            $('html, body').animate({
                scrollTop: $('#'+idProximo).offset().top
            }, 2000);

            $(this).attr('href','#'+idProximo)

        } else {
            //se for o ultimo, joga pra cima
            $('html, body').animate({
                scrollTop: $('.infografico').offset().top
            },  2000);
        }

    } 

    else {
        //se nao tem target, é o primeiro click
        $('html, body').animate({
            scrollTop: $('#'+idAtual).offset().top
        }, 2000);
    }

});

  //funcoes
  function hide_all_modals() {
    $('#login_modal').modal('hide');
    $('#cadastro_modal').modal('hide');
    $('#recupera_senha_modal').modal('hide');
  }

  function check_modals() {
    if (matches = window.location.href.match(/#login/)) {
      hide_all_modals();
      $('#login_modal').modal('show');
    } else if (matches = window.location.href.match(/#cadastro/)) {
      hide_all_modals();
      $('#cadastro_modal').modal('show');
    } else if (matches = window.location.href.match(/#recuperarsenha/)) {
      hide_all_modals();
      $('#recupera_senha_modal').modal('show');
    }
  }

})

//vanilla functions
function contador(elements) {

    for(let element of elements){

        let startNumber = parseInt(element.textContent),
            endNumber = parseInt(element.getAttribute('data-final-number'))
            
        setInterval(
            () => {

                if(startNumber < endNumber) {

                    startNumber++
                    element.textContent = startNumber

                } 

            }
            ,1
        )
    
    }
}
