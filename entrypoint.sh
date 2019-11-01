!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"

# Der ENTRYPOINT wird Verwendet um den Hauptbefehls für das Image festzulegen,
# sodass das Image so nach diesen Befehl ausgeführt wird
# Die ENTRYPOINT-Anweisung kann auch in Kombination mit einem Hilfsskript verwendet werden,
# sodass sie auf ähnliche Weise wie der obige Befehl funktioniert,
# auch wenn das Tool möglicherweise mehr als einen Schritt erfordert.
# Wird benötigt, damit Dei Server beim start warten bis Peotgre gebildet wird.