from flask import Blueprint
routes = Blueprint('routes', __name__)

from .face import *
from .partner import *
from .auth import *
from .user import *