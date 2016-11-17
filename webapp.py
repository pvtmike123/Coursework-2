from functools import wraps
from contextlib import closing
import sqlite3 as lite
import sys
from flask import Flask, render_template, request, Response, session, g, redirect, url_for, \
     abort, flash


DATABASE = '/Users/flemin100/Documents/Uni/AWT/Coursework-2/webapp/sales.db'


app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return lite.connect(app.config['DATABASE'])


@app.route('/')
@app.route('/index')
def index():
    g.db = connect_db()
    cur = g.db.execute('select title, author, id, content from content')
    sales = [dict(title=row[0], author=row[1], id=row[2], content=row[3]) for row in cur.fetchall()]
    g.db.close()
    return render_template("index.html", sales=sales)


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/admin-home')
@requires_auth
def secret_page():
    g.db = connect_db()
    cur = g.db.execute('select title, author, id, content from content')
    sales = [dict(title=row[0], author=row[1], id=row[2], content=row[3]) for row in cur.fetchall()]
    g.db.close()
    return render_template('admin/admin.html', sales=sales)


@app.route('/admin-posts')
@requires_auth
def posts():
    g.db = connect_db()
    cur = g.db.execute('select title, author, id, content from content')
    sales = [dict(title=row[0], author=row[1], id=row[2], content=row[3]) for row in cur.fetchall()]
    g.db.close()
    return render_template('admin/admin_blog_posts.html', sales=sales)


@app.route('/my-details')
@requires_auth
def my_details():
    g.db = connect_db()
    cur = g.db.execute('select title, author, id, content from content')
    sales = [dict(title=row[0], author=row[1], id=row[2], content=row[3]) for row in cur.fetchall()]
    g.db.close()
    return render_template('admin/my_details.html', sales=sales)


@app.route('//blog_post/<page_id>')
def post(page_id):
    pageid = id
    g.db = connect_db()
    cur = g.db.execute('select title, author from content')
    sql = "SELECT * FROM content WHERE id = $id"
    sales = [dict(title=row[0], author=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template("blog_post.html", sales=sales)


@app.route('/about')
def about_me():

    return render_template("about.html")


if __name__ == '__main__':
    app.run()
