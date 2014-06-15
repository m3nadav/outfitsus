import json
from sqlalchemy import MetaData, Column, Integer, String, create_engine
from sqlalchemy.orm import mapper, create_session
#Initialize db connection as sqlalchemy engine
eng = create_engine("mysql://nadav:123456@localhost/outfitsus", encoding='utf-8', echo=False)
meta = MetaData(bind=eng)
meta.reflect()
self.userTable=meta.tables['fb_logged_users']

class User:
    pass

usermapper = mapper(User, userTable)

sess = create_session()
logged_user = sess.query(User).get(session['fid'])
if !logged_user:
    logged_user = User()


sess.add(logged_user)
sess.flush()
