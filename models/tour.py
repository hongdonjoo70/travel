from datetime import datetime, timezone
import enum
from extensions import db

class RegionEnum(str, enum.Enum):
    SEOUL_GYEONGGI = "서울/경기"
    JEONLA = "전라"
    CHUNGCHEONG = "충청"
    GANGWON = "강원"
    GYEONGBUK = "경북"
    JEJU = "제주"

    @classmethod
    def get_display_names(cls):
        return [r.value for r in cls]

class Theme(db.Model):
    __tablename__ = 'themes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False) # e.g. RESORT, EXPERIENCE
    name = db.Column(db.String(50), unique=True, nullable=False) # '휴양지', '체험'
    description = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    products = db.relationship('TourProduct', backref='theme', lazy='dynamic')

    def __repr__(self):
        return f"<Theme {self.name}>"

class TourProduct(db.Model):
    __tablename__ = 'tour_products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    region = db.Column(db.String(50), nullable=False, index=True) # 6개 지역
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'), nullable=False)
    original_price = db.Column(db.Integer, nullable=False)
    member_discount_rate = db.Column(db.Float, default=0.15) # 회원 15% 기본 할인
    recommendation_count = db.Column(db.Integer, default=0, index=True) # 누적 추천수
    image_url = db.Column(db.String(255), default='/static/img/default-tour.jpg')
    image_urls = db.Column(db.Text, nullable=True) # JSON 문자열 형태의 3~4개 이상 이미지 URL 목록
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    reviews = db.relationship('Review', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    likes = db.relationship('ProductLike', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    cart_items = db.relationship('CartItem', backref='product', lazy='dynamic')

    def get_discounted_price(self, is_member=False):
        """회원인 경우 할인율이 적용된 가격을 반환, 비회원은 정가 반환"""
        if is_member:
            return int(self.original_price * (1 - self.member_discount_rate))
        return self.original_price

    def get_discount_amount(self, is_member=False):
        """회원 할인 금액 반환"""
        if is_member:
            return self.original_price - self.get_discounted_price(True)
        return 0

    def get_average_rating(self):
        """상품 평점 평균 계산"""
        review_list = self.reviews.all()
        if not review_list:
            return 0.0
        return round(sum(r.rating for r in review_list) / len(review_list), 1)

    def is_liked_by(self, user):
        """특정 사용자가 이미 추천했는지 여부"""
        if not user or not user.is_authenticated:
            return False
        return self.likes.filter_by(user_id=user.id).first() is not None

    def get_image_list(self):
        """관광 상품의 다중 이미지 URL 목록 반환 (없을 경우 기본 image_url 또는 기본 이미지 반환)"""
        if self.image_urls:
            try:
                import json
                urls = json.loads(self.image_urls)
                if isinstance(urls, list) and len(urls) > 0:
                    return urls
            except Exception:
                urls = [u.strip() for u in self.image_urls.splitlines() if u.strip()]
                if urls:
                    return urls
        if self.image_url:
            return [self.image_url]
        return ['/static/img/default-tour.jpg']

    def set_image_list(self, urls):
        """이미지 URL 목록을 JSON으로 직렬화하여 저장하고 대표 이미지 동기화"""
        import json
        if isinstance(urls, list):
            self.image_urls = json.dumps(urls, ensure_ascii=False)
            if urls:
                self.image_url = urls[0]
        elif isinstance(urls, str):
            self.image_urls = urls
            self.image_url = urls

    def __repr__(self):
        return f"<TourProduct {self.name} ({self.region})>"

class ProductLike(db.Model):
    __tablename__ = 'product_likes'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='uix_user_product_like'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('tour_products.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Accommodation(db.Model):
    """관광지 연계 추천 숙박 시설 (민박, 호텔) 모델"""
    __tablename__ = 'accommodations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    acc_type = db.Column(db.String(20), nullable=False) # '민박' 또는 '호텔'
    region = db.Column(db.String(50), nullable=False, index=True) # 6대 권역
    tour_product_id = db.Column(db.Integer, db.ForeignKey('tour_products.id'), nullable=True) # 특정 관광 상품 연계 (선택)
    price_per_night = db.Column(db.Integer, nullable=False) # 1박 기본 정상 요금
    member_discount_rate = db.Column(db.Float, default=0.10) # 회원 우대 할인율 (기본 10%)
    rating = db.Column(db.Float, default=4.8) # 평점
    features = db.Column(db.String(255), nullable=True) # 주요 특징 (쉼표 구분)
    image_url = db.Column(db.String(255), default='/static/img/default-tour.jpg')
    description = db.Column(db.Text, nullable=True)
    is_recommended = db.Column(db.Boolean, default=True) # 추천 여부
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # 관광 상품 역참조 관계
    tour_product = db.relationship('TourProduct', backref=db.backref('accommodations', lazy='dynamic'))

    def get_discounted_price(self, is_member=True):
        """회원인 경우 할인된 1박 요금 반환"""
        if is_member:
            return int(self.price_per_night * (1 - self.member_discount_rate))
        return self.price_per_night

    def get_discount_amount(self, is_member=True):
        """1박 할인 금액 반환"""
        if is_member:
            return self.price_per_night - self.get_discounted_price(True)
        return 0

    def get_feature_list(self):
        """특징 태그를 리스트로 반환"""
        if self.features:
            return [f.strip() for f in self.features.split(',') if f.strip()]
        return []

    def __repr__(self):
        return f"<Accommodation [{self.acc_type}] {self.name} ({self.region})>"

