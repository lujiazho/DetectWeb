from datetime import datetime
from hashlib import md5
import time

from werkzeug.security import generate_password_hash, check_password_hash
# 提供关于用户session管理方法
from flask_login import UserMixin
from flask import current_app
import jwt

from detectweb import db, login_manager
from detectweb.models.tweet import Tweet
from detectweb.models.predict import Predict

# 没有建立类，因为这个表只描述关系，两个column都只存储了ForeignKey
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    country = db.Column(db.String(20))
    province = db.Column(db.String(20))
    city = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(120))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_activated = db.Column(db.Boolean, default=False)

    # 这不是一个column，和Tweet这个class建立关系，属于一对多，一个user多个tweets
    tweets = db.relationship('Tweet', backref='author', lazy='dynamic')
    predicts = db.relationship('Predict', backref='author', lazy='dynamic')

    # 这个关系创建后，单个user中的followed变量就代表了自己关注的人u1.followed.append(u3)就表示u1关注u3
    # followers就代表了关注自己的人
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id), # 通过这个找到自己关注了几个人
        secondaryjoin=(followers.c.followed_id == id), # 被多少人关注
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return 'id={}, username={}, email={}, password_hash={}'.format(
            self.id, self.username, self.email, self.password_hash
        )
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 动态生成头像
    def avatar(self, size=80):
        md5_digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://cdn.v2ex.com/gravatar/{}?d=identicon&s={}'.format(
            md5_digest, size)

    # 关注
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    # 取关
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # 返回user是否是自己正关注的人
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    # 自己的以及关注的人的tweet
    def own_and_followed_tweets(self):
        # 把tweet和followers两张表join在一起，条件是join的第二个参数，合起来就是[谁，关注了谁，被关注人的tweet，...]
        # 然后进行filter，我只关心我关注的，即follower_id是我的id
        followed = Tweet.query.join(
            followers, (followers.c.followed_id == Tweet.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Tweet.query.filter_by(user_id=self.id)
        # 然后把这两个表union起来，按时间降排序（最新的在前面）
        return followed.union(own).order_by(Tweet.create_time.desc())

    # jwt为java web token
    def get_jwt(self, expire=7200):
        return jwt.encode(
            {
                'email': self.email, # 键值对，email
                'exp': time.time() + expire # 键值对，expire时间，7200秒代表两个小时，不过verify时并没有检查是否过期
            },
            current_app.config['SECRET_KEY'], # secret码
            algorithm='HS256' # 算法
        ).decode('utf-8') # 如果不加decode就是个binary string

    """
    想直接通过User class来使用，而不是先实例化一个
    """
    @staticmethod
    def verify_jwt(token):
        # 用户点击链接后，服务端验证token是否合法
        try:
            email = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            email = email['email']
        except:
            return
        # 返回合法的用户
        return User.query.filter_by(email=email).first()

# 根据文档提供的方法，为了session管理
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

"""
国内Gravatar镜像源收集
gravatar官方的www https://www.gravatar.com/avatar/
gravatar官方的cn https://cn.gravatar.com/avatar/
gravatar官方的en https://en.gravatar.com/avatar/
gravatar官方的secure https://secure.gravatar.com/avatar/
V2EX https://cdn.v2ex.com/gravatar/
Loli https://gravatar.loli.net/avatar/
极客族 https://sdn.geekzu.org/avatar/
Zeruns's Blog：https://gravatar.zeruns.tech/avatar/
宝硕博客：https://gravatar.baoshuo.ren/avatar
左岸博客源：https://avatar.zrahh.com/avatar
"""