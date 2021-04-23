from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory
from flask_login import UserMixin, LoginManager, login_user, login_required
from flask_pymongo import PyMongo, ObjectId
from werkzeug.utils import secure_filename
import os


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './upload'
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


login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(username=user['username'], password=user['password'], id=user['_id'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


@app.route('/cabinet', methods=['GET', 'POST'])
@login_required
def cabinet():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Invalid file extension')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            flash('Successfully saved', 'success')
            return redirect(url_for('uploaded_file', filename=filename))
    if request.method == 'GET':
        return render_template('cabinet.html')


@app.route('/<path:path>')
def index3(path):
    return app.send_static_file(path)


@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
