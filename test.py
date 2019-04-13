from flask import Flask, render_template, redirect, request, session
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from random import randrange
import os
from wwdb import DBWorking
import os
from processing import Processing


class FiltersForm(FlaskForm):
    sepia = SubmitField('Сепия')
    anagliph = SubmitField('Анаглиф')
    mosaic = SubmitField('Мозайка')
    monochrome = SubmitField('Монохром')
    full_monochrome = SubmitField('HARD Монохром')
    negative = SubmitField('Негатив')
    bright = SubmitField('Яркость')


class LoginForm(FlaskForm):
    reg_login = login = StringField('Логин', validators=[DataRequired()])
    reg_pwd = pwd = PasswordField('Пароль', validators=[DataRequired()])
    sign_in = SubmitField('Войти')

    pwd_again = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    sign_up = SubmitField('Зарегистрироваться')


class AddImageForm(FlaskForm):
    img = FileField('Выбрать изображение', validators=[DataRequired()])
    to_step2 = SubmitField('Перейти к следующему шагу')


class EditForm(AddImageForm):
    size_x = x = StringField('x', validators=[DataRequired()])
    size_y = y = StringField('y', validators=[DataRequired()])
    coll = SubmitField('Добавить в мою коллекцию')
    to_step3 = SubmitField('Перейти к следующему шагу')


class MainForm(FiltersForm, LoginForm, EditForm):
    main_page = SubmitField('Главная')
    editor = SubmitField('Редактор')
    authorise = SubmitField('Авторизация')
    my_acc = SubmitField('Моя коллекция')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Vitalya_secret_key'


def sign_up():
    pass


def redirection():
    if request.form:
        if request.form.get("main_page"):
            return redirect('/main')
        elif request.form.get("authorise"):
            MainForm.authorise = SubmitField('Авторизация')
            return redirect('/sign')
        elif request.form.get("editor"):
            return redirect('/editor')
        elif request.form.get("my_acc"):
            return redirect('/account')
        elif request.form.get("to_step3"):
            return redirect('/edit_step3')


def make_id():
    name = ''
    dirs = os.listdir('static/editor')
    while True:
        for i in range(30):
            name += chr(randrange(65, 123))
        if name not in dirs:
            return name


def make_edit_dir():
    try:
        session['path'] = 'static/editor/{}/'.format(session['id'])
        os.mkdir(session['path'])
    except FileExistsError:
        pass


@app.route('/', methods=["GET", "POST"])
@app.route('/main', methods=["GET", "POST"])
def main():
    if not session.get('id', None):
        session['id'] = make_id()
    main_form = MainForm()
    red = redirection()
    if red:
        return red
    return render_template('main.html', form=main_form)


@app.route('/sign', methods=["GET", "POST"])
def sign():
    main_form = MainForm()
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
    return render_template('sign.html', form=main_form, status=res if type(res) == str else '')


@app.route('/editor', methods=["GET", "POST"])
def editor():
    main_form = MainForm()
    red = redirection()
    if request.files and request.form.get('to_step2'):
        make_edit_dir()
        image = request.files['img']
        name = str(image).split("'")[1]
        with open(session['path'] + name + '1.jpg', 'wb') as file:
            file.write(image.read())
        return redirect('/edit_step2')
    if red:
        return red
    return render_template('editor.html', form=main_form)


@app.route('/account', methods=['GET', 'POST'])
def account():
    main_form = MainForm()
    red = redirection()
    if red:
        return red
    return render_template('account.html', form=main_form)


@app.route('/error', methods=['GET', 'POST'])
def sign_in():
    main_form = MainForm()
    if main_form.validate_on_submit():
        login = request.form['login']
        pwd = request.form['pwd']
        session["login"] = login


app.run('127.0.0.1', 8000)
