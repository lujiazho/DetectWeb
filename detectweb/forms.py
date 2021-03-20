from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, \
    Length

from detectweb.models.user import User


class LoginForm(FlaskForm):
    # 不知道为啥不设置为False就出问题
    class Meta:
        csrf = False
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("保持登陆状态")
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField("用户名", validators=[DataRequired()])
    email = StringField("邮箱", validators=[DataRequired(), Email()])
    password = PasswordField("密码", validators=[DataRequired()])
    password2 = PasswordField(
        "重复密码", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('please use different username')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('please use different email address')


class EditProfileForm(FlaskForm):
    about_me = TextAreaField('About me', validators=[Length(min=0, max=120)])
    submit = SubmitField('Save')


class TweetForm(FlaskForm):
    tweet = TextAreaField('Tweet', validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Tweet')

# 输入邮箱请求重置密码
class PasswdResetRequestForm(FlaskForm):
    email = StringField("电子邮箱", validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(
                'You do not have an account for this email address')

# 重置密码
class PasswdResetForm(FlaskForm):
    password = PasswordField("密码", validators=[DataRequired()])
    password2 = PasswordField(
        "重复密码", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')
