from flask import Blueprint, render_template

view = Blueprint('register_view', __name__, template_folder='templates', static_folder='static', static_url_path='/static/controllers')


@view.route('/register')
def admin_register():
    return render_template('register.html')
