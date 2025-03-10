# Install app

## Create isolate environment

```bash
python -m venv venv
```

## Active isolate environment

```bash
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Update submodule source code

```bash
git submodule update --init --recursive
```

## Migrate database

```bash
python manage.py migrate
```

## Run command create group default(for user)

```bash
python manage.py user_add_groups
```

## Run command create group default(for coin)

```bash
python manage.py coin_add_groups
```

## Create super user

```bash
python manage.py createsuperuser
```

## Run app

```bash
python manage.py runserver
```

## Other command

### Run command create wallet

```bash
python manage.py add_wallets
```

> Case: System already user, coin app add later. Old user have not wallet

### Run command test

```bash
python manage.py test app/[app_name]
```

### Show urls

> Requirment : `django-extension` app in `setting.py`

```bash
python manage.py show_urls
```

### Language

#### Tools

- getext: Unzip and add bin to environment path

- poedit: Editor for translation

#### Find and make `po` file

```bash
python manage.py makemessages -l vi
```

#### Apply po file

```bash
python manage.py compilemessages 
```

#### Required libraries when using salary app in linux or Window

> Note: Install before running the command python manage.py migrate

 * Window
    - msys2: install app https://www.msys2.org/#installation

    - gtk2-runtime: install app https://sourceforge.net/projects/gtk-win/

 * Linux 
    - mingw-w64: sudo apt install mingw-w64 -y

    - gtk2.0: sudo apt-get install gtk2.0

## Build project in linux running gunicorn

#### Run create static file

```bash
B1. python manage.py collectstatic
```

#### Run project gunicorn
```bash
B2. gunicorn --bind 0.0.0.0:8000 --pythonpath app [project_name].wsgi:application
```

## Build project in docker

#### Clone source

```bash
B1. Clone code from git git@github.com:Nextcore-JSC/NextcoreApp.git
```

#### Create file .env
```bash
B2. Copy file env_example and rename to .env
```

#### Build docker container
```bash
B3. docker compose -d --build
```

#### createsuperuser 
```bash
B4. docker exec -it [container_name] python manage.py createsuperuser
```
