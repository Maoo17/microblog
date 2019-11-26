#!/bin/sh
source venv/bin/activate
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn --statsd-host=localhost:9125 --statsd-prefix=gunicorn --bind :5000 microblog:app

# --access-logfile - --error-logfile -
# exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app
# gunicorn --statsd-host=localhost:9125 --statsd-prefix=helloworld --bind 127.0.0.1:8080 hello:app