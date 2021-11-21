from flask import Flask
from LogCorona.init_db import get_db
from LogCorona.loggers import init_logger

app = Flask(__name__)
app_logger = init_logger()

if app.config['ENV'] == 'ProductionConfig':
    app.config.from_object('config.ProductionConfig')
    db = get_db()
else:
    app.config.from_object('config.TestingConfig')
    db = get_db()

from LogCorona import routes
