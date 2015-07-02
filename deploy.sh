#!/bin/sh

# Template script to use to deploy on a new VM the application
# DO NOT USE AS-IS - you must customise it to your specific service name

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
sudo apt-get update -q -y
sudo apt-get -q -y install libxml2-dev libxslt-dev python-dev lib32z1-dev
cd $DIR/..
. ../../bin/activate
pip install -r requirements.txt

sudo supervisorctl reread [service name]
sudo supervisorctl update [service name]
kill -HUP $(sudo supervisorctl pid [service name])
