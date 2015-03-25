from syzoj import db
from random import randint
import time


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("articles", lazy='dynamic'))

    public_time = db.Column(db.Integer)  # googbye at 2038-1-19
    update_time = db.Column(db.Integer)

    tag = db.Column(db.Text)

    comments_num = db.Column(db.Integer)
    allow_comment = db.Column(db.Boolean)

    def __init__(self, title, content, user, allow_comment=True, public_time=int(time.time())):
        self.title = title
        self.content = content
        self.user = user
        self.public_time = public_time
        self.update_time = public_time
        self.comments_num = 0
        self.allow_comment = allow_comment

    def __repr__(self):
        return "<Article %r>" % self.title

    def save(self):
        db.session.add(self)
        db.session.commit()


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

    article_id = db.Column(db.Integer, db.ForeignKey("article.id"))
    article = db.relationship("Article", backref=db.backref("comments", lazy='dynamic'))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("comments", lazy='dynamic'))

    public_time = db.Column(db.Integer)  # googbye at 2038-1-19

    def __init__(self, content, article, user, public_time=int(time.time())):
        self.content = content
        self.article = article
        self.user = user
        self.public_time = public_time

    def __repr__(self):
        return "<Comment %r>" % self.content

    def save(self):
        db.session.add(self)
        db.session.commit()