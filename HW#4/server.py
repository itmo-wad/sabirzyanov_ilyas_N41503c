from flask import Flask, request, render_template, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager, login_user, login_required
from flask_pymongo import PyMongo, ObjectId

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qweqweqweqweeqqwe'
app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
mongo = PyMongo(app)

class User(UserMixin):
    def __init__(self, username, password, id):
        self.id = id
        self.password = password
        self.username = username

    def __repr__(self):
        return f"User('{self.username}', '{self.password}')"


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    print('here')
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(username=user['username'], password=user['password'], id=user['_id'])


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form.get('password')
        username = request.form.get('username')
        user = mongo.db.users.find_one({"username": username, "password": password})
        if user:
            print('there')
            user = User(username=user['username'], password=user['password'], id=user['_id'])
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
