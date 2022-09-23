from flask import Blueprint, render_template
from config.firebase import firebase_config


view = Blueprint('attendance_view', __name__, template_folder='templates', static_folder='static', static_url_path='/static/pages')


@view.route('/attendance')
def attendance_page():
    return render_template('attendance.html')
