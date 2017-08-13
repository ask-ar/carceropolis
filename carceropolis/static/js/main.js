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


// //Pagina de dados
//   $('.dados-gerais').addClass('animated fadeInDownBig')

//   /**
//    * Copyright 2012, Digital Fusion
//    * Licensed under the MIT license.
//    * http://teamdf.com/jquery-plugins/license/
//    *
//    * @author Sam Sehnert
//    * @desc A small plugin that checks whether elements are within
//    *     the user visible viewport of a web browser.
//    *     only accounts for vertical position, not horizontal.
//    * src: https://codepen.io/chriscoyier/pen/DjmJe
//    */

//   $.fn.visible = function(partial) {
    
//       var $t            = $(this),
//           $w            = $(window),
//           viewTop       = $w.scrollTop(),
//           viewBottom    = viewTop + $w.height(),
//           _top          = $t.offset().top,
//           _bottom       = _top + $t.height(),
//           compareTop    = partial === true ? _bottom : _top,
//           compareBottom = partial === true ? _top : _bottom;
    
//     return ((compareBottom <= viewBottom) && (compareTop >= viewTop));

//   }
  
//   var win = $(window);

//   var allSections = $(".infografico section");

//   allSections.each(function(i, el) {
//     var el = $(el);
//     if (el.visible(true)) {
//       el.addClass("already-visible"); 
//     } 
//   })

//   win.scroll(function(event) {
    
//     allSections.each(function(i, el) {
//       var el = $(el);
//       if (el.visible(true)) {
//         el.addClass('animated slideInLeft'); 
//       } 
//     });
    
//   })

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


// Animação Scroll com AOS

$(function() {
  AOS.init();
});

$(window).on('load', function() {
  AOS.refresh();
});