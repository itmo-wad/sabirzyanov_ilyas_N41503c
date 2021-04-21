from flask import Flask, request, render_template, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager, login_user, current_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qweqweqweqweeqqwe'


class User(UserMixin):
    def __init__(self, username, password):
        self.id = '1'
        self.password = password
        self.username = username

    def __repr__(self):
        return f"User('{self.username}', '{self.password}')"


registered_users = {
    'username_1': 'pass1'
}
users = {}

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form.get('password')
        username = request.form.get('username')
        if username in registered_users:
            if registered_users.get(username) == password:
                user = User(username=username, password=password)
                users[user.id] = user
                login_user(user)
                return redirect(url_for('cabinet'))
        flash('Login Unsuccessful. Please check email and password')
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/cabinet')
@login_required
def cabinet():
    return render_template('cabinet.html')


@app.route('/<path:path>')
def index3(path):
    return app.send_static_file(path)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
