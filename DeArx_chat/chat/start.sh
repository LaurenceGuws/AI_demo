#!/bin/sh
if [ ! -f /app/instance/chat.db ]; then
    flask setup
fi
flask run --debug --host=0.0.0.0 --port=5000
