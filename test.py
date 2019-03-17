from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class MainForm(FlaskForm):
    main_page = SubmitField('Главная')
    editor = SubmitField('Редактор')
    authorise = SubmitField('Авторизация')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class Server:
    def __init__(self):
        @app.route('/', methods=["GET", "POST"])
        @app.route('/main', methods=["GET", "POST"])
        def main():
            form = MainForm()
            red = redirection()
            if red:
                return red
            return render_template('main.html', form=form)

        @app.route('/sign', methods=["GET", "POST"])
        def sign():
            form = MainForm()
            log_form = LoginForm()
            red = redirection()
            if red:
                return red
            return render_template('sign.html', form=form, log_form=log_form)

        @app.route('/editor', methods=["GET", "POST"])
        def editor():
            form = MainForm()
            red = redirection()
            if red:
                return red
            return render_template('redactor.html', form=form)

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


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Alexcoratt_secret_key'
serv = Server()
app.run('127.0.0.1', 8000)
