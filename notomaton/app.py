from flask import Flask
app = Flask('notomaton')
from . import routes
from .sync import sync_assets
sync_assets()
