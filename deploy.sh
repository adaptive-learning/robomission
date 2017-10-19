#!/bin/sh
# deployment script run by Viper server after push

echo "Starting deploy script"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
make install
python $DIR/backend/manage.py collectstatic --noinput
