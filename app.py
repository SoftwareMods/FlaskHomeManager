import os, ssl
#import routes
from routes.frontend import frontend
from routes.bills import bills
from routes.tasks import tasks
from routes.chores import chores
from routes.journal import journal
from routes.school import school
from routes.study import study
from routes.shopping import shopping
from routes.settings import settings

from flask import Flask, session
from flask_talisman import Talisman
import tempfile

HOME_PATH = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = tempfile.gettempdir()
app.config.from_pyfile('config.py')
app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

# Our application uses blueprints as well; these go well with the
# application factory. We already imported the blueprint, now we just need
# to register it:
app.register_blueprint(frontend)
app.register_blueprint(bills)
app.register_blueprint(tasks)
app.register_blueprint(chores)
app.register_blueprint(journal)
app.register_blueprint(school)
app.register_blueprint(study)
app.register_blueprint(shopping)
app.register_blueprint(settings)

csp = {
        'default-src': "'self' http://localhost:8081 data: 'unsafe-inline'",
        'child-src': "'none'",
        'object-src': "'none'"
}
talisman = Talisman(app, content_security_policy=csp)

if __name__ == '__main__':
    talisman.run('127.0.0.1', 8081, debug=True)
