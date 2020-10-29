#!/bin/sh

#zapnuti mongod pro mlabweb.
if ! pidof -x mongod > /dev/null; then
    mongod --config /etc/mongod.conf > /dev/null &
fi

cd /data/MLABweb/src/MLABweb

if ! pidof -x mlab_web.py  > /dev/null; then
    python mlab_web.py > /dev/null &
fi

