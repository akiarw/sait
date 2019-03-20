from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wwdb import DBWorking


class MainForm(FlaskForm):
    main_page = SubmitField('Главная')
    editor = SubmitField('Редактор')
    authorise = SubmitField('Авторизация')
    my_acc = SubmitField('Моя коллекция')


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
            global user
            main_form = MainForm()
            red = redirection()
            if red:
                return red
            return render_template('main.html', form=main_form, user=user)

        @app.route('/sign', methods=["GET", "POST"])
        def sign():
            global user
            main_form = MainForm()
            log_form = LoginForm()

            if request.form:
                if request.form.get('sign_in'):
                    res = sign_in()
                    if res:
                        return res

                elif request.form.get('sign_up'):
                    res = sign_up()
                    if res:
                        return res

            red = redirection()
            if red:
                return red
            return render_template('sign.html', form=main_form, log_form=log_form, user=user)

        @app.route('/editor', methods=["GET", "POST"])
        def editor():
            global user
            main_form = MainForm()
            red = redirection()
            if red:
                return red
            return render_template('redactor.html', form=main_form, user=user)

        @app.route('/account', methods=['GET', 'POST'])
        def account():
            global user
            main_form = MainForm()
            red = redirection()
            if red:
                return red
            return render_template('account.html', user=user, form=main_form, nickname=user.login,
                                   names=user.all_images())

        def redirection():
            if request.form:
                global user
                mp = request.form.get("main_page")
                auth = request.form.get("authorise")
                edit = request.form.get("editor")
                if mp:
                    return redirect('/main')
                elif auth:
                    user = None
                    MainForm.authorise = SubmitField('Авторизация')
                    return redirect('/sign')
                elif edit:
                    return redirect('/editor')

        def sign_in():
            global user
            login = request.form['login']
            pwd = request.form['pwd']
            user = DBWorking(login)
            if login and pwd:
                status = user.sign_in(pwd)
                if status == 'successful':
                    MainForm.authorise = SubmitField('Выход')
                    return redirect('/account')
                else:
                    print(status)

        def sign_up():
            global user
            login = request.form['reg_login']
            pwd = request.form['reg_pwd']
            repwd = request.form['pwd_again']
            user = DBWorking(login)
            if login and pwd:
                if pwd == repwd:
                    status = user.sign_up(pwd)
                    if status == 'successful':
                        MainForm.authorise = SubmitField('Выход')
                        return redirect('/account')  # сами введите нужный адрес
                    else:
                        print(status)
                else:
                    print('different passwords')


user = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Vitalya_secret_key'
serv = Server()
app.run('127.0.0.1', 8000)
