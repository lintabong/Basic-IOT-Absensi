from flask import Blueprint, render_template

view = Blueprint('login_view', __name__, template_folder='templates', static_folder='static', static_url_path='/static/controllers')


@view.route('/login', methods=['GET','POST'])
@view.route('/index')
@view.route('/')
def admin_login():
    return render_template('login.html')
