from flask import Flask
from controllers import login, logout, register
from pages import dashboard, attendance, add_user, user_list

app = Flask(__name__, static_folder=None)


app.register_blueprint(login.view)
app.register_blueprint(logout.view)
app.register_blueprint(register.view)
app.register_blueprint(dashboard.view)
app.register_blueprint(attendance.view)
app.register_blueprint(add_user.view)
app.register_blueprint(user_list.view)


if __name__ == '__main__':
    app.run(debug=True)
