
from db.database import db_conn
from flask import Flask, request,Blueprint
from handlers.message_handler import handle_message
from db.init_db import init_db
import logging
from routes.webhook import webhook_bp


logging.basicConfig(level=logging.DEBUG)
#init_db()

app = Flask(__name__)
app.debug = True
app.register_blueprint(webhook_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)