from flask import Blueprint, render_template

view = Blueprint('dash_view', __name__, template_folder='templates', static_folder='static', static_url_path='/static/pages')


@view.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')
