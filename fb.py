from flask import Flask, redirect, url_for, session, request, render_template, mysql
from sqlalchemy import MetaData, Column, Integer, String, create_engine
from sqlalchemy.orm import mapper, create_session
from flask_oauth import OAuth
import facebook as fb
import json

"""
Thats how you post a link on user's wall!
post_id = graph.put_wall_post("Yep :)",{"name":"Test Link", "link":"http://fb.mermers.net/fb","caption":"Test Caption","description":"Test Description","picture":"http://images.nationalgeographic.com/wpf/media-live/photos/000/687/cache/bonobo-congo-ziegler_68751_990x742.jpg",'privacy':{'value':'SELF'}})['id']
"""

SECRET_KEY = 'Nadav Mermer'
DEBUG = True
FACEBOOK_APP_ID = '324858954337623'
FACEBOOK_APP_SECRET = 'de6cd1c9f02cf369745b284eed772852'
OUTFITSUS_ALBUM_NAME = 'outfitsus'

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
class Post(object):
    pass
usermapper = mapper(User, meta.tables['fb_logged_users'])
postmapper = mapper(Post, meta.tables['fb_users_posts'])

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email,user_birthday,user_photos,publish_actions,user_friends,user_relationships,user_status,read_stream'}
)


@app.route('/')
def index():
    if not get_facebook_oauth_token():
        return redirect(url_for('login'))
    return redirect(url_for('init'))

@app.route('/logout')
def logout():
    session['oauth_token'] = None
    return redirect(url_for('index'))

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
    return redirect(url_for('init'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

@app.route('/init')
def init():
    if not session.has_key('oauth_token') or session['oauth_token'] == None:
        return redirect(url_for('index'))
    sess = create_session()
    graph = fb.GraphAPI(session['oauth_token'][0])
    #get current user's object
    user = graph.get_object("me")
    #preparing "logged_user" <User> object for logging user into the DB
    user["ufid"] = user["id"] #in the db we have ufid column instead of just id
    user["oauth_token"] = session['oauth_token'][0] #i wanna keep the oauth for future use
    split_birthday = user["birthday"].split('/')
    user["birthday"] = split_birthday[2]+"-"+split_birthday[0]+"-"+split_birthday[1] # changing birthday date format
    logged_user = sess.query(User).get(user["ufid"]) #querying for existing user row in db
    if not logged_user:
        logged_user = User() #if user doesnt exist in db create a new object
    for key in user.keys():
        logged_user.__setattr__(key,user[key]) #dump all "user" graphAPI response into User object

    #adding the app album_id to the User object (logged_user) for future photo uploading
    albums = graph.get_object('/me/albums')
    logged_user.album_id = None
    for album in albums['data']:
        if album['name'] == OUTFITSUS_ALBUM_NAME:
            logged_user.album_id = album['id']
            user["album"] = album
    if logged_user.album_id == None:
        logged_user.album_id = graph.put_object('/me','albums',name=OUTFITSUS_ALBUM_NAME,privacy="{'value':'SELF'}")['id']
    #saving user's details to the db
    sess.add(logged_user)
    sess.flush()

    #searching for other friends signed to this app
    friends = graph.get_connections(user["id"], "friends")
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if not get_facebook_oauth_token():
        return redirect(url_for('index'))

    return render_template('fb.html', post_action=url_for('post'), logout_action=url_for('logout'))

@app.route('/home/post', methods=['GET', 'POST'])
def post():
    def wall_post(token, form):
        if not token:
            return False
        graph = fb.GraphAPI(token)
        #privacy = {'privacy':{'value':'self'}} if form['privacy'] == 'self' else None'
        if form.has_key('link'):
            attachment = {'name':form['name'],'link':form['link'],'caption':form['caption'],'description':form['description'],'picture':form['picture'],'privacy':{'value':'self'}}
            return graph.put_wall_post(form['message'], attachment)['id']
        else:
            return graph.put_wall_post(form['message'],{'privacy':{'value':'SELF'}})['id']
    post_id = False
    if not get_facebook_oauth_token():
        return redirect(url_for('index'))
    if request.method == 'POST':
        if request.form.has_key('wall_post'):
            post_id = wall_post(get_facebook_oauth_token()[0], request.form)
    if post_id:
        sess = create_session()
        post = Post()
        post.ufid = session['fid']
        post.post_id = post_id
        post.type = 'wall post'
        sess.add(post)
        sess.flush()
    return render_template('wall_post.html', post=post)


if __name__ == '__main__':
    app.run()
