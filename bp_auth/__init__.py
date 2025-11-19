from flask import Blueprint

bp = Blueprint(
    "bp_auth",                        # имя блюпринта
    __name__,
    template_folder="templates",            # относительный путь от папки bp_request
    static_folder="static",                 # относительный путь от папки bp_request
)
from . import access
from . import auth