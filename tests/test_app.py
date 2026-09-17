import unittest
from app import create_app
from config import Config
from extensions import db
from models.user import User
from models.tour import Theme, TourProduct, RegionEnum, ProductLike
from models.cart import Cart, CartItem
from models.order import Order
from models.review import Review

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False # 테스트 편의를 위해 CSRF 비활성화

class TravelAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # 기본 테마 및 테스트 데이터 설정
        self.theme_resort = Theme(code='RESORT', name='휴양지')
        self.theme_exp = Theme(code='EXPERIENCE', name='체험')
        db.session.add_all([self.theme_resort, self.theme_exp])
        db.session.commit()

        # 6개 지역 대표 상품 생성
        self.p1 = TourProduct(
            name='제주 힐링 투어',
            description='제주 휴양지 코스',
            region=RegionEnum.JEJU.value,
            theme_id=self.theme_resort.id,
            original_price=100000,
            member_discount_rate=0.20, # 20% 할인
            recommendation_count=500
        )
        self.p2 = TourProduct(
            name='강원 루지 체험',
            description='강원도 액티비티 체험 코스',
            region=RegionEnum.GANGWON.value,
            theme_id=self.theme_exp.id,
            original_price=50000,
            member_discount_rate=0.10, # 10% 할인
            recommendation_count=800
        )
        db.session.add_all([self.p1, self.p2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signup_and_login(self):
        """1. 회원가입 (id, 이름, email, 전화번호) 및 로그인 테스트"""
        # 회원가입
        res = self.client.post('/auth/signup', data={
            'username': 'traveler1',
            'name': '김여행',
            'email': 'kim@travel.com',
            'phone': '010-5555-6666',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        user = User.query.filter_by(username='traveler1').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, '김여행')
        self.assertEqual(user.phone, '010-5555-6666')
        self.assertTrue(user.check_password('password123'))
        self.assertIsNotNone(user.cart) # 장바구니 자동 생성 확인

        # 로그인
        res = self.client.post('/auth/login', data={
            'username': 'traveler1',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('김여행', res.get_data(as_text=True))

    def test_regional_and_theme_filters(self):
        """2. 6개 권역 및 테마별 상품 필터링 테스트"""
        # 메인 화면
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

        # 제주 지역 필터링
        res_jeju = self.client.get('/?region=제주')
        self.assertIn('제주 힐링 투어', res_jeju.get_data(as_text=True))

        # 테마 필터링 (체험)
        res_theme = self.client.get('/?theme=EXPERIENCE')
        self.assertIn('강원 루지 체험', res_theme.get_data(as_text=True))

    def test_popular_ranking_screen(self):
        """3. 추천 수가 높은 관광상품 랭킹 화면 테스트"""
        res = self.client.get('/products/popular')
        self.assertEqual(res.status_code, 200)
        text = res.get_data(as_text=True)
        # 800 추천수를 가진 강원 루지 체험이 1위여야 함
        pos_p2 = text.find('강원 루지 체험')
        pos_p1 = text.find('제주 힐링 투어')
        self.assertTrue(pos_p2 < pos_p1, "추천 수가 높은 상품이 먼저 나와야 합니다.")

    def test_cart_and_member_discount(self):
        """4. 장바구니 및 회원 할인 계산 테스트"""
        # 회원 가입 및 로그인
        self.client.post('/auth/signup', data={
            'username': 'shopper',
            'name': '박쇼핑',
            'email': 'shopper@test.com',
            'phone': '010-1111-2222',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.client.post('/auth/login', data={'username': 'shopper', 'password': 'password123'})

        # 장바구니에 제주 상품 2개 담기 (정가 100,000 -> 회원가 80,000)
        res = self.client.post('/cart/add', data={
            'product_id': self.p1.id,
            'quantity': 2
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        cart_res = self.client.get('/cart')
        cart_html = cart_res.get_data(as_text=True)
        # 회원 할인액 40,000원, 최종 160,000원 반영 확인
        self.assertIn('160,000원', cart_html)
        self.assertIn('40,000원', cart_html)

    def test_checkout_and_payment(self):
        """5. 결제 및 주문 생성 검증 (회원 할인 저장 확인)"""
        # 회원 로그인
        self.client.post('/auth/signup', data={
            'username': 'buyer',
            'name': '이결제',
            'email': 'buyer@test.com',
            'phone': '010-3333-4444',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.client.post('/auth/login', data={'username': 'buyer', 'password': 'password123'})

        # 단일 상품 바로 결제 (p1: 정가 100,000원 -> 회원가 80,000원)
        res = self.client.post('/order/pay', data={
            'direct_product_id': self.p1.id,
            'quantity': 1,
            'payment_method': 'CARD'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        order = Order.query.filter_by(final_amount=80000).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.original_amount, 100000)
        self.assertEqual(order.discount_amount, 20000)
        self.assertEqual(order.payment.paid_amount, 80000)

    def test_review_permission(self):
        """6. 후기 권한 테스트: 비회원은 읽기만, 회원은 작성 가능"""
        # 비회원 상세 조회 (200 OK)
        res = self.client.get(f'/products/{self.p1.id}')
        self.assertEqual(res.status_code, 200)

        # 비회원이 후기 작성 시도 -> 로그인 페이지로 302 리다이렉트
        res_unauth = self.client.post(f'/reviews/product/{self.p1.id}/create', data={
            'rating': '5',
            'title': '비회원 작성 시도',
            'content': '작성될 수 없어야 합니다.'
        })
        self.assertEqual(res_unauth.status_code, 302)
        self.assertIn('/auth/login', res_unauth.location)

        # 회원 로그인 후 후기 작성
        self.client.post('/auth/signup', data={
            'username': 'reviewer',
            'name': '최리뷰',
            'email': 'reviewer@test.com',
            'phone': '010-7777-8888',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.client.post('/auth/login', data={'username': 'reviewer', 'password': 'password123'})

        res_review = self.client.post(f'/reviews/product/{self.p1.id}/create', data={
            'rating': '5',
            'title': '최고의 제주 여행이었습니다',
            'content': '회원 할인도 받고 즐겁게 힐링하고 왔습니다.'
        }, follow_redirects=True)
        self.assertEqual(res_review.status_code, 200)

        # 리뷰 DB 확인
        rev = Review.query.filter_by(title='최고의 제주 여행이었습니다').first()
        self.assertIsNotNone(rev)
        self.assertEqual(rev.rating, 5)

if __name__ == '__main__':
    unittest.main()
