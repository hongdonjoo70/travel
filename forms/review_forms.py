from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class ReviewForm(FlaskForm):
    rating = SelectField('평점', choices=[
        ('5', '★★★★★ (5점 - 아주 만족해요)'),
        ('4', '★★★★☆ (4점 - 만족해요)'),
        ('3', '★★★☆☆ (3점 - 보통이에요)'),
        ('2', '★★☆☆☆ (2점 - 아쉬워요)'),
        ('1', '★☆☆☆☆ (1점 - 실망이에요)')
    ], default='5', validators=[DataRequired()])
    title = StringField('후기 제목', validators=[
        DataRequired(message='제목을 입력해주세요.'),
        Length(min=2, max=100, message='제목은 2자 이상 100자 이하로 입력해주세요.')
    ])
    content = TextAreaField('후기 내용', validators=[
        DataRequired(message='후기 내용을 상세히 입력해주세요.'),
        Length(min=10, max=2000, message='후기 내용은 10자 이상 2000자 이하로 입력해주세요.')
    ])
    submit = SubmitField('후기 등록하기')

