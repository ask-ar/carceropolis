# INSTALAÇÃO (para desenvolvimento local)
Abaixo os principais passos para instalação do projeto em ambiente de desenvolvimento.

## Desenvolvendo com Docker
Para facilitar o ambiente de desenvolvimento também disponibilizamos um
Dockerfile e um docker-compose.

Assim, para poder utilizar estes recursos, você precisará ter instalado em seu
sistema o [Docker](https://docs.docker.com/engine/installation/)
(versão Community Edtion >= 17.06) e o
[docker-compose](https://docs.docker.com/compose/install/) (versão >= 1.15.0).

Após instalar ambos, faça o clone deste repositório em algum diretório em seu
computador.

Estando no diretório do repositório, utilize o seguinte comando para iniciar o
projeto completo: `docker-compose up`. Se desejar rodar o projeto em
background, utilize a flag `-d`: `docker-compose up -d`.

Na primeira vez em que você rodar o projeto e criar os containers, será
realizada uma rotina de configuração da base de dados e também o carregamento
(load) de dados pré-configurados. Esse processo pode demorar um pouco (menos de
um minuto em média).

Se o projeto estiver rodando em "foreground" e você quiser pará-lo, basta
pressionar ctrl+c. Se ele estiver rodando em background, rode
`docker-compose stop`. Se quiser apagar os containers e volumes criados para
realizar uma nova instalação do zero, basta rodar `docker-compose down -v`.

Caso hajam alterações na base, para gerar novas "migrations" basta rodar
`docker-compose exec carceropolis python3 manage.py makemigrations` (com o
projeto rodando).

Por fim, vale destacar que qualquer modificação nos arquivos da pasta clonada
em seu sistema será automaticamente aplicada à instancia do projeto sendo
executada.

#### Problemas com Docker
Execute os comandos no **diretório do Carcerópolis** para apagar todas as imagens e container referente ao projeto. Após isto reinicie o processo de instalação.

1. Remover todas as imagens:
```bash
docker-compose down --rmi all -v --remove-orphans
```

2. Remover todos os containers:
```bash
docker-compose rm -f -s -v
``` 

3. Verificar se ainda tem algum container:
```bash
docker ps -a 
```
Caso positivo, remover cada um manualmente com:
```bash
docker container rm <container_id>
```

#### Atualizando arquivos estáticos
Para atualizar os arquivos estáticos do projeto, enquanto o Docker roda em um terminal, em outro execute este comando:
```bash
docker-compose exec carceropolis python manage.py collectstatic --no-input
```

## Server local (sem Docker)
### GNU/Linux - Básico
Sistemas GNU/Linux contém python por padrão, então o que precisaremos é
garantir que duas aplicações python estejam instaladas: O projeto está rodando
com Python3.

```
sudo apt install python3 python3-pip
sudo pip3 install virtualenv
```

Além disso, você precisa instalar o postgresql:
```
sudo apt install postgresql
```

### MacOS - Básico

> Esta seção precisa ser revisada para "subir" de python2 para python3.

Para instalar o projeto localmente precisamos do Python. No caso do Mac, iremos
utilizar o `Homebrew`. Para instalá-lo, rode a linha de comando abaixo em um
Terminal (para mais informações: http://brew.sh/):

```
sudo /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Adicione a linha abaixo no final do arquivo `~/.profile` (`~` é a pasta
principal do seu usuário).

```
export PATH=/usr/local/bin:/usr/local/sbin:$PATH
```

Agora iremos instalar o ``python`` propriamente dito.

```
sudo brew install python
```

Para mais informações:
http://docs.python-guide.org/en/latest/starting/install/osx/

Em teoria, junto do ``python`` será instalado também o ``pip``, que é um
software para instalação automatizada de outros pacotes ``python``.

Para verificar se a instalação ocorreu corretamente, execute, no terminal, o
seguinte comando:

```
pip --version
```

Eventualmente o ``pip`` pode não ter sido instalado corretamente, e, dessa
forma, você irá observar uma mensagem de erro.
Caso isso ocorra, tente seguir os seguintes passos:

```
sudo brew install openssl
sudo brew install curl --with-openssl
sudo brew link --force openssl
sudo brew reinstall python
```

Para mais informações:
http://stackoverflow.com/questions/15185661/update-openssl-on-os-x-with-homebrew

Seguindo com a instalação do projeto.....

Primeiramente iremos instalar o ``virtualenv``, para nos ajudar na organização
do ambiente ``python`` (para conhecer melhor:
https://virtualenv.pypa.io/en/stable/) :

```
sudo pip install virtualenv
```

### Para todas as plataformas
Seguindo com a instalação localmente depois dos ambientes configurados.

O passo seguinte é navegar até a pasta do projeto carceropolis.

Agora iremos criar um 'virtualenv' ('ambiente virtual'), que ficará armazenado
na pasta "venv":

```
virtualenv venv
```

Com o ambiente criado, o passo seguinte é "ativá-lo", ou seja, dizer que na
sessão atual do terminal o python a ser utilizado é o do "ambiente virtual"
(então todas as instalações serão feitas só no contexto desse ambiente)

```
source venv/bin/activate
```

Vamos nos certificar de que estamos com o virtualenv rodando python3:
```
python --version
```

Verifique o output para confirmar se o python do venv é de alguma versão do
python3. Caso não seja, será preciso criar novamente o venv com python3 (veja
seção abaixo `Virtualenv com python3` sobre isso.)

Continuando, agora iremos instalar os requisitos do projeto no ambiente
virtual:

```
pip install -r requirements.txt
```

O presente projeto é desenvolvido em Django. Dessa forma, ele possui um arquivo
de configuração (settings.py), que, no nosso caso, fica no diretório
`carceropolis`. Este arquivo contém as configurações principais e gerais do
projeto. Precisamos também de um segundo arquivo, de nome `local_settings.py`,
que conterá as configurações mais detalhadas que não deverão ser salvas no
repositório git por conterem informações sensíveis.

Assim, crie o arquivo `local_settings.py` no diretório `carceropolis` (o mesmo
aonde está o `settings.py`). Este arquivo deverá conter o conteúdo abaixo,
com as devidas modificações de conteúdo/valor das variáveis:

    # This file is exec'd from settings.py, so it has access to and can
    # modify all the variables in settings.py.

    # If this file is changed in development, the development server will
    # have to be manually restarted because changes will not be noticed
    # immediately.

    DEBUG = True

    # Make these unique, and don't share it with anybody.
    SECRET_KEY = "as9d8j(*HJw(*&DHWQ87d!HQW87dhQ87whd(*"
    NEVERCACHE_KEY = "&!@HFDmfmfiwfm8)#$*jfmkaslmdapdo213#@)"

    DATABASES = {
        "default": {
            # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
            "ENGINE": "django.db.backends.sqlite3",
            # DB name or path to database file if using sqlite3.
            "NAME": "dev.db",
            # Not used with sqlite3.
            "USER": "",
            # Not used with sqlite3.
            "PASSWORD": "",
            # Set to empty string for localhost. Not used with sqlite3.
            "HOST": "",
            # Set to empty string for default. Not used with sqlite3.
            "PORT": "",
        }
    }

    ###################
    # DEPLOY SETTINGS #
    ###################

    # Domains for public site
    ALLOWED_HOSTS = [""]


**ATENÇÃO**: SE VOCÊ ESTIVER USANDO O DOCKERFILE/DOCKER-COMPOSE PARA RODAR O
PROJETO, CONFIGURE O **NAME** COMO `postgres`, **USER** COMO `postgres` e
**HOST** COMO `db`. Comente ou remova a linha do **PASSWORD**.

Agora iremos rodar o projeto para que as principais configurações sejam
implementadas:

```
python manage.py migrate
python manage.py loaddata cidades/fixtures/cidades.json.bz2
python manage.py loaddata carceropolis/fixtures/initialdata.json.bz2
```

Agora, para ver o projeto rodando, utilize o comando abaixo:

```
python manage.py runserver
```

E visite, em seu navegador, o endereço: http://127.0.0.1:8000

#### Virtualenv com python3

Caso você tenha criado um virtualenv com python2 ao invés de python3, saia do
virtualenv (`deactivate`), remova o diretório do virtualenv (`rm venv`), e rode
o comando:
```
virtualenv venv $(which python3)
```

Pronto, agora você tem um virtualenv com a versão do python3 instalada no seu
sistema. =)

## Trabalhando com o CSS
Este projeto utiliza o Compass para escrever CSS. O Compass é um
pre-processador de CSS escrito em Ruby, no qual seu output é CSS puro.

Para utilizar o Compass, você deve instalar o [Ruby](http://rubyinstaller.org/)
em seu computador e depois instalar o [Compass](http://compass-style.org/).

Após instalação, você pode verificar as configurações de compilação no arquivo
`./carceropolis/config.rb`

Os arquivos .scss (compass) estão no diretório `./carceropolis/scss`

Para trabalhar com arquivos .sccs você deve iniciar o serviço que observa
modificações neles, para compilar-los assim que salvos. Para isto você deve
digitar no terminal no diretório onde o arquivo `config.rb` está salvo.

`$ compass watch`

Siga a sintaxe da linguagem para realizar as modificações necessárias.

Nunca faça modificações direto nos arquivos CSS pois estes serão apagados a
toda nova compilação do Compass.

Para compilar apenas uma vez:

`$ compass compile`

Parar parar o watch `control c`

### Compass no Linux
Caso obtenha o seguinte erro no terminal após executar o comando `compass watch`

```
FATAL: Listen error: unable to monitor directories for changes.
Visit https://github.com/guard/listen/wiki/Increasing-the-amount-of-inotify-watchers for info on how to fix this
```
Execute este comando e após isto o watcher voltará a funcionar:
`echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p`

## Exportando a base de dados
Para exportar a base de dados após alterar algum dado, de forma que ela possa
ser reimportada, o comando a ser executado é:
`./manage.py dumpdata --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission > initialdata.json`

Para importá-lo de volta à base utilize:
`./manage.py loaddata initialdata.json`

Vale a ressalva que se o projeto estiver sendo rodado utilizando Docker, esses
comandos devem ser rodados no container em execução:

`docker exec <CONTAINER_ID> python3 manage.py ...`

## Geolocalização dos dados

Para geolocalizar unidades prisionais que estejam na base, usar o seguinte comando:

    python manage.py geolocate

Pode ser usado o parâmetro `--all` para forçar a geolocalização de todas as unidades.

É usada uma cache local (`geo.cache`) para armazenar os retornos das APIs de mapeamento, agilizando o processo.

## Traduções

Para traduzir algum texto, primeiro adicione o que quer traduzir com `{% trans "palavra ou id" %}`, depois gere os `.po`:

    python manage.py makemessages -l en -l pt_BR

Depois edite:

    carceropolis/carceropolis/locale/en/LC_MESSAGES/django.po
    carceropolis/carceropolis/locale/pt_BR/LC_MESSAGES/django.po

E por fim compile:

    python manage.py compilemessages

Mais informações aqui: https://docs.djangoproject.com/en/2.0/topics/i18n/translation/
