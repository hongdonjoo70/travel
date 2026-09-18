from datetime import datetime, timezone
import uuid
from extensions import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(64), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True) # 비회원 구매 시 None
    guest_name = db.Column(db.String(80), nullable=True)   # 비회원 구매자 이름
    guest_email = db.Column(db.String(120), nullable=True) # 비회원 이메일
    guest_phone = db.Column(db.String(30), nullable=True)  # 비회원 전화번호
    original_amount = db.Column(db.Integer, nullable=False)
    discount_amount = db.Column(db.Integer, default=0)
    final_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='COMPLETED') # PENDING, COMPLETED, CANCELLED
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    accommodations = db.relationship('OrderAccommodation', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='order', uselist=False, cascade='all, delete-orphan')

    @classmethod
    def generate_order_no(cls):
        now_str = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
        rand_str = uuid.uuid4().hex[:6].upper()
        return f"ORD-{now_str}-{rand_str}"

    @property
    def customer_name(self):
        return self.user.name if self.user else (self.guest_name or '비회원 고객')

    @property
    def customer_email(self):
        return self.user.email if self.user else (self.guest_email or '-')

    @property
    def customer_phone(self):
        return self.user.phone if self.user else (self.guest_phone or '-')

    def __repr__(self):
        return f"<Order {self.order_no} ({self.final_amount}원)>"

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('tour_products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.Integer, nullable=False) # 주문 시점 적용가
    discount_applied = db.Column(db.Integer, default=0) # 개당 할인액
    subtotal_price = db.Column(db.Integer, nullable=False)

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), unique=True, nullable=False)
    payment_method = db.Column(db.String(30), default='CARD') # CARD, BANK_TRANSFER, EASY_PAY
    paid_amount = db.Column(db.Integer, nullable=False)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(20), default='SUCCESS') # SUCCESS, FAILED, CANCELLED
    paid_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class OrderAccommodation(db.Model):
    """회원이 관광 상품과 함께 연계 예약한 숙박 시설 내역"""
    __tablename__ = 'order_accommodations'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    accommodation_id = db.Column(db.Integer, db.ForeignKey('accommodations.id'), nullable=False)
    nights = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.Integer, nullable=False) # 1박 회원 결제 금액
    discount_applied = db.Column(db.Integer, default=0) # 1박당 회원 할인액
    subtotal_price = db.Column(db.Integer, nullable=False) # 총 숙박 금액 (unit_price * nights)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    accommodation = db.relationship('Accommodation', backref='order_bookings')

    def __repr__(self):
        return f"<OrderAccommodation order_id={self.order_id} acc_id={self.accommodation_id} subtotal={self.subtotal_price}>"

