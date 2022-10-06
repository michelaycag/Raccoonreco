from flask import Blueprint
routes = Blueprint('routes', __name__)

from .recognize import *
from .user import *