from flask import Blueprint
routes = Blueprint('routes', __name__)

from .face import *
from .user import *
from .auth import *