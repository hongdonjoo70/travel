from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.user import User
from models.cart import Cart
from forms.auth_forms import SignupForm, LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            name=form.name.data.strip(),
            email=form.email.data.strip(),
            phone=form.phone.data.strip()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # 회원용 장바구니 자동 생성
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()

        flash(f'환영합니다, {user.name}님! 회원가입이 완료되었습니다. 로그인해주세요.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.strip()).first()
        if user and user.check_password(form.password.data):
            remember = form.remember_me.data if hasattr(form, 'remember_me') else False
            login_user(user, remember=remember)
            # 사용자의 카트가 없으면 생성 보장
            if not user.cart:
                cart = Cart(user_id=user.id)
                db.session.add(cart)
                db.session.commit()

            flash(f'{user.name}님, 환영합니다! 회원 특별 할인가가 적용됩니다.', 'info')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('아이디 또는 비밀번호가 일치하지 않습니다.', 'danger')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('성공적으로 로그아웃되었습니다.', 'secondary')
    return redirect(url_for('main.index'))

