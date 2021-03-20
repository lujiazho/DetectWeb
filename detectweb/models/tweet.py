from datetime import datetime

from detectweb import db


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(64))
    body = db.Column(db.String(140))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    # 这个user是小写，代表table的名字（默认情况下，table名字为小写的class）
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "id={}, img={}, body={}, create_time={}, user_id={}".format(
            self.id, self.img, self.body, self.create_time, self.user_id
        )
