import os

_basedir = os.path.abspath(os.path.dirname(__file__))

singif_is_live = os.environ.get('SINGIF_IS_LIVE')
if singif_is_live:
    SINGIF_IS_LIVE = 1
    DEBUG = False
else:
    SINGIF_IS_LIVE = 0
    DEBUG = True

CSRF_ENABLED = True

CSRF_SESSION_KEY = os.environ.get('FLASK_CSRF_SESSION_KEY','defaultkey')

THREADS_PER_PAGE = 8
ADMINS = frozenset(['live2bshiv@gmail.com', 'tobyfox@gmail.com'])
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'defaultsecret')


#DB config
DATABASE = 'singif_staging.db'
if SINGIF_IS_LIVE:
    DATABASE = 'singif.db'


DATABASE_PATH = os.path.join(_basedir, DATABASE)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
