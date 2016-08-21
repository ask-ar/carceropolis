## INSTALAÇÃO (para desenvolvimento)
Abaixo os principais passos para instalação do projeto em ambiente de desenvolvimento.

### GNU/Linux - Básico
Sistemas GNU/Linux contém python por padrão, então o que precisaremos é garantir que duas aplicações python estejam instaladas:

```
sudo apt-get install python-pip
sudo pip install virtualenv
```

### MacOS - Básico
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

O passo seguinte é navegar até a pasta do projeto carcerópolis.

Agora iremos criar um 'virtualenv' ('ambiente virtual'), que ficará armazenado
na pasta "venv":

```
virtualenv venv
```

Com o ambiente criado, o passo seguinte é "ativá-lo", ou seja, dizer que na
sessão atual do terminal o python a ser utilizado é o do "ambiente virtual"
(então todas as istalações serão feitas só no contexto desse ambiente)

```
source venv/bin/activate
```

Agora iremos instalar os requisitos do projeto no ambiente virtual:

```
pip install -r requirements.txt
```

O presente projeto é desenvolvido em Django. dessa forma, ele possui um arquivo
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
python manage.py createdb
python manage.py migrate
```

Agora, para ver o projeto rodando, utilize o comando abaixo:

```
python manage.py runserver
```

e visite, em seu navegador, o endereço: http://127.0.0.1:8000
