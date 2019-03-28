from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wwdb import DBWorking
import os
from PIL import Image
import sys


class Filters:

    def __init__(self, image):
        self.image = image
        self.size_x, self.size_y = self.image.size
        self.matrix = self.image.load()

    def negative(self):
        self.matrix = self.image.load()
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.matrix[x, y] = tuple(map(lambda cl: 255 - cl, self.matrix[x, y]))

    def full_monochrome(self, power=350):
        self.matrix = self.image.load()
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.matrix[x, y] = (255, 255, 255) if sum(self.matrix[x, y]) > power else (0, 0, 0)

    def monochrome(self):
        self.matrix = self.image.load()
        for x in range(self.size_x):
            for y in range(self.size_y):
                med = sum(self.matrix[x, y]) // 3
                self.matrix[x, y] = med, med, med

    def sepia(self, koeff=30):
        self.matrix = self.image.load()
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.matrix[x, y] = tuple(map(lambda cl, i: cl + koeff * i, self.matrix[x, y], range(2, -1, -1)))

    def anagliph(self, delta=10):
        self.matrix = self.image.load()
        for x in range(self.size_x - delta - 1, -1, -1):
            for y in range(self.size_y):
                r, g, b = self.matrix[x, y]
                r1, g1, b1 = self.matrix[x + delta, y]
                self.matrix[x + delta, y] = r, g1, b1

    def bright(self, koeff=10):
        self.matrix = self.image.load()
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.matrix[x, y] = tuple(
                    map(lambda cl: 255 if cl + koeff > 255 else 0 if cl + koeff < 0 else cl + koeff, self.matrix[x, y]))

    def mosaic(self, lup=(0, 0), rdwn=None, power=30):
        if not rdwn:
            rdwn = (self.size_x, self.size_y)
        for i in range(lup[1], rdwn[1], power * 2):
            self.move_fragment((lup[0], i), (rdwn[0], i + power), (-1) ** i * power)
        for i in range(lup[0], rdwn[0], power * 2):
            self.move_fragment((i + power, lup[1] - power), (i + power * 2, rdwn[1] - power), delta_y=(-1) ** i * power)


