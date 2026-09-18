from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.tour import TourProduct, Theme, RegionEnum, ProductLike, Accommodation
from forms.cart_forms import AddToCartForm

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('')
def list_products():
    region = request.args.get('region')
    theme_id = request.args.get('theme_id', type=int)
    sort_by = request.args.get('sort', 'popular') # popular, latest, price_asc, price_desc

    query = TourProduct.query
    if region and region in RegionEnum.get_display_names():
        query = query.filter_by(region=region)
    if theme_id:
        query = query.filter_by(theme_id=theme_id)

    if sort_by == 'popular':
        query = query.order_by(TourProduct.recommendation_count.desc())
    elif sort_by == 'latest':
        query = query.order_by(TourProduct.created_at.desc())
    elif sort_by == 'price_asc':
        query = query.order_by(TourProduct.original_price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(TourProduct.original_price.desc())

    products = query.all()
    themes = Theme.query.filter_by(is_active=True).all()
    regions = RegionEnum.get_display_names()

    return render_template(
        'product/list.html',
        products=products,
        themes=themes,
        regions=regions,
        selected_region=region,
        selected_theme_id=theme_id,
        sort_by=sort_by
    )

@product_bp.route('/<int:product_id>')
def detail(product_id):
    product = TourProduct.query.get_or_404(product_id)
    cart_form = AddToCartForm(product_id=product.id)
    is_liked = product.is_liked_by(current_user)
    reviews = product.reviews.order_by(db.desc('created_at')).all()

    # 같은 지역의 다른 추천 상품
    related_products = TourProduct.query.filter(
        TourProduct.region == product.region,
        TourProduct.id != product.id
    ).limit(3).all()

    # 회원 전용 연계 추천 숙박 시설 ([민박] 및 [호텔])
    recommended_minbaks = Accommodation.query.filter_by(
        region=product.region, acc_type='민박', is_recommended=True
    ).limit(4).all()

    recommended_hotels = Accommodation.query.filter_by(
        region=product.region, acc_type='호텔', is_recommended=True
    ).limit(4).all()

    return render_template(
        'product/detail.html',
        product=product,
        cart_form=cart_form,
        is_liked=is_liked,
        reviews=reviews,
        related_products=related_products,
        recommended_minbaks=recommended_minbaks,
        recommended_hotels=recommended_hotels
    )

@product_bp.route('/popular')
def popular():
    """추천 수가 높은 관광 상품 랭킹 화면"""
    region = request.args.get('region')
    theme_id = request.args.get('theme_id', type=int)

    query = TourProduct.query
    if region and region in RegionEnum.get_display_names():
        query = query.filter_by(region=region)
    if theme_id:
        query = query.filter_by(theme_id=theme_id)

    # 추천수 내림차순 정렬
    top_products = query.order_by(TourProduct.recommendation_count.desc()).all()
    themes = Theme.query.filter_by(is_active=True).all()
    regions = RegionEnum.get_display_names()

    return render_template(
        'product/popular.html',
        products=top_products,
        themes=themes,
        regions=regions,
        selected_region=region,
        selected_theme_id=theme_id
    )

@product_bp.route('/<int:product_id>/like', methods=['POST'])
@login_required
def toggle_like(product_id):
    """관광 상품 추천(좋아요) 토글"""
    product = TourProduct.query.get_or_404(product_id)
    existing_like = ProductLike.query.filter_by(
        user_id=current_user.id,
        product_id=product.id
    ).first()

    if existing_like:
        db.session.delete(existing_like)
        product.recommendation_count = max(0, product.recommendation_count - 1)
        liked = False
        msg = '추천을 취소하였습니다.'
    else:
        new_like = ProductLike(user_id=current_user.id, product_id=product.id)
        db.session.add(new_like)
        product.recommendation_count += 1
        liked = True
        msg = '상품을 추천하였습니다!'

    db.session.commit()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        return jsonify({
            'success': True,
            'liked': liked,
            'count': product.recommendation_count,
            'message': msg
        })

    flash(msg, 'info')
    return redirect(request.referrer or url_for('product.detail', product_id=product.id))

