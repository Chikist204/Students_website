import json
from os import abort
from flask import request, make_response, jsonify
from flask import Flask, render_template, redirect
from data import db_session  # news_api
from data.users import User
from forms.user import RegisterForm
import datetime
from flask_login import LoginManager, login_required, logout_user
from flask_login import login_user
from flask_login import current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == request.form['username']).first()
        if user and user.check_password(request.form['password']):
            if request.form.get('remember-me') is None:
                login_user(user, remember=False)
            else:
                login_user(user, remember=True)
            return redirect("/")
        return render_template('login2.html', message="Неправильный логин или пароль", )
    return render_template('login2.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    return render_template("index.html")


@app.route("/about")
def about():
    with open("db/about.json", encoding="utf-8") as file:
        data = json.load(file)
    return render_template("about.html", data=data)


@app.route("/schedule")
def schedule():
    with open('db/schedule.json', encoding='utf-8') as file:
        data = json.load(file)
    return render_template("schedule.html", data=data)


@app.route("/location")
def location():
    pass


@app.route("/profile/<username>")
def profile(username):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()
    with open('db/schedule.json', encoding='utf-8') as file:
        data = json.load(file)
    if username == current_user.username:
        return render_template("profile.html", data=data)
    else:
        return render_template("profile2.html", user=user)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if request.method == 'POST':
        if request.form['password'] != request.form['password2']:
            return render_template('register2.html', message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == request.form['email']).first():
            return render_template('register2.html', message="Такой пользователь уже есть")
        if db_sess.query(User).filter(User.username == request.form['username']).first():
            return render_template('register2.html', message="Такой пользователь уже есть")
        user = User(
            name=request.form['name'],
            email=request.form['email'],
            username=request.form['username'],
            role=request.form['position'],
            group=request.form['group'],
        )
        user.set_password(request.form['password'])
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register2.html')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/students.db")
    # app.register_blueprint(news_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
