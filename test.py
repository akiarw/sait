import os
from random import randrange, choice

from flask import Flask, render_template, redirect, request, session
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

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
    submit = SubmitField('Применить')
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
    return None


def name_next_image(name):
    num = int(name.split(')', maxsplit=1)[0][1:])
    name = '({}){}'.format(num + 1, name.split(')', maxsplit=1)[1])
    return name


def make_id():
    name = ''
    dirs = os.listdir('static/editor')
    while True:
        for i in range(30):
            name += chr(choice([randrange(49, 57), randrange(65, 91), randrange(97, 123)]))
        if name not in dirs:
            return name


def make_edit_dir():
    try:
        session['path'] = 'static/editor/{}/'.format(session['id'])
        os.mkdir(session['path'])
    except FileExistsError:
        pass
    except FileNotFoundError:
        session['id'] = make_id()


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


@app.route('/edit_step2', methods=["GET", "POST"])
def edit_step2():
    main_form = MainForm()
    red = redirection()
    session['image'] = Processing(session['path'] + session['im_name'])
    if red:
        return red
    if request.form.get('submit'):
        x, y = int(request.form['x']), int(request.form['y'])
        session['image'].resize(x, y, True)
        session['im_name'] = name_next_image(session['im_name'])
        session['image'].save(session['path'] + session['im_name'])
    elif request.form.get("to_step3"):
        return redirect('/edit_step3')
    return render_template('edit_step2.html', form=main_form, id=session['id'], name=session['im_name'])


@app.route('/edit_step3', methods=["GET", "POST"])
def edit_step3():
    main_form = MainForm()
    red = redirection()
    if red:
        return red
    if request.form.get('sepia'):
        session['image'].sepia()
        session['im_name'] = name_next_image(session['im_name'])
        session['image'].save(session['path'] + session['im_name'])
    return render_template('edit_step3.html', form=main_form, id=session['id'], name=session['im_name'])


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
        session['im_name'] = '(1)' + str(image).split("'")[1]
        session['ims'] = [session['im_name']]
        with open(session['path'] + session['im_name'], 'wb') as file:
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
