from flask import Blueprint, render_template
from config.firebase import firebase_config


view = Blueprint('user_list_view', __name__, template_folder='templates', static_folder='static', static_url_path='/static/pages')


@view.route('/userlist')
def userList():
    return render_template('user_list.html')
