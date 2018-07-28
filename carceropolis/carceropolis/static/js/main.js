jQuery(function ($) {

    //sidebar mobile menu
    $("#menu-toggle").on('click', function (e) {
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

    $(window).on('resize', function () {
        $('.centered').each(function (e) {
            $(this).css('margin-top', ($('#main-slider').height() - $(this).height()) / 2);
        });
    });

    //portfolio
    $(window).on('loadl', function () {
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
    $('.gototop').on('click', function (event) {
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
    if (location.pathname.toLowerCase() === '/dados/' ) {
        $('section#title').hide()
        
        const animTarget = "#dados-bar"
        
        const animDadosGerais = (ativo = `#dados-gerais`) => {
            $(`${ativo} [data-tobold]`).addClass(`toBold`)
            contador(
                document.querySelectorAll(`${ativo} [data-final-number]`)
                , 12
                , 1000
                , () => $(`${ativo} .anim1`).addClass(`bounceInDown`)
            )
        }

        const animacoes = function(eventOrHash) {
            
            typeof(eventOrHash) === 'string'
            ? this.ativo = location.hash 
            : this.ativo = $(eventOrHash.target).find('a').attr('href')

            switch (this.ativo) {
                case `#dados-gerais`:
                    animDadosGerais(this.ativo)
                    break

                case `#perfil-populacional`:
                    //aparecer primeiro o bloco "A população carcerária..."
                    $(`${this.ativo} .anim1`).addClass(`slideInLeft`)
                    //aparecer depois o gráfico, animando a linha
                    $(`${this.ativo} svg .linha`).addClass(`linha full`)
                    //aparecer depois o Estado de São Paulo e preencher proporcionalmente a 35% da área (animação)
                    $(`${this.ativo} svg .linha`).on('animationend', () => {
                        $(`${this.ativo} .anim2`).addClass(`slideInUp`).removeClass(`anim2`)
                    })
                    //aparecer, por fim, o bloco "segundo dados do IBGE..."
                    $(`${this.ativo} .anim2`).on('animationend', () => {
                        $(`${this.ativo} .anim3`).addClass(`slideInUp`).removeClass(`anim3`)
                    })
                    break

                case `#infraestrutura`:
                    let moving = `${this.ativo} .moving`,
                        clickIndex = 1

                    $(moving).addClass('anim')
                    $(`${this.ativo} .c10`).addClass(`fadeIn`)

                    $(`${this.ativo}`).on('click', () => {
                        
                        switch (clickIndex) {
                            case 1:
                                $(moving).addClass('anim2')
                                $(`${this.ativo} .c19`).removeClass(`fadeOut`)
                                $(`${this.ativo} .c19`).addClass(`fadeIn`)
                                clickIndex++
                            break
                            case 2:
                                $(moving).addClass('anim3')
                                $(`${this.ativo} .c48`).removeClass(`fadeOut`)
                                $(`${this.ativo} .c48`).addClass(`fadeIn`)
                                clickIndex++
                            break
                            case 3:
                                $(moving).removeClass('anim2 anim3')
                                $(`${this.ativo} .c48`).addClass(`fadeOut`)
                                $(`${this.ativo} .c19`).addClass(`fadeOut`)

                                $(`${this.ativo} .c48`).toggleClass(`fadeIn`)
                                $(`${this.ativo} .c19`).toggleClass(`fadeIn`)
                                
                                clickIndex = 1
                        }
                    })

                case `#situacao-juridica`:
                    contador(document.querySelectorAll(`${this.ativo} [data-final-number]`), 20)
                    /*
                    4. Situação Jurídica
                    - preencher o branco
                    - destacar e aparecer o respectivo texto em branco com animação (contador) do 41%
                    - preencher o vermelho
                    - destacar e aparecer o respectivo texto em vermelho com animação (contador) do 37%
                    - aparecer "1 em cada 5" e depois o restante do rexto "presídio oferece..."
                    - aparecer o último bloco de conteúdo, com apenas os quadrados brancos e com "crimes sem violência" em branco
                    - depois, preencher os semi-círculos vermelhos ao mesmo que tempo que aparece o círculo vermelho
                        do 7 ao mesmo tempo que  "crimes sem violência" torna-se vermelho
                    */
                    break

                case `#trabalho-educacao`:
                    /* 5. Trabalho e educação
                    - imagem aparece primeiro
                    - depois vem o texto por cima, pelo lado esquerdo
                    - primeiro conjunto de 5 quadradinhos alinhados verticalmente
                    - segundo conjunto de quadradinhos, aparecer num grid de 5 linhas e aparecer coluna por coluna (da esquerda para a direita)
                    - preencher barra de progresso da esquerda para a direita de forma que o 18% seja revelado dentro da barra */
                    contador(document.querySelectorAll(`${this.ativo} [data-final-number]`), 5)
                    break

                case `#saude`:
                    contador(document.querySelectorAll(`${this.ativo} [data-final-number]`), 5)
                    /*  6. Saúde
                    - aparecer o texto "consultório médico"
                    - "Saúde" e texto "Apesar da metade..." na mesma cor do atual texto "49 ginecologistas..." com fundo branco
                    - animação (contador) no 49
                    - número 36.495 inciando normal e tornando-se negrito
                    - entrar próxima caixa de texto, sem o "3 vezes..." e os caixões
                    - por fim, aparecer o "3 vezes mais chances de morrer" e os 3 caixoes concomitantemente */
                    break

                case `#materno-infantil`:
                    contador(document.querySelectorAll(`${this.ativo} [data-final-number]`), 1)
                    /*  7. Materno-infantil
                    - animação (contador) no 534
                    - animação (contador) no 585 */
                    break

                case `#alas-exclusivas`:
                    contador(document.querySelectorAll(`${this.ativo} [data-final-number]`), 1)
                    /* 8. Alas Exclusivas
                    - animação (contador) no 12%
                    - número 1.294 inciando normal e tornando-se negrito
                    - preencher celas vermelhas e depois as cadeiras de rodas brancas */
                    break

                case `#unidades-prisionais`:
                    contador(document.querySelectorAll(`${this.ativo} [data-final-number]`), 1)

                    break

                default:
                    throw `Alvo da animação desconhecido: ${this.ativo}`
            }
        }

        location.hash
        ? animacoes(location.hash)
        : animDadosGerais()
        
        $('body')
                .attr('data-spy', 'scroll')
                .attr('data-target', animTarget)
                .addClass('dados')
                .scrollspy({ target: animTarget, offset: 600 })
                .on('activate.bs.scrollspy', event => animacoes(event))
        
    }

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

/**
 * Contador
 * @constructor
 * @param {NodeList} elements - Elementos com o atributo data-final-number.
 * @param {number} speed - Velocidade de incrementacao do contador.
 * @param {number} delayToStart - Espera para iniciar o contador.
 * @param {function} callback - Após o contador acontecer, chama esta função.
 */
const contador = function(elements, speed = 1, delayToStart = 0, callback=undefined) {
    
    setTimeout(incrementador, delayToStart);

    function incrementador() {
        'use strict'

        for (let element of elements) {
            let startNumber = parseInt(element.innerText),
                endNumber = parseInt(element.getAttribute('data-final-number'));
            setInterval(
                () => {
                    if (startNumber < endNumber) {
                        startNumber++
                        element.innerText = startNumber
                    }
                }
                , speed
            );
        }
        if (callback) callback();
    }
}
