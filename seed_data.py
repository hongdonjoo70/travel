from extensions import db
from models.user import User
from models.tour import Theme, TourProduct, RegionEnum
from models.cart import Cart
from models.review import Review

def seed_database():
    """초기 데이터 시딩 (테마, 사용자, 6개 권역 관광 상품, 후기)"""
    # 1. 테마 등록 (휴양지, 체험, 확장 테마)
    themes_data = [
        {'code': 'RESORT', 'name': '휴양지', 'description': '지친 일상을 벗어나 자연 속에서 편안히 쉬어가는 힐링 여행'},
        {'code': 'EXPERIENCE', 'name': '체험', 'description': '보고 듣고 직접 만져보는 오감 만족 이색 액티비티 & 문화 체험'},
        {'code': 'CULTURE', 'name': '문화/역사', 'description': '유네스코 세계유산과 천년 역사의 숨결을 느끼는 투어'}
    ]

    theme_map = {}
    for t_data in themes_data:
        theme = Theme.query.filter_by(code=t_data['code']).first()
        if not theme:
            theme = Theme(code=t_data['code'], name=t_data['name'], description=t_data['description'])
            db.session.add(theme)
            db.session.flush()
        theme_map[t_data['code']] = theme

    # 2. 테스트 회원 계정 생성
    test_user = User.query.filter_by(username='hong').first()
    if not test_user:
        test_user = User(
            username='hong',
            name='홍길동',
            email='hong@example.com',
            phone='010-1234-5678',
            role='MEMBER'
        )
        test_user.set_password('12341234')
        db.session.add(test_user)
        db.session.flush()

        # 장바구니 자동 생성
        cart = Cart(user_id=test_user.id)
        db.session.add(cart)

    # 3. 6개 지역별 관광 상품 등록
    products_data = [
        {
            'name': '제주 비자림 숲길 & 함덕 해변 프라이빗 힐링 투어',
            'description': '천년의 숲 비자림에서 피톤치드를 마시고, 에메랄드빛 함덕 서우봉 해변에서 즐기는 여유로운 제주 휴양 코스입니다.',
            'region': RegionEnum.JEJU.value,
            'theme': theme_map['RESORT'],
            'original_price': 120000,
            'member_discount_rate': 0.20, # 20% 회원할인
            'recommendation_count': 1420,
            'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80'
        },
        {
            'name': '대관령 양떼목장 산책 & 평창 익스트림 루지 체험',
            'description': '한국의 알프스 대관령 초원을 거닐며 건초 주기 체험을 하고, 신나는 마운틴 루지로 스릴을 만끽하는 강원도 대표 코스!',
            'region': RegionEnum.GANGWON.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 85000,
            'member_discount_rate': 0.15,
            'recommendation_count': 1180,
            'image_url': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80'
        },
        {
            'name': '전주 한옥마을 다도 체험 & 명품 전통 한복 대여 패키지',
            'description': '고즈넉한 전주 한옥마을 골목을 전통 한복을 입고 거닐며 명인과 함께하는 전통 다도 예절을 배우는 문화 감성 여행입니다.',
            'region': RegionEnum.JEONLA.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 50000,
            'member_discount_rate': 0.15,
            'recommendation_count': 980,
            'image_url': 'https://images.unsplash.com/photo-1538485399081-7191377e8241?auto=format&fit=crop&w=600&q=80'
        },
        {
            'name': '가평 아침고요수목원 & 남이섬 메타세쿼이아 낭만 힐링',
            'description': '사계절 아름다운 야생화와 정원이 펼쳐진 수목원과 북한강을 가로지르는 남이섬에서 즐기는 수도권 최고의 휴양지 코스.',
            'region': RegionEnum.SEOUL_GYEONGGI.value,
            'theme': theme_map['RESORT'],
            'original_price': 65000,
            'member_discount_rate': 0.15,
            'recommendation_count': 890,
            'image_url': 'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=600&q=80'
        },
        {
            'name': '경주 불국사 & 황리단길 야경 감성 힐링 산책',
            'description': '신라 천년의 역사 유적지와 트렌디한 황리단길 카페 골목, 동궁과 월지의 환상적인 야경을 감상하는 경북 힐링 명소입니다.',
            'region': RegionEnum.GYEONGBUK.value,
            'theme': theme_map['RESORT'],
            'original_price': 75000,
            'member_discount_rate': 0.15,
            'recommendation_count': 760,
            'image_url': 'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=600&q=80'
        },
        {
            'name': '단양 남한강 패러글라이딩 & 도담삼봉 수상 모터보트',
            'description': '청풍명월 충청의 푸른 하늘을 날아오르는 짜릿한 패러글라이딩과 남한강의 절경 도담삼봉을 누비는 익스트림 액티비티 체험!',
            'region': RegionEnum.CHUNGCHEONG.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 110000,
            'member_discount_rate': 0.15,
            'recommendation_count': 640,
            'image_url': 'https://images.unsplash.com/photo-1508873696983-2df5293cb32b?auto=format&fit=crop&w=600&q=80'
        },
        {
            'name': '수원 화성 성곽길 달빛 투어 & 플라잉 수원 열기구 체험',
            'description': '정조대왕의 얼이 깃든 수원화성 야경을 둘러보고 계류식 헬륨 기구에 탑승해 수원 도심의 야경을 한눈에 내려다보는 특별한 밤!',
            'region': RegionEnum.SEOUL_GYEONGGI.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 45000,
            'member_discount_rate': 0.10,
            'recommendation_count': 520,
            'image_url': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=600&q=80'
        },
        {
            'name': '여수 밤바다 낭만 요트 세일링 & 오동도 동백열차',
            'description': '선상에서 즐기는 불꽃놀이와 낭만 가득한 여수 밤바다 요트 투어, 바다 위의 꽃섬 오동도를 탐방하는 전라 대표 휴양 코스.',
            'region': RegionEnum.JEONLA.value,
            'theme': theme_map['RESORT'],
            'original_price': 80000,
            'member_discount_rate': 0.15,
            'recommendation_count': 490,
            'image_url': 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=600&q=80'
        }
    ]

    for p_info in products_data:
        existing = TourProduct.query.filter_by(name=p_info['name']).first()
        if not existing:
            product = TourProduct(
                name=p_info['name'],
                description=p_info['description'],
                region=p_info['region'],
                theme_id=p_info['theme'].id,
                original_price=p_info['original_price'],
                member_discount_rate=p_info['member_discount_rate'],
                recommendation_count=p_info['recommendation_count'],
                image_url=p_info['image_url']
            )
            db.session.add(product)
            db.session.flush()

            # 샘플 후기 추가
            if test_user:
                review = Review(
                    user_id=test_user.id,
                    product_id=product.id,
                    title=f"정말 만족스러웠던 {product.region} 여행이었습니다!",
                    content="회원 할인가로 저렴하게 예약해서 다녀왔는데 기대 이상으로 훌륭했습니다. 코스 구성도 알차고 가족들과 좋은 추억 만들고 갑니다. 추천합니다!",
                    rating=5
                )
                db.session.add(review)

    db.session.commit()
    print("[Seed] 데이터베이스 초기 데이터가 성공적으로 적재되었습니다.")

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_database()

