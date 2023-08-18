#!/bin/sh
source ../virtual_env/Scripts/activate

export FLASK_APP=app
export FLASK_DEBUG=True
flask run -h localhost -p 8081
# in browser: http://localhost:8081
