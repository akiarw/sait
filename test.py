from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wwdb import DBWorking


class MainForm(FlaskForm):
    main_page = SubmitField('Главная')
    editor = SubmitField('Редактор')
    authorise = SubmitField('Авторизация')


class LoginForm(FlaskForm):
    reg_login = login = StringField('Логин', validators=[DataRequired()])
    reg_pwd = pwd = PasswordField('Пароль', validators=[DataRequired()])
    sign_in = SubmitField('Войти')

    pwd_again = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    sign_up = SubmitField('Зарегистрироваться')


class Server:
    def __init__(self):
        @app.route('/', methods=["GET", "POST"])
        @app.route('/main', methods=["GET", "POST"])
        def main():
            main_form = MainForm()
            red = redirection()
            if red:
                return red
            return render_template('main.html', form=main_form)

        @app.route('/sign', methods=["GET", "POST"])
        def sign():
            main_form = MainForm()
            log_form = LoginForm()

            if request.form:
                if request.form.get('sign_in'):
                    login = request.form['login']
                    pwd = request.form['pwd']
                    if login and pwd:
                        if sign_in(login, pwd) == 'successful':
                            return redirect('/account')  # сами введите нужный адрес

                elif request.form.get('sign_up'):
                    login = request.form['reg_login']
                    pwd = request.form['reg_pwd']
                    repwd = request.form['pwd_again']
                    if login and pwd:
                        if pwd == repwd:
                            if sign_up(login, pwd) == 'successful':
                                return redirect('/account')  # сами введите нужный адрес

            red = redirection()
            if red:
                return red
            return render_template('sign.html', form=main_form, log_form=log_form)

        @app.route('/editor', methods=["GET", "POST"])
        def editor():
            main_form = MainForm()
            red = redirection()
            if red:
                return red
            return render_template('redactor.html', form=main_form)

        def redirection():
            if request.form:
                mp = request.form.get("main_page")
                auth = request.form.get("authorise")
                edit = request.form.get("editor")
                if mp:
                    return redirect('/main')
                elif auth:
                    return redirect('/sign')
                elif edit:
                    return redirect('/editor')

        def sign_in(login, pwd):
            global user
            user = DBWorking(login)
            return user.sign_in(pwd)

        def sign_up(login, pwd):
            global user
            user = DBWorking(login)
            return user.sign_up(pwd)


user = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Alexcoratt_secret_key'
serv = Server()
app.run('127.0.0.1', 8090)
