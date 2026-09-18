from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from models.user import User

class SignupForm(FlaskForm):
    username = StringField('아이디', validators=[
        DataRequired(message='아이디를 입력해주세요.'),
        Length(min=4, max=20, message='아이디는 4자 이상 20자 이하로 입력해주세요.')
    ])
    password = PasswordField('비밀번호', validators=[
        DataRequired(message='비밀번호를 입력해주세요.'),
        Length(min=6, max=30, message='비밀번호는 6자 이상 30자 이하로 입력해주세요.')
    ])
    confirm_password = PasswordField('비밀번호 확인', validators=[
        DataRequired(message='비밀번호 확인을 입력해주세요.'),
        EqualTo('password', message='비밀번호가 일치하지 않습니다.')
    ])
    name = StringField('이름', validators=[
        DataRequired(message='이름을 입력해주세요.'),
        Length(min=2, max=30, message='이름은 2자 이상 입력해주세요.')
    ])
    email = StringField('이메일', validators=[
        DataRequired(message='이메일을 입력해주세요.'),
        Email(message='올바른 이메일 형식을 입력해주세요.')
    ])
    phone = StringField('전화번호', validators=[
        DataRequired(message='전화번호를 입력해주세요.'),
        Regexp(r'^[0-9\-+]{9,20}$', message='올바른 전화번호 형식(예: 010-1234-5678)을 입력해주세요.')
    ])
    submit = SubmitField('회원가입')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('이미 사용 중인 아이디입니다.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('이미 등록된 이메일 주소입니다.')

class LoginForm(FlaskForm):
    username = StringField('아이디', validators=[
        DataRequired(message='아이디를 입력해주세요.')
    ])
    password = PasswordField('비밀번호', validators=[
        DataRequired(message='비밀번호를 입력해주세요.')
    ])
    remember_me = BooleanField('로그인 상태 유지')
    submit = SubmitField('로그인')