class Shaping:

    def __init__(self, image):
        self.image = image
        self.size_x, self.size_y = self.image.size
        self.sub_image = None

    def resize(self, x, y=None, is_perc=False):
        if is_perc:
            if y:
                x *= self.size_x // 100
                y *= self.size_y // 100
            else:
                x = (x[0] * self.size_x // 100, x[1] * self.size_y // 100)
        if y:
            self.image = self.image.resize((x, y))
            self.size_x, self.size_y = x, y
        else:
            self.image = self.image.resize(x)
            self.size_x, self.size_y = x

    def crop(self, lup, rdwn, is_perc=False):
        if is_perc:
            lup = (lup[0] * self.size_x // 100, lup[1] * self.size_y // 100)
            rdwn = (rdwn[0] * self.size_x // 100, rdwn[1] * self.size_y // 100)
        self.image = self.image.crop(lup + rdwn)
        self.size_x, self.size_y = self.image.size

    def move_fragment(self, lup, rdwn, delta_x=0, delta_y=0):
        self.sub_image = Processing(self.image)
        self.sub_image.crop(lup, rdwn)
        self.sub_image.paste_image((lup[0] + delta_x, lup[1] + delta_y), self)

    def paste_image(self, pos, screen=None):
        if screen:
            screen.image.paste(self.image, pos)
        else:
            sys.exit("I don't know name of screen you mean(((")

    def rotate(self, angle):
        self.image = self.image.rotate(angle)


class Processing(Filters, Shaping):

    def __init__(self, image=None):
        self.open_image(image)
        super().__init__(self.image)

    def open_image(self, image):
        if type(image) == str:
            self.image = Image.open(image)
        elif image:
            self.image = image
        else:
            sys.exit("I don't know name of image you need(((")

    def save(self, res_file='res.jpg'):
        try:
            self.image.save(res_file)
        except ValueError:
            self.image.save(res_file + '.jpg')


class MainForm(FlaskForm):
    main_page = SubmitField('Главная')
    editor = SubmitField('Редактор')
    authorise = SubmitField('Авторизация')
    my_acc = SubmitField('Моя коллекция')
    go_to_step3 = SubmitField('Перейти к следующему шагу')
    sepia = SubmitField('Сепия')
    anagliph = SubmitField('Анаглиф ')
    mosaic = SubmitField('Мозайка')
    monochrome = SubmitField('Монохром')
    full_monochrome = SubmitField('HARD Монохром')
    negative = SubmitField('Негатив')
    bright = SubmitField('Яркость')
    coll = SubmitField('Добавить в мою коллекцию')


class LoginForm(FlaskForm):
    reg_login = login = StringField('Логин', validators=[DataRequired()])
    reg_pwd = pwd = PasswordField('Пароль', validators=[DataRequired()])
    sign_in = SubmitField('Войти')

    pwd_again = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    sign_up = SubmitField('Зарегистрироваться')


class AddImageForm(FlaskForm):
    img = FileField('Выбрать изображение', validators=[DataRequired()])
    get_im = SubmitField('Перейти к следующему шагу')


class EditForm(AddImageForm):
    size_x = x = StringField('x', validators=[DataRequired()])
    size_y = y = StringField('y', validators=[DataRequired()])


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
            if request.files:
                image = request.files['img']
                global way
                name = str(image).split()[1][1:-1]
                way = make_edit_dir() + name
                with open(way, 'wb') as file:
                    file.write(image.read())
                global prc
                prc = Processing(way)
                return redirect('/edit_step2')

            if red:
                return red
            return render_template('editor.html', form=main_form, user=user, edit_form=edit_form)

        @app.route('/edit_step2', methods=['GET', 'POST'])
        def step2():
            main_form = MainForm()
            red = redirection()
            edit_form = EditForm()
            if red:
                return red
            return render_template('edit_step2.html', form=main_form, edit_form=edit_form)

        @app.route('/edit_step3', methods=['GET', 'POST'])
        def step3():
            main_form = MainForm()
            red = redirection()
            edit_form = EditForm()
            if red:
                return red
            if request.form:
                if request.form.get('sepia'):
                    prc.sepia()
                    prc.save(way)
                elif request.form.get('anagliph'):
                    prc.anagliph()
                    prc.save(way)
                elif request.form.get('mosaic'):
                    prc.mosaic()
                    prc.save(way)
                elif request.form.get('monochrome'):
                    prc.monochrome()
                    prc.save(way)
                elif request.form.get('full_monochrome'):
                    prc.full_monochrome()
                    prc.save(way)
                elif request.form.get('negative'):
                    prc.negative()
                    prc.save(way)
                elif request.form.get('bright'):
                    prc.bright()
                    prc.save(way)
                elif request.form.get('coll'):
                    try:
                        num_ph = 1
                        is_created = False
                        while not is_created:
                            coll_way = 'static/' + nickname + '/photo' + str(num_ph)
                            if os.path.isfile(coll_way + ".jpg"):
                                num_ph += 1
                            else:
                                name_ph = 'photo' + str(num_ph) + '.jpg'
                                is_created = True
                        prc.save(coll_way)
                        DBWorking(nickname).save_im_info(name_ph)
                    except NameError:
                        return redirect('/sign')
            return render_template('edit_step3.html', form=main_form, edit_form=edit_form, src=way)

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
                elif request.form.get("go_to_step3"):
                    return redirect('/edit_step3')
                elif request.form.get("apply"):
                    return redirect('/edit_step3')

        @app.route('/error', methods=['GET', 'POST'])
        def sign_in():
            main_form = MainForm()
            global user, nickname
            login = request.form['login']
            nickname = login
            pwd = request.form['pwd']
            user = DBWorking(login)
            if login and pwd:
                status = user.sign_in(pwd)
                if status == 'successful':
                    MainForm.authorise = SubmitField('Выход')
                    return redirect('/account')
                else:
                    return render_template('error.html', form=main_form)
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

        def make_edit_dir():
            global mk_dir_num
            mk_dir_num += 1
            is_created = False
            while not is_created:
                try:
                    way = 'static/A' + str(mk_dir_num) + '/'
                    os.mkdir(way)
                    is_created = True
                except FileExistsError:
                    mk_dir_num += 1
            return way


user = None
mk_dir_num = 0
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Vitalya_secret_key'
serv = Server()
app.run('127.0.0.1', 8000)
