import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.tour import TourProduct, Accommodation
from models.cart import Cart
from models.order import Order, OrderItem, Payment, OrderAccommodation

order_bp = Blueprint('order', __name__, url_prefix='/order')

@order_bp.route('/checkout')
def checkout():
    is_member = current_user.is_authenticated
    direct_product_id = request.args.get('product_id', type=int)
    quantity = request.args.get('quantity', 1, type=int)

    items_to_checkout = []
    total_original = 0
    total_final = 0

    if direct_product_id:
        product = TourProduct.query.get_or_404(direct_product_id)
        subtotal_orig = product.original_price * quantity
        subtotal_fin = product.get_discounted_price(is_member=is_member) * quantity
        items_to_checkout.append({
            'product': product,
            'quantity': quantity,
            'original_price': product.original_price,
            'final_price': product.get_discounted_price(is_member=is_member),
            'subtotal_original': subtotal_orig,
            'subtotal_final': subtotal_fin
        })
        total_original = subtotal_orig
        total_final = subtotal_fin
    else:
        if not is_member:
            flash('비회원 구매는 상품 상세 페이지에서 바로 구매를 이용해주세요.', 'info')
            return redirect(url_for('product.list_products'))

        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart or cart.items.count() == 0:
            flash('결제할 장바구니 상품이 없습니다.', 'warning')
            return redirect(url_for('cart.view_cart'))

        for item in cart.items:
            subtotal_orig = item.get_subtotal_original()
            subtotal_fin = item.get_subtotal_final(is_member=True)
            items_to_checkout.append({
                'product': item.product,
                'quantity': item.quantity,
                'original_price': item.product.original_price,
                'final_price': item.product.get_discounted_price(is_member=True),
                'subtotal_original': subtotal_orig,
                'subtotal_final': subtotal_fin
            })
            total_original += subtotal_orig
            total_final += subtotal_fin

    # 회원 전용 연계 숙박 예약 항목 조회 (acc_ids)
    acc_ids_str = request.args.get('acc_ids', '').strip()
    selected_accommodations = []
    acc_original_total = 0
    acc_final_total = 0

    if is_member and acc_ids_str:
        acc_ids = [int(x.strip()) for x in acc_ids_str.split(',') if x.strip().isdigit()]
        if acc_ids:
            accommodations = Accommodation.query.filter(Accommodation.id.in_(acc_ids)).all()
            for acc in accommodations:
                orig_p = acc.price_per_night
                fin_p = acc.get_discounted_price(is_member=True)
                disc_p = acc.get_discount_amount(is_member=True)
                acc_original_total += orig_p
                acc_final_total += fin_p
                selected_accommodations.append({
                    'accommodation': acc,
                    'nights': 1,
                    'original_price': orig_p,
                    'final_price': fin_p,
                    'discount_amount': disc_p
                })

    total_original += acc_original_total
    total_final += acc_final_total
    total_discount = total_original - total_final

    return render_template(
        'order/checkout.html',
        items=items_to_checkout,
        selected_accommodations=selected_accommodations,
        acc_ids=acc_ids_str,
        total_original=total_original,
        total_discount=total_discount,
        total_final=total_final,
        direct_product_id=direct_product_id,
        quantity=quantity,
        is_member=is_member
    )

