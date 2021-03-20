import os

# 获取绝对路径
config_path = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 先找环境变量，若没有，则用默认的
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(config_path, 'detectweb.db'))
    # 取消一个警告（暂不知什么用）
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a9087FFJFF9nnvc2@#$%FSD')
    # 每页的tweet数
    TWEET_PER_PAGE = os.environ.get('TWEET_PER_PAGE', 5)
    # 每页predict数
    PREDICT_PER_PAGE = os.environ.get('PREDICT_PER_PAGE', 5)

    # 因为有了这个默认的sender，就不需要写sender了，这个参数必须要配置
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', '937371423@qq.com')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '937371423@qq.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'password')
    # 用于邮件subject
    MAIL_SUBJECT_RESET_PASSWORD = '[DetectWeb] Please Reset Your Password'
    # 用于邮件激活
    MAIN_SUBJECT_USER_ACTIVATE = '[DetectWeb] Please Activate Your Accout'
