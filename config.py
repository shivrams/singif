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
CSRF_SESSION_KEY = "Wa$t3Be1//Gpr0ducli\/3"

THREADS_PER_PAGE = 8
ADMINS = frozenset(['live2bshiv@gmail.com', 'tobyfox@gmail.com'])


#DB config
DATABASE = 'singif_staging.db'
if SINGIF_IS_LIVE:
    DATABASE = 'singif.db'


DATABASE_PATH = os.path.join(_basedir, DATABASE)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

#API Keys
GIPHY_API_KEY = "dc6zaTOxFJmzC"
TUNEWIKI_API_KEY = ""
METROLYRICS_API_KEY = "1234567890123456789012345678901234567890"