@order_bp.route('/pay', methods=['POST'])
def process_payment():
    is_member = current_user.is_authenticated
    direct_product_id = request.form.get('direct_product_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    payment_method = request.form.get('payment_method', 'CARD')

    total_orig = 0
    total_fin = 0
    order_items_data = []

    guest_name = None
    guest_email = None
    guest_phone = None
    user_id = None

    if not is_member:
        guest_name = request.form.get('guest_name', '').strip() or '비회원 고객'
        guest_email = request.form.get('guest_email', '').strip()
        guest_phone = request.form.get('guest_phone', '').strip()
    else:
        user_id = current_user.id

    if direct_product_id:
        product = TourProduct.query.get_or_404(direct_product_id)
        unit_price = product.get_discounted_price(is_member=is_member)
        discount = product.get_discount_amount(is_member=is_member)
        subtotal = unit_price * quantity
        total_orig = product.original_price * quantity
        total_fin = subtotal

        order_items_data.append({
            'product_id': product.id,
            'quantity': quantity,
            'unit_price': unit_price,
            'discount_applied': discount,
            'subtotal_price': subtotal
        })
    else:
        if not is_member:
            flash('비회원은 바로 구매만 가능합니다.', 'danger')
            return redirect(url_for('product.list_products'))

        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart or cart.items.count() == 0:
            flash('결제할 상품이 없습니다.', 'danger')
            return redirect(url_for('cart.view_cart'))

        for item in cart.items:
            unit_price = item.product.get_discounted_price(is_member=True)
            discount = item.product.get_discount_amount(is_member=True)
            subtotal = unit_price * item.quantity
            total_orig += item.product.original_price * item.quantity
            total_fin += subtotal

            order_items_data.append({
                'product_id': item.product.id,
                'quantity': item.quantity,
                'unit_price': unit_price,
                'discount_applied': discount,
                'subtotal_price': subtotal
            })

    # 회원 연계 숙박 결제 처리
    acc_ids_str = request.form.get('acc_ids', '').strip()
    order_accommodations_data = []

    if is_member and acc_ids_str:
        acc_ids = [int(x.strip()) for x in acc_ids_str.split(',') if x.strip().isdigit()]
        if acc_ids:
            accommodations = Accommodation.query.filter(Accommodation.id.in_(acc_ids)).all()
            for acc in accommodations:
                orig_p = acc.price_per_night
                fin_p = acc.get_discounted_price(is_member=True)
                disc_p = acc.get_discount_amount(is_member=True)
                total_orig += orig_p
                total_fin += fin_p
                order_accommodations_data.append({
                    'accommodation_id': acc.id,
                    'nights': 1,
                    'unit_price': fin_p,
                    'discount_applied': disc_p,
                    'subtotal_price': fin_p
                })

    total_discount = total_orig - total_fin

    # 주문 객체 생성 (회원/비회원 공통)
    order = Order(
        order_no=Order.generate_order_no(),
        user_id=user_id,
        guest_name=guest_name,
        guest_email=guest_email,
        guest_phone=guest_phone,
        original_amount=total_orig,
        discount_amount=total_discount,
        final_amount=total_fin,
        status='COMPLETED'
    )
    db.session.add(order)
    db.session.flush() # order.id 확보

    # 주문 상세 항목 생성
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data['product_id'],
            quantity=item_data['quantity'],
            unit_price=item_data['unit_price'],
            discount_applied=item_data['discount_applied'],
            subtotal_price=item_data['subtotal_price']
        )
        db.session.add(order_item)

    # 연계 숙박 예약 항목 생성
    for acc_data in order_accommodations_data:
        order_acc = OrderAccommodation(
            order_id=order.id,
            accommodation_id=acc_data['accommodation_id'],
            nights=acc_data['nights'],
            unit_price=acc_data['unit_price'],
            discount_applied=acc_data['discount_applied'],
            subtotal_price=acc_data['subtotal_price']
        )
        db.session.add(order_acc)

    # 모의 결제 트랜잭션 기록
    payment = Payment(
        order_id=order.id,
        payment_method=payment_method,
        paid_amount=total_fin,
        transaction_id=f"TX-{uuid.uuid4().hex[:12].upper()}",
        status='SUCCESS'
    )
    db.session.add(payment)

    # 장바구니 결제인 경우 장바구니 비우기
    if is_member and not direct_product_id:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            cart.clear()

    db.session.commit()
    if is_member:
        flash('결제가 안전하게 완료되었습니다! 회원 우대 할인이 적용되었습니다.', 'success')
    else:
        flash('비회원 예약 및 결제가 안전하게 완료되었습니다! (정가 적용)', 'success')
    return redirect(url_for('order.complete', order_id=order.id))

@order_bp.route('/complete/<int:order_id>')
def complete(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order/complete.html', order=order)

@order_bp.route('/history')
@login_required
def history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('order/history.html', orders=orders)

