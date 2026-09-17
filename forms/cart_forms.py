from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class AddToCartForm(FlaskForm):
    product_id = HiddenField('상품 ID', validators=[DataRequired()])
    quantity = IntegerField('수량', default=1, validators=[
        DataRequired(),
        NumberRange(min=1, max=99, message='수량은 1개 이상 99개 이하로 선택해주세요.')
    ])
    submit = SubmitField('장바구니 담기')

class UpdateCartForm(FlaskForm):
    cart_item_id = HiddenField('장바구니 품목 ID', validators=[DataRequired()])
    quantity = IntegerField('수량', validators=[
        DataRequired(),
        NumberRange(min=1, max=99, message='수량은 1개 이상 99개 이하로 변경해주세요.')
    ])
    submit = SubmitField('변경')

