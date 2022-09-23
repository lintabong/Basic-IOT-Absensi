from flask import Blueprint, session

view = Blueprint('logout_view', __name__, template_folder='templates', static_folder='static', static_url_path='/static/controllers')


@view.route('/logout')
def admin_logout():
    session.pop()
    return {'message':'logout'}
