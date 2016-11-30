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
    cur = g.db.execute('SELECT title, author, id, content, image FROM content LIMIT 6')
    sales = [dict(title=row[0], author=row[1], id=row[2], content=row[3], image=row[4]) for row in cur.fetchall()]
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
    cur = g.db.execute('SELECT title, author, id, content FROM content')
    sales = [dict(title=row[0], author=row[1], id=row[2], content=row[3]) for row in cur.fetchall()]
    g.db.close()
    return render_template('admin/admin.html', sales=sales)


@app.route('/admin-posts')
@requires_auth
def posts():
    g.db = connect_db()
    cur = g.db.execute('SELECT title, author, id, content FROM content')
    sales = [dict(title=row[0], author=row[1], id=row[2], content=row[3]) for row in cur.fetchall()]
    g.db.close()
    return render_template('admin/admin_blog_posts.html', sales=sales)


@app.route('/my-details')
@requires_auth
def my_details():
    g.db = connect_db()
    cur = g.db.execute('SELECT id, first_name, second_name, email, dob, img FROM users')
    users = [dict(id=row[0], first_name=row[1], second_name=row[2], email=row[3], dob=row[4], img=row[5]) for row in
             cur.fetchall()]
    g.db.close()
    return render_template('admin/my_details.html', users=users)


@app.route('/blog/<id>')
def blog(id=id):
    g.db = connect_db()
    cur = g.db.execute('SELECT title, author, id, image, content, date FROM content WHERE id=?', [id])
    sales = [dict(title=row[0], author=row[1], id=row[2], image=row[3], content=row[4], date=row[5]) for row in
             cur.fetchall()]
    g.db.close()
    return render_template("blog_post.html", sales=sales)


@app.route('/edit/<id>')
@requires_auth
def editblog(id=id):
    g.db = connect_db()
    cur = g.db.execute('SELECT title, author, id, image, content, date FROM content WHERE id=?', [id])
    sales = [dict(title=row[0], author=row[1], id=row[2], image=row[3], content=row[4], date=row[5]) for row in
             cur.fetchall()]
    g.db.close()
    return render_template("admin/edit_blog_post.html", sales=sales)


@app.route('/delete-blog/<id>')
def deleteblog(id=id):
    g.db = connect_db()
    g.db.execute('DELETE FROM content WHERE id=?', [id])
    g.db.close()
    redirect(url_for('secret_page'))


@app.route('/about')
def about_me():
    return render_template("about.html")


@app.route('/blogs-all')
def allblogs():
    g.db = connect_db()
    cur = g.db.execute('SELECT title, author, id, content, image FROM content')
    sales = [dict(title=row[0], author=row[1], id=row[2], content=row[3], image=row[4]) for row in cur.fetchall()]
    g.db.close()
    return render_template("blogs_all.html", sales=sales)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run('0.0.0.0')
