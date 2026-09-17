from datetime import datetime, timezone
from extensions import db

class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    items = db.relationship('CartItem', backref='cart', lazy='dynamic', cascade='all, delete-orphan')

    def get_total_original_price(self):
        """장바구니 전체 상품 정가 합계"""
        return sum(item.product.original_price * item.quantity for item in self.items)

    def get_total_discount_amount(self, is_member=True):
        """회원 할인 적용 총 할인액"""
        if not is_member:
            return 0
        return sum(item.product.get_discount_amount(True) * item.quantity for item in self.items)

    def get_total_final_price(self, is_member=True):
        """최종 결제 예상 금액"""
        return sum(item.product.get_discounted_price(is_member) * item.quantity for item in self.items)

    def get_total_count(self):
        """장바구니 총 품목(수량) 수"""
        return sum(item.quantity for item in self.items)

    def clear(self):
        """장바구니 비우기"""
        for item in self.items:
            db.session.delete(item)

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    __table_args__ = (
        db.UniqueConstraint('cart_id', 'product_id', name='uix_cart_product'),
    )

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('tour_products.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_subtotal_original(self):
        return self.product.original_price * self.quantity

    def get_subtotal_final(self, is_member=True):
        return self.product.get_discounted_price(is_member) * self.quantity

    def get_discount_amount(self, is_member=True):
        return self.product.get_discount_amount(is_member) * self.quantity
