#!/usr/bin/env sh
# Install custom python package if requirements.txt is present
if [ -e "/project/requirements.txt" ]; then
    pip install -r /project/requirements.txt
fi

TRY_LOOP="20"

wait_for_port() {
  local name="$1" host="$2" port="$3"
  local j=0
  while ! nc -z "$host" "$port" >/dev/null 2>&1 < /dev/null; do
    j=$((j+1))
    if [ $j -ge $TRY_LOOP ]; then
      echo >&2 "$(date) - $host:$port still not reachable, giving up"
      exit 1
    fi
    echo "$(date) - waiting for $name ($host:$port)... $j/$TRY_LOOP"
    sleep 5
  done
}

cleanup() {
    # Cleanup instance files, such as socket files, test files and so on.
    echo "Doing exit cleanup."
    echo "  - Removing /sockets folder."
    rm -rf /sockets
    rm -rf /project/static/[a-jt-z]* /project/static/mezzanine
    rm -rf /project/carceropolis/htmlcov
    rm -rf /project/.coverage
}

deploy() {
    echo "Loading initial data."
    echo "  Collecting static files."
    python manage.py collectstatic --noinput
    echo "  Making migrations."
    python manage.py makemigrations
    echo "  Applying migrations."
    python manage.py migrate --no-input
    echo "####################################################################"
    echo "\n\n  Loading cidades fixtures.\n"
    python manage.py loaddata cidades/fixtures/cidades.json.bz2
    echo "####################################################################"
    echo "\n\n  Loading carceropolis fixtures.\n"
    python manage.py loaddata carceropolis/fixtures/initialdata.json.bz2
}

wait_for_db() {
    local host=${DB_HOST:-db}
    local port=${DB_PORT:-5432}

    wait_for_port "Postgres" "$host" "$port"
}

case "$1" in
  migrate)
    echo "Initializing migrate mode."
    wait_for_db
    python manage.py makemigrations
    python manage.py migrate --no-input
    ;;
  clean)
    echo "Initializing cleaning mode."
    cleanup
    ;;
  *)
    echo "Default initialization."
    wait_for_db
    if [ ! -e "/project/carceropolis/static/.initial_load_done" ]; then
        echo "First run! Running deploy script."
        deploy
        touch /project/carceropolis/static/.initial_load_done
    fi
    echo "  Running migrations."
    python manage.py migrate
    echo "  Collecting static files."
    python manage.py collectstatic --noinput
    echo "Starting uwsgi"
    uwsgi --ini /project/deploy/uwsgi.ini
    ;;
esac
