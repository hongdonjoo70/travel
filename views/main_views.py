from flask import Blueprint, render_template, request
from models.tour import TourProduct, Theme, RegionEnum

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    selected_region = request.args.get('region')
    selected_theme = request.args.get('theme')

    query = TourProduct.query
    if selected_region and selected_region in RegionEnum.get_display_names():
        query = query.filter_by(region=selected_region)
    if selected_theme:
        query = query.join(Theme).filter(Theme.code == selected_theme)

    products = query.order_by(TourProduct.recommendation_count.desc()).all()
    themes = Theme.query.filter_by(is_active=True).all()
    regions = RegionEnum.get_display_names()

    # Top 3 베스트 추천 상품
    top_picks = TourProduct.query.order_by(TourProduct.recommendation_count.desc()).limit(3).all()

    return render_template(
        'index.html',
        products=products,
        themes=themes,
        regions=regions,
        selected_region=selected_region,
        selected_theme=selected_theme,
        top_picks=top_picks
    )

