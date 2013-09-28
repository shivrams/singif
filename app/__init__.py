from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, send_from_directory

frontend_app = Flask(__name__)
backend_app = Flask(__name__)

frontend_app.config.from_object('config')
backend_app.config.from_object('config')

db = SQLAlchemy(backend_app)

from app.api.views import mod as api_module
backend_app.register_blueprint(api_module)

from app.player.views import mod as player_module
frontend_app.register_blueprint(player_module)

#controllers
@frontend_app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@frontend_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@frontend_app.route("/test")
def index():
    return 'hmmm'
