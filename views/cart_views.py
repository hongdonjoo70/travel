from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.tour import TourProduct
from models.cart import Cart, CartItem
from forms.cart_forms import AddToCartForm, UpdateCartForm

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('')
@login_required
def view_cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()

    update_form = UpdateCartForm()
    return render_template('cart/index.html', cart=cart, update_form=update_form)

@cart_bp.route('/add', methods=['POST'])
@login_required
def add_to_cart():
    form = AddToCartForm()
    if form.validate_on_submit():
        product_id = int(form.product_id.data)
        quantity = form.quantity.data
        product = TourProduct.query.get_or_404(product_id)

        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()

        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=quantity)
            db.session.add(cart_item)

        db.session.commit()
        flash(f"'{product.name}' 상품이 장바구니에 담겼습니다. (회원 혜택가 적용)", 'success')
        return redirect(url_for('cart.view_cart'))

    flash('장바구니 담기에 실패했습니다.', 'danger')
    return redirect(request.referrer or url_for('product.list_products'))

@cart_bp.route('/update', methods=['POST'])
@login_required
def update_quantity():
    form = UpdateCartForm()
    if form.validate_on_submit():
        cart_item_id = int(form.cart_item_id.data)
        quantity = form.quantity.data

        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            item = CartItem.query.filter_by(id=cart_item_id, cart_id=cart.id).first()
            if item:
                item.quantity = quantity
                db.session.commit()
                flash('상품 수량이 변경되었습니다.', 'info')
                return redirect(url_for('cart.view_cart'))

    flash('수량 변경에 실패했습니다.', 'danger')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_item(item_id):
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart:
        item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
        if item:
            name = item.product.name
            db.session.delete(item)
            db.session.commit()
            flash(f"'{name}' 상품이 장바구니에서 삭제되었습니다.", 'secondary')

    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/clear', methods=['POST'])
@login_required
def clear_cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart:
        cart.clear()
        db.session.commit()
        flash('장바구니를 모두 비웠습니다.', 'secondary')
    return redirect(url_for('cart.view_cart'))

