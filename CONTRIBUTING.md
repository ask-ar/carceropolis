## INSTALAÇÃO (para desenvolvimento local)
Abaixo os principais passos para instalação do projeto em ambiente de desenvolvimento.

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


Agora iremos rodar o projeto para que as principais configurações sejam
implementadas:

```
python manage.py migrate
python manage.py loaddata cidades/fixtures/cidade.json.bz2
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

### Trabalhando com o CSS
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

###Compass no Linux
Caso obtenha o seguinte erro no terminal após executar o comando `compass watch`

```
FATAL: Listen error: unable to monitor directories for changes.
Visit https://github.com/guard/listen/wiki/Increasing-the-amount-of-inotify-watchers for info on how to fix this
```
Execute este comando e após isto o watcher voltará a funcionar:
`echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p`

### Desenvolvendo com Docker
Para facilitar o ambiente de desenvolvimento também disponibilizamos um
Dockerfile e um docker-compose.

Assim, para poder utilizar estes recursos, você precisará ter instalado em seu
sistema o [Docker](https://docs.docker.com/engine/installation/)
(versão Community Edtion >= 17.06) e o
[docker-compose](https://docs.docker.com/compose/install/) (versão >= 1.15.0).

Após instalar ambos, faça o clone deste repositório em algum diretório em seu
computador e rode o seguinte comando para iniciar os containers:
`docker-compose up`. Para "desligar" o container basta apertar CTRL+C. Se quiser
subir novamente o mesmo container, rode o mesmo comando novamente.

Agora, com os containers rodando execute os seguintes comandos (considerando
que o nome do container criado é "carceropolis_web_1". Para conferir execute
`docker container ls`):

```
docker run carceropolis_web_1 python3 manage.py migrate
docker run carceropolis_web_1 python3 manage.py loaddata cidades/fixtures/cidade.json.bz2
docker run carceropolis_web_1 python3 manage.py loaddata carceropolis/fixtures/initialdata.json.bz2
```

Com isto você terá criado uma imagem docker para o postgresql (base de dados) e
outra imagem docker para o projeto carcerópolis, vinculando o diretório
corrente, aonde está o source-code do projeto, ao diretório "/project" dentro
do container chamado `web` (ou `carceropolis_web`).

Agora, para rodar o projeto utilize o comando: `docker-compose up`. Caso alguma
modificação tenha sido realizada no modelo de dados (gerando uma nova
migration), basta que você rode o comando
`docker exec carceropolis_web_1 python3 manage.py migrate`
para atualizar a base de dados.

Por fim, vale destacar que qualquer modificação nos arquivos da pasta clonada
em seu sistema será automaticamente aplicada à instancia do projeto sendo
executada.

REF: https://docs.docker.com/compose/django/#connect-the-database
