from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wwdb import DBWorking
import os


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


class EditForm(FlaskForm):
    filename = FileField('Выбрать изображение', validators=[DataRequired()])
    get_im = SubmitField('Подтвердить')


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
            res = None

            if request.form:
                if request.form.get('sign_in'):
                    res = sign_in()
                    if type(res) != str:
                        return res

                elif request.form.get('sign_up'):
                    res = sign_up()
                    if type(res) != str:
                        return res

            red = redirection()
            if red:
                return red
            return render_template('sign.html', form=main_form, log_form=log_form, user=user,
                                   status=res if type(res) == str else '')

        @app.route('/editor', methods=["GET", "POST"])
        def editor():
            global user
            main_form = MainForm()
            edit_form = EditForm()
            red = redirection()
            if red:
                return red
            return render_template('redactor.html', form=main_form, user=user, edit_form=edit_form)

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
                if request.form.get("main_page"):
                    return redirect('/main')
                elif request.form.get("authorise"):
                    user = None
                    MainForm.authorise = SubmitField('Авторизация')
                    return redirect('/sign')
                elif request.form.get("editor"):
                    return redirect('/editor')
                elif request.form.get("my_acc"):
                    return redirect('/account')

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
                return status

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
                    return status
                return 'different passwords'


user = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Vitalya_secret_key'
serv = Server()
app.run('127.0.0.1', 8000)
