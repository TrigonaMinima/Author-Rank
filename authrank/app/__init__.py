from flask import Flask

from .config import upload_folder


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
from app import views
