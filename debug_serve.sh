#!/bin/sh
source ../virtual_env/Scripts/activate

export FLASK_APP=prod
export FLASK_DEBUG=True
waitress-serve --listen=*:8081 app:app
# in browser: http://localhost:8081
