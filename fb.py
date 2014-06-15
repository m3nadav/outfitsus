from flask import Flask, redirect, url_for, session, request, render_template, mysql
from sqlalchemy import MetaData, Column, Integer, String, create_engine
from sqlalchemy.orm import mapper, create_session
from flask_oauth import OAuth
import facebook as fb
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
eng = create_engine("mysql://nadav:123456@localhost/outfitsus", encoding='utf-8', echo=False)
meta = MetaData(bind=eng)
meta.reflect()
class User(object):
    pass
usermapper = mapper(User, meta.tables['fb_logged_users'])
sess = create_session()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email,user_birthday,user_education_history,user_photos,publish_actions,user_videos,user_hometown,user_work_history,user_friends,user_relationships,user_status,user_website'}
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
    graph = fb.GraphAPI(session['oauth_token'][0])
    #get current user's object
    user = graph.get_object("me")
    #preparing to log user in DB
    user["ufid"] = user["id"]
    user["oauth_token"] = session['oauth_token'][0]
    #user["birthday"] =
    logged_user = sess.query(User).get(user["id"])
    is_user_exists = True
    if not logged_user:
        logged_user = User()
    logged_user.__dict__.update(user)
    #logging the user in DB
    sess.add(logged_user)
    sess.flush()

    #searching for other friends signed to this app
    friends = graph.get_connections(user["id"], "friends")
    return render_template('fb.html', user_object=json.dumps(user), friends=json.dumps(friends))

if __name__ == '__main__':
    app.run()
