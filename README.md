# Flask Home Manager
## Initial Setup
By default a python environment is setup for you under serve.sh with the following, modify as desired
```
python3 -m venv ../virtual_env
source ../virtual_env/Scripts/activate
```
Before running serve.sh run these lines then run
```
pip install flask
pip install flask_talisman
pip install cryptography
pip install waitress
```
To start the application call serve.sh
```
/path/to/serve.sh
```
In your browser, navigate to localhost:8081 (or whatever port you have defined in serve.sh)


