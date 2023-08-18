#!/bin/sh
source ../virtual_env/Scripts/activate

export FLASK_APP=app
export FLASK_DEBUG=False
waitress-serve --listen=*:8081 app:app
# in browser: http://localhost:8081
