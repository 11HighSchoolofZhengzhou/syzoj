from syzoj import db
from random import randint
import time


class Session(db.Model):
    id = db.Column(db.String(120), primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("sessions", lazy='dynamic'))

    login_time = db.Column(db.Integer)  # googbye at 2038-1-19
    expiration_time = db.Column(db.Integer)

    def __init__(self, user, login_time=int(time.time()), valid_time=3600 * 24 * 7):
        self.id = str(randint(1, int(1e50)))
        self.user = user
        self.login_time = login_time
        self.expiration_time = login_time + valid_time

    def __repr__(self):
        print "<Session_id %r User_id %r" % (self.id, self.user_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def is_valid(self, now=int(time.time())):
        # print "now:%r expiration_tim:%r" % (now,self.expiration_time)
        if now < self.expiration_time:
            return True
        else:
            self.delete()
            return False


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))

    nickname = db.Column(db.String(80))
    nameplate = db.Column(db.Text)
    information = db.Column(db.Text)

    is_admin = db.Column(db.Boolean)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

        self.nickname = username
        self.is_admin = False

    def __repr__(self):
        return "<User:%r password:%r email:%r>" % (self.username, self.password, self.email)

    def save(self):
        db.session.add(self)
        db.session.commit()