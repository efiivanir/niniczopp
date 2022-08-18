from flask import Blueprint

bp = Blueprint('davids', __name__)

from app.davids import routes