#!/usr/bin/env bash
set -e
cmd="$@"

function mysql_ready() {
    python << END
import sys
import MySQLdb
try:
    conn = MySQLdb.connect(db="$MYSQL_DATABASE",
                           user="$MYSQL_USER",
                           password="$MYSQL_PASSWORD",
                           host="$DB_SERVICE")
except MySQLdb.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until mysql_ready; do
    >&2 echo "MySQL is unavailable - sleeping"
    sleep 1
done

>&2 echo "MySQL is up - continuing..."
exec $cmd