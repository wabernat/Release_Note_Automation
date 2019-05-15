from flask import Flask
app = Flask('notomaton')
from . import routes
