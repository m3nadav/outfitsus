from flask import Flask, redirect, url_for, session, request, render_template, mysql
from flask_oauth import OAuth
import json


SECRET_KEY = 'Nadav Mermer'
DEBUG = True
FACEBOOK_APP_ID = '324858954337623'
FACEBOOK_APP_SECRET = 'de6cd1c9f02cf369745b284eed772852'


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()
# init db connection
mysql = mysql.MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
cursor = mysql.connect().cursor()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email,user_birthday,user_education_history,user_photos,publish_actions'}
)


@app.route('/')
def index():
    #if not get_facebook_oauth_token():
        return redirect(url_for('login'))
    #return redirect(url_for('home'))

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    #f = open('/tmp/my_data','w')
    session['fid'] = me.data['id']
    #f.write(json.dumps(session['me']))
    #f.close()
    birthday = me.data['birthday'][3:5]+'-'+me.data['birthday'][0:2]+'-'+me.data['birthday'][6:]


    #insert_user = "INSERT INTO logged_user (ufid,name,birthday,email,locale,gender,updated_time,link) VALUES ("+me.data['if']+",'"+me.data['name']+"','"+me.data['birthday']+"','"+me.data['email']+"','"+me.data['locale']+"','"+me.data['gender']+"','"+me.data['updated_time']+"','"+me.data['link']+"');"

    #cursor.execute(insert_user);

    return redirect(url_for('home'))
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

@app.route('/home')
def home():
    if not session.has_key('oauth_token') or session['oauth_token'] == None:
        return redirect(url_for('index'))
    return render_template('fb.html', user_object=get_facebook_oauth_token())

if __name__ == '__main__':
    app.run()
