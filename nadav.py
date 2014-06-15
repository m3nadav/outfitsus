from flask import Flask, request, render_template, redirect, url_for, abort, session, escape, mysql
app = Flask(__name__)
app.debug = True
app.secret_key = 'asd'
mysql = mysql.MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
links = []
global common
common = {}

@app.route('/')
def index():
    return render_template('site_map.html', common = common)

@app.route('/user')
@app.route('/user/<user>')
def hello_user(user=None):
    return render_template('login.html', title='hey user!', name=user)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        common['username'] = session['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>'''

@app.route('/logoff')
def logout():
    session.pop('username', None)
    common.pop('username', None)
    return redirect(url_for('index'))

@app.route('/forbidden')
def forbid():
    abort(403)
    print "HELLO"

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html', error=error), 404

@app.route('/mysql')
@app.route('/mysql/<page_title>')
def page_stats(page_title=None):
    cursor = mysql.connect().cursor()
    if page_title:
        query = "select page_title, sum(edit) edit, sum(view) view from log where page_title='%s'" % page_title
    else:
        query = "select page_title, sum(edit) edit, sum(view) view from log group by page_title"
    cursor.execute(query)
    return render_template('statistics.html', results=cursor.fetchall())

@app.route('/check')
def check():
    return render_template('main.html', common = common)

#collect some data about the site_map
for rule in app.url_map.iter_rules():
    if "GET" in rule.methods and not '<' in rule.rule:
        links.append((rule.rule,rule.endpoint))
common['links'] = links

if __name__ == "__main__":
    app.run(host="192.168.1.78", port=8888)
