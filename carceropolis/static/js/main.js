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
    $('body').scrollspy({ target: '#dados-bar' })

    $('#dados-bar').on('activate.bs.scrollspy', function (event) {

        let ativo = $(event.target).find('a').attr('href')

        switch (ativo) {
            case `#dados-gerais`:
                /*
                1. Dados Gerais
                - número 622 inciando normal e tornando-se negrito
                - animação (contador) no 111%
                */
                $(`${ativo} [data-tobold]`).addClass(`toBold`)
                contador(document.querySelectorAll(`${ativo} [data-final-number]`), 12, 1500)
                setTimeout(
                    () => $(`${ativo} .anim1`).addClass(`bounceInDown`)
                    , 3000
                )
                break

            case `#perfil-populacional`:
                /*
                  2. Perfil Populacional
                  - aparecer primeiro o bloco "A população carcerária..."
                  - aparecer depois o gráfico, animando a linha 
                  - aparecer depois o Estado de São Paulo e preencher proporcionalmente a 35% da área (animação)
                  - aparecer, por fim, o bloco "segundo dados do IBGE..."
                */
                $(`${ativo} .anim1`).addClass(`slideInLeft`)
                $(`${ativo} svg .linha`).attr(`class`, `linha full`)

                setTimeout(
                    () => $(`${ativo} .anim2`).addClass(`slideInUp`).removeClass(`anim2`)
                    , 3000
                )
                setTimeout(
                    () => $(`${ativo} .anim3`).addClass(`slideInUp`).removeClass(`anim3`)
                    , 4500
                )
                break

            case `#perfil-populacional`:
                /* 
               3. Infraestrutura
               - fixar topo e rodapé (sobre déficit)
               - aparecer os blocos conforme usuário rolar o scroll 
               */
                break

            case `#situacao-juridica`:
                contador(document.querySelectorAll('#situacao-juridica [data-final-number]'), 20)
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
                break

            case `#saude`:
                contador(document.querySelectorAll('#saude [data-final-number]'), 20)
                /*  6. Saúde
                - aparecer o texto "consultório médico"
                - "Saúde" e texto "Apesar da metade..." na mesma cor do atual texto "49 ginecologistas..." com fundo branco
                - animação (contador) no 49
                - número 36.495 inciando normal e tornando-se negrito
                - entrar próxima caixa de texto, sem o "3 vezes..." e os caixões
                - por fim, aparecer o "3 vezes mais chances de morrer" e os 3 caixoes concomitantemente */
                break

            case `#materno-infantil`:
                contador(document.querySelectorAll('#materno-infantil [data-final-number]'), 1)
                /*  7. Materno-infantil
                - animação (contador) no 534
                - animação (contador) no 585 */
                break

            case `#alas-exclusivas`:
                contador(document.querySelectorAll('#alas-exclusivas [data-final-number]'), 50)
                /* 8. Alas Exclusivas
                - animação (contador) no 12%
                - número 1.294 inciando normal e tornando-se negrito
                - preencher celas vermelhas e depois as cadeiras de rodas brancas */
                break

            default:
                console.log("Animation error")
        }
    })

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
function contador(elements, speed = 1, delay = 0) {

    setTimeout(incrementador, delay)

    function incrementador() {

        for (let element of elements) {

            let startNumber = parseInt(element.textContent),
                endNumber = parseInt(element.getAttribute('data-final-number'))

            setInterval(
                () => {

                    if (startNumber < endNumber) {

                        startNumber++
                        element.textContent = startNumber

                    }
                }
                , speed
            )

        }
    }
}