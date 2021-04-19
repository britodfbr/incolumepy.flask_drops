import db
from flask import Flask, abort, url_for
from converters import RegexConverter


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter

@app.route('/')
def index():
    html = ['<ul>', '</ul>']
    for username, user in db.users.items():
        html.insert(1, f"<li><a href='{url_for('user', username=username)}'>{user['name']}</a></li>")
    return '\n'.join(html)


def profile(username):
    user = db.users.get(username)
    if not user:
        return abort(404, "User not found")
    return f"""<h1>{user['name']}</h1>
    <img src="{user['image']}" /> <br />
    Telefone: {user['phone']} <br />
    <a href="/">Voltar</a>
    """


app.add_url_rule('/users/<username>/', view_func=profile, endpoint='user')


@app.route('/users/<username>/<int:quote_id>/')
def quote(username, quote_id):
    user = db.users.get(username)
    if user and quote_id:
        quote = user.get('quote').get(quote_id)

        return f"""<h1>{user['name']}</h1>
        <img src="{user['image']}" /> <br />
        Telefone: {user['phone']} <br />
        <p><q>{quote}</q></p>
        <hr />"""
    else:
        return abort(404, "User not found")


@app.route('/files/<path:filename>')
def filepath(filename):
    return f"filename: {filename}"


@app.route('/reg/<regex("a.*"):name>/')
def reg(name):
    return F"Argumento iniciado com a letra a: {name}"


@app.route('/reg/<regex("e.*"):name>/')
def reg_2(name):
    return F"Argumento iniciado com a letra e: {name}"

app.run(use_reloader=True, host='0.0.0.0', port=8080)
