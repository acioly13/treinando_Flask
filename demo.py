import flask
import flask.views
import os
import functools

app = flask.Flask(__name__)

app.secret_key = "joao"

users = {'joao'}


class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')

    def post(self):
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return flask.redirect(flask.url_for('index'))
        required = ['username', 'passwd']
        for r in required:
            if r not in flask.request.form:
                flask.flash("Erro: {0} é necessário.".format(r))
                return flask.redirect(flask.url_for('index'))
        username = flask.request.form['username']
        passwd = flask.request.form['passwd']
        if username in users:
            flask.session['username'] = username
        else:
            flask.flash("Usúario não Existe ou Senha Incorreta")
        return flask.redirect(flask.url_for('index'))


def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return method(*args, **kwargs)
        else:
            flask.flash("Login Necessário Para acessar a Página!")
            return flask.redirect(flask.url_for('index'))

    return wrapper


class Music(flask.views.MethodView):
    def get(self):
        songs = os.listdir('static/music')
        return flask.render_template("music.html", songs=songs)


app.add_url_rule('/',
                 view_func=Main.as_view('index'),
                 methods=["GET", "POST"])
app.add_url_rule('/music/',
                 view_func=Music.as_view('music'),
                 methods=['GET'])

app.debug = True
app.run()
