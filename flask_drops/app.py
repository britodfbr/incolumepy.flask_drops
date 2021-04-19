import db
from flask import Flask, abort, url_for

app = Flask(__name__)


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


app.add_url_rule('/profile/<username>/', view_func=profile, endpoint='user')

app.run(use_reloader=True, host='0.0.0.0', port=8080)
