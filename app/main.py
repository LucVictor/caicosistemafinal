import os
import logging
import sqlalchemy
from flask import Flask, render_template, request, url_for, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import calendar
from sqlalchemy import func, case, cast, Time
from decimal import Decimal
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from babel.dates import format_datetime
from datetime import datetime, timedelta, time
from functools import wraps
import pandas as pd
import os
import numpy as np

ALLOWED_EXTENSIONS = {
    'jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'avif', 'bmp', 'ico', 'xlsx','xls'
}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] =  'app/static/uploads'
app.config['UPLOAD_FOLDER_PRANCHETA'] = 'app/static/uploads/recebimento_fotos'

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URL',
                                                  'mysql+pymysql://usuario:password@endereco/banco')
app.config["SECRET_KEY"] = "secretkey"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 28000,
    'pool_pre_ping': True
}
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Caminho completo para a pasta 'static'
static_folder = os.path.join(os.path.dirname(__file__), 'static')

# Garante que a pasta 'static' existe
os.makedirs(static_folder, exist_ok=True)

# Caminho para o arquivo de log dentro da pasta 'static'
log_file = os.path.join(static_folder, 'logs.txt')

# Configuração do logging
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a'
)

logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.DEBUG)


@app.route('/download-log')
def download_log():
    log_path = os.path.join(os.path.dirname(__file__), 'static', 'logs.txt')
    if os.path.exists(log_path):
        return send_file(
            log_path,
            as_attachment=True,
            download_name='logs.txt',
            mimetype='text/plain'
        )
    else:
        return "Arquivo de log não encontrado.", 404



from app.models.models import *
from app.functions.functions import *
from app.routes.index import *
from app.routes.avarias import *
from app.routes.entregas import *
from app.routes.vencimentos import *
from app.routes.vendas import *
from app.routes.adm import *
from app.routes.atacado import *
from app.routes.conferencia import *
from app.routes.recebimento import *
