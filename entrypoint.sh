#!/bin/sh

# Generate password hash for admin user
hashedPass=$(/opt/venv/cardinal/bin/python -c 'from werkzeug.security import generate_password_hash; print(generate_password_hash("'$CARDINAL_PASSWORD'", "sha256"))')

# Test MariaDB connectivity
for i in `seq 1 60`;
    do sleep 1;
        if nc -vz mariadb 3306; then
            mysql -h mariadb -u"$CARDINAL_SQL_USERNAME" -p"$CARDINAL_SQL_PASSWORD" cardinal -e "INSERT INTO users (username,password) VALUES ('$CARDINAL_USERNAME','$hashedPass')"
            break
        else
            echo "Retrying MariaDB connection..."
            continue
        fi
    done

# Initiate NGINX for uWSGI
/usr/sbin/nginx -c /etc/nginx/nginx.conf

# Initiate uWSGI
cd /opt/Cardinal/webapp && /opt/venv/cardinal/bin/uwsgi --ini wsgi.ini --master --enable-threads

# Initiate rq worker for asynchronous work
cd /opt/Cardinal/webapp && /opt/venv/cardinal/bin/rq worker high default low -u redis://redis &
