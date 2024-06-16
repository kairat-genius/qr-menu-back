from .User import app, jwt
from .Email import app
from .Restaurant import app
from .Tables import app
from .Category import app
from .Dishes import app
from .Ingredients import app
from .Client import app
from .Support import app

from ...settings import api

api.mount("/api", app)