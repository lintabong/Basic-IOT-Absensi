from flask import Blueprint, render_template
from config.firebase import firebase_config


view = Blueprint('add_user_view', __name__, template_folder='templates', static_folder='static', static_url_path='/static/pages')


@view.route('/adduser')
def addUser():
    return render_template('add_user.html')
