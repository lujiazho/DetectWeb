"""
https://devdocs.io/
https://codepen.io/
https://getbootstrap.com/
https://www.codeply.com/go
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager
from flask_mail import Mail

from detectweb.config import Config

db = SQLAlchemy()
migrate = Migrate()
# session管理
login_manager = LoginManager()
# 这条一加，访问index时就会自动跳转（重定向）到所赋值的那个函数去，即login
# 不过从index重定向到login会有额外参数“next=%2Findex”，这个%2F就代表了/index这个页面
login_manager.login_view = 'login'
# 邮件对象
mail = Mail()

from detectweb.route import index, login, logout, register, user, page_not_found, \
    edit_profile, reset_password_request, password_reset, explore, user_activate, \
    predict, feedback, dashboard, feedback_history, predict_history, predictbykind, \
    visitor, predict_for_visitor, intro, article


def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(Config)
    db.init_app(app) # sqlite数据库
    migrate.init_app(app, db) # 数据库迭代
    login_manager.init_app(app) # session管理
    mail.init_app(app) # 初始化邮件服务
    # 似乎这一行的第三个参数的index加不加都行
    app.add_url_rule('/index', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
    app.add_url_rule('/visitor', 'visitor', visitor, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
    app.add_url_rule('/predict', 'predict', predict, methods=['GET', 'POST'])
    app.add_url_rule('/predictbykind', 'predictbykind', predictbykind, methods=['POST'])
    app.add_url_rule('/predict_for_visitor', 'predict_for_visitor', predict_for_visitor, methods=['GET', 'POST'])
    app.add_url_rule('/feedback', 'feedback', feedback, methods=['GET', 'POST'])
    app.add_url_rule('/dashboard', 'dashboard', dashboard, methods=['GET'])
    app.add_url_rule('/feedback_history', 'feedback_history', feedback_history, methods=['GET', 'POST'])
    app.add_url_rule('/predict_history', 'predict_history', predict_history, methods=['GET', 'POST'])
    # 第二个参数就是别名，比如这里的username，就可以url_for里填写profile
    # 如果写url_for(user)，就没法传username参数，也不知道该到那个user界面（其link为用户名）
    app.add_url_rule('/<username>', 'profile', user, methods=['GET', 'POST'])
    app.add_url_rule('/edit_profile', 'edit_profile', edit_profile, methods=['GET', 'POST'])
    app.add_url_rule(
        '/reset_password_request',
        'reset_password_request',
        reset_password_request,
        methods=['GET', 'POST']
    )
    app.add_url_rule(
        '/password_reset/<token>',
        'password_reset',
        password_reset,
        methods=['GET', 'POST']
    )
    app.register_error_handler(404, page_not_found) # 加上这个，abort404的时候就会找这个函数
    app.add_url_rule('/explore', 'explore', explore)
    app.add_url_rule('/activate/<token>', 'user_activate', user_activate)
    app.add_url_rule('/intro', 'intro', intro, methods=['GET'])
    app.add_url_rule('/article', 'article', article, methods=['GET'])
    return app
