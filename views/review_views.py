from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.tour import TourProduct
from models.review import Review
from forms.review_forms import ReviewForm

review_bp = Blueprint('review', __name__, url_prefix='/reviews')

@review_bp.route('/product/<int:product_id>/create', methods=['GET', 'POST'])
@login_required
def create_review(product_id):
    product = TourProduct.query.get_or_404(product_id)
    form = ReviewForm()

    if form.validate_on_submit():
        review = Review(
            user_id=current_user.id,
            product_id=product.id,
            title=form.title.data.strip(),
            content=form.content.data.strip(),
            rating=int(form.rating.data)
        )
        db.session.add(review)
        db.session.commit()
        flash('소중한 여행 후기가 등록되었습니다!', 'success')
        return redirect(url_for('product.detail', product_id=product.id))

    return render_template('review/create.html', form=form, product=product)

@review_bp.route('/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id and current_user.role != 'ADMIN':
        flash('본인이 작성한 후기만 삭제할 수 있습니다.', 'danger')
        return redirect(url_for('product.detail', product_id=review.product_id))

    product_id = review.product_id
    db.session.delete(review)
    db.session.commit()
    flash('후기가 삭제되었습니다.', 'info')
    return redirect(url_for('product.detail', product_id=product_id))

