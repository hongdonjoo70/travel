import json
import random
from datetime import datetime, timezone, timedelta
from extensions import db
from models.user import User
from models.tour import Theme, TourProduct, RegionEnum, Accommodation
from models.cart import Cart
from models.review import Review

def seed_database():
    """초기 데이터 시딩 (테마, 사용자, 6개 권역 총 36개 풍부한 관광 상품[각 4장 고화질 이미지], 다채로운 이용 후기)"""
    # 1. 테마 등록 (휴양지, 체험, 문화/역사 등)
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

    # 2. 회원 계정 생성 (테스트 유저들)
    users_data = [
        {'username': 'hong', 'name': '홍길동', 'email': 'hong@example.com', 'phone': '010-1234-5678', 'role': 'MEMBER'},
        {'username': 'traveler_kim', 'name': '김여행', 'email': 'kim@example.com', 'phone': '010-2222-3333', 'role': 'MEMBER'},
        {'username': 'jeju_holic', 'name': '이바다', 'email': 'ocean@example.com', 'phone': '010-4444-5555', 'role': 'MEMBER'},
        {'username': 'tour_master', 'name': '박방랑', 'email': 'wanderer@example.com', 'phone': '010-7777-8888', 'role': 'MEMBER'},
        {'username': 'happy_min', 'name': '최민우', 'email': 'min@example.com', 'phone': '010-9999-0000', 'role': 'MEMBER'},
    ]

    created_users = []
    for u in users_data:
        user = User.query.filter_by(username=u['username']).first()
        if not user:
            user = User(
                username=u['username'],
                name=u['name'],
                email=u['email'],
                phone=u['phone'],
                role=u['role']
            )
            user.set_password('12341234')
            db.session.add(user)
            db.session.flush()

            # 장바구니 자동 생성
            cart = Cart(user_id=user.id)
            db.session.add(cart)
        created_users.append(user)

    # 3. 6대 권역별 총 36개 추천 관광 상품 정의 (권역당 6개씩, 관광지별 4개 고화질 이미지 슬라이드)
    products_data = [
        # --- [1] 서울/경기 (6개) ---
        {
            'name': '가평 아침고요수목원 & 남이섬 메타세쿼이아 낭만 힐링',
            'description': '사계절 아름다운 야생화와 정원이 펼쳐진 수목원과 북한강을 가로지르는 남이섬에서 즐기는 수도권 최고의 낭만 힐링 코스.',
            'region': RegionEnum.SEOUL_GYEONGGI.value,
            'theme': theme_map['RESORT'],
            'original_price': 65000,
            'member_discount_rate': 0.15,
            'recommendation_count': 890,
            'image_urls': [
                'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '수원 화성 성곽길 달빛 투어 & 플라잉 수원 열기구 체험',
            'description': '정조대왕의 얼이 깃든 수원화성 야경을 둘러보고 계류식 헬륨 기구에 탑승해 수원 도심의 야경을 한눈에 내려다보는 특별한 밤!',
            'region': RegionEnum.SEOUL_GYEONGGI.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 45000,
            'member_discount_rate': 0.10,
            'recommendation_count': 520,
            'image_urls': [
                'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1538485399081-7191377e8241?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1508873696983-2df5293cb32b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '포천 아트밸리 모노레일 & 허브아일랜드 불빛동화 힐링',
            'description': '버려진 채석장을 에메랄드빛 호수 예술공원으로 탈바꿈한 포천 아트밸리와 은은한 허브 향기 가득한 야경 불빛 축제 코스.',
            'region': RegionEnum.SEOUL_GYEONGGI.value,
            'theme': theme_map['RESORT'],
            'original_price': 58000,
            'member_discount_rate': 0.15,
            'recommendation_count': 710,
            'image_urls': [
                'https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '파주 헤이리 예술마을 도자기 공예 & 출판도시 북스테이',
            'description': '예술가들의 숨결이 깃든 헤이리 마을에서 직접 도자기를 빚어보고, 감각적인 건축미를 자랑하는 지혜의 숲에서 여유를 누립니다.',
            'region': RegionEnum.SEOUL_GYEONGGI.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 42000,
            'member_discount_rate': 0.10,
            'recommendation_count': 460,
            'image_urls': [
                'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '양평 두물머리 물안개 산책길 & 세미원 연꽃 힐링 정원',
            'description': '북한강과 남한강이 만나는 두물머리의 고즈넉한 풍경과 수생식물 정원 세미원에서 만나는 청량한 자연 휴식처.',
            'region': RegionEnum.SEOUL_GYEONGGI.value,
            'theme': theme_map['RESORT'],
            'original_price': 35000,
            'member_discount_rate': 0.10,
            'recommendation_count': 630,
            'image_urls': [
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '용인 한국민속촌 전통 옹기 만들기 & 야간 조선 한복 축제',
            'description': '살아있는 조선 시대로의 시간 여행! 장인과 함께하는 전통 공예 체험과 달빛 아래 펼쳐지는 신명나는 전통 연희 공연.',
            'region': RegionEnum.SEOUL_GYEONGGI.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 52000,
            'member_discount_rate': 0.15,
            'recommendation_count': 810,
            'image_urls': [
                'https://images.unsplash.com/photo-1538485399081-7191377e8241?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80'
            ]
        },

        # --- [2] 강원 (6개) ---
        {
            'name': '대관령 양떼목장 산책 & 평창 익스트림 루지 체험',
            'description': '한국의 알프스 대관령 초원을 거닐며 건초 주기 체험을 하고, 신나는 마운틴 루지로 스릴을 만끽하는 강원도 대표 코스!',
            'region': RegionEnum.GANGWON.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 85000,
            'member_discount_rate': 0.15,
            'recommendation_count': 1180,
            'image_urls': [
                'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '강릉 안목해변 커피거리 & 정동진 바다열차 낭만 투어',
            'description': '동해 바다의 푸른 파도를 바라보며 즐기는 스페셜티 커피 한 잔과 해안선을 따라 달리는 정동진 바다열차 낭만 여행.',
            'region': RegionEnum.GANGWON.value,
            'theme': theme_map['RESORT'],
            'original_price': 70000,
            'member_discount_rate': 0.10,
            'recommendation_count': 940,
            'image_urls': [
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1508873696983-2df5293cb32b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '춘천 남이섬 스카이라인 짚와이어 & 의암호 카누 물레길',
            'description': '북한강 상공을 활강하는 짜릿한 짚와이어와 잔잔한 의암호 수면 위를 미끄러지듯 노 젓는 낭만 카누 체험.',
            'region': RegionEnum.GANGWON.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 65000,
            'member_discount_rate': 0.15,
            'recommendation_count': 780,
            'image_urls': [
                'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '속초 영랑호 벚꽃 둘레길 & 설악산 권금성 케이블카',
            'description': '웅장한 설악산의 기암괴석을 한눈에 조망하는 권금성 케이블카와 영랑호 호수변을 따라 걷는 피톤치드 힐링 산책.',
            'region': RegionEnum.GANGWON.value,
            'theme': theme_map['RESORT'],
            'original_price': 78000,
            'member_discount_rate': 0.15,
            'recommendation_count': 1050,
            'image_urls': [
                'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '정선 아리랑 열차 & 구절리 풍경 레일바이크 어드벤처',
            'description': '산세 깊은 정선 산골짜기를 레일바이크로 시원하게 달리고, 정선 아리랑 5일장에서 정겨운 먹거리를 즐깁니다.',
            'region': RegionEnum.GANGWON.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 55000,
            'member_discount_rate': 0.10,
            'recommendation_count': 620,
            'image_urls': [
                'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '인제 원대리 자작나무숲 힐링 트레킹 & 오색 탄산온천',
            'description': '순백의 자작나무가 빼곡히 솟아오른 숲길을 걸으며 심신을 정화하고, 천연 탄산온천에 몸을 담그는 웰니스 힐링.',
            'region': RegionEnum.GANGWON.value,
            'theme': theme_map['RESORT'],
            'original_price': 68000,
            'member_discount_rate': 0.15,
            'recommendation_count': 830,
            'image_urls': [
                'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=800&q=80'
            ]
        },

        # --- [3] 충청 (6개) ---
        {
            'name': '단양 남한강 패러글라이딩 & 도담삼봉 수상 모터보트',
            'description': '청풍명월 충청의 푸른 하늘을 날아오르는 짜릿한 패러글라이딩과 남한강의 절경 도담삼봉을 누비는 익스트림 액티비티 체험!',
            'region': RegionEnum.CHUNGCHEONG.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 110000,
            'member_discount_rate': 0.15,
            'recommendation_count': 1250,
            'image_urls': [
                'https://images.unsplash.com/photo-1508873696983-2df5293cb32b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '태안 안면도 꽃지해수욕장 일몰 & 머드 갯벌 바지락 체험',
            'description': '할미·할아비 바위 너머로 지는 환상적인 서해안 3대 낙조를 감상하고 청정 갯벌에서 조개잡이 생태 체험을 즐깁니다.',
            'region': RegionEnum.CHUNGCHEONG.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 48000,
            'member_discount_rate': 0.10,
            'recommendation_count': 690,
            'image_urls': [
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '제천 청풍호반 케이블카 & 비봉산 하늘전망대 파노라마',
            'description': '내륙의 바다 청풍호를 가로질러 비봉산 정상에 오르면 사방으로 다도해 같은 호수 절경이 파노라마처럼 펼쳐집니다.',
            'region': RegionEnum.CHUNGCHEONG.value,
            'theme': theme_map['RESORT'],
            'original_price': 62000,
            'member_discount_rate': 0.15,
            'recommendation_count': 740,
            'image_urls': [
                'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1508873696983-2df5293cb32b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '보령 대천해수욕장 해상 짚트랙 & 보령해저터널 드라이브',
            'description': '서해 바다 위를 시속 80km로 활강하는 스릴 만점 해상 짚트랙과 국내 최장 보령해저터널을 달리는 드라이브 코스.',
            'region': RegionEnum.CHUNGCHEONG.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 58000,
            'member_discount_rate': 0.10,
            'recommendation_count': 590,
            'image_urls': [
                'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '부여 백제역사유적지구 & 궁남지 포룡정 밤도깨비 산책',
            'description': '찬란했던 백제 사비 시대의 왕궁 터를 둘러보고, 한국 최초의 인공 정원 궁남지 연못을 거닐며 역사의 정취를 느낍니다.',
            'region': RegionEnum.CHUNGCHEONG.value,
            'theme': theme_map['RESORT'],
            'original_price': 42000,
            'member_discount_rate': 0.10,
            'recommendation_count': 450,
            'image_urls': [
                'https://images.unsplash.com/photo-1538485399081-7191377e8241?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '아산 지중해마을 골목 산책 & 파라다이스 스파 도고 힐링',
            'description': '이국적인 산토리니 감성의 하얀 골목을 걷고 유황 온천수로 피로를 녹여내는 충남 아산의 힐링 스파 여행.',
            'region': RegionEnum.CHUNGCHEONG.value,
            'theme': theme_map['RESORT'],
            'original_price': 75000,
            'member_discount_rate': 0.15,
            'recommendation_count': 820,
            'image_urls': [
                'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=800&q=80'
            ]
        },

        # --- [4] 전라 (6개) ---
        {
            'name': '여수 밤바다 낭만 요트 세일링 & 오동도 동백열차',
            'description': '선상에서 즐기는 불꽃놀이와 낭만 가득한 여수 밤바다 요트 투어, 바다 위의 꽃섬 오동도를 탐방하는 전라 대표 휴양 코스.',
            'region': RegionEnum.JEONLA.value,
            'theme': theme_map['RESORT'],
            'original_price': 80000,
            'member_discount_rate': 0.15,
            'recommendation_count': 1340,
            'image_urls': [
                'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '순천만 갈대군락지 생태 탐방 & 국가정원 스카이큐브',
            'description': '끝없이 펼쳐진 황금빛 순천만 갈대숲과 세계 각국의 정원을 한자리에서 관람할 수 있는 대한민국 생태 수도 투어.',
            'region': RegionEnum.JEONLA.value,
            'theme': theme_map['RESORT'],
            'original_price': 45000,
            'member_discount_rate': 0.10,
            'recommendation_count': 1120,
            'image_urls': [
                'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1508873696983-2df5293cb32b?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '전주 한옥마을 다도 체험 & 명품 전통 한복 대여 패키지',
            'description': '고즈넉한 전주 한옥마을 골목을 전통 한복을 입고 거닐며 명인과 함께하는 전통 다도 예절을 배우는 문화 감성 여행입니다.',
            'region': RegionEnum.JEONLA.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 50000,
            'member_discount_rate': 0.15,
            'recommendation_count': 980,
            'image_urls': [
                'https://images.unsplash.com/photo-1538485399081-7191377e8241?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '담양 죽녹원 대나무숲 산책 & 메타세쿼이아 힐링 로드',
            'description': '초록빛 대숲에서 뿜어져 나오는 음이온을 마시며 심신을 힐링하고, 곧게 뻗은 메타세쿼이아 길을 자전거로 달립니다.',
            'region': RegionEnum.JEONLA.value,
            'theme': theme_map['RESORT'],
            'original_price': 38000,
            'member_discount_rate': 0.10,
            'recommendation_count': 760,
            'image_urls': [
                'https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '보성 대한다원 햇녹차 찻잎 따기 & 편백 치유의 숲',
            'description': '계단식 초록 차밭의 절경을 배경으로 직접 찻잎을 덖고 맛보는 티클래스와 피톤치드 편백나무숲 트레킹.',
            'region': RegionEnum.JEONLA.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 52000,
            'member_discount_rate': 0.15,
            'recommendation_count': 680,
            'image_urls': [
                'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '신안 퍼플섬 보랏빛 다리 투어 & 태평염전 천일염 만들기',
            'description': '지붕도 다리도 온통 보라색인 환상의 섬 퍼플교를 거닐고 유네스코 생물권보전지역 증도에서 천일염 소금 만들기 체험.',
            'region': RegionEnum.JEONLA.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 64000,
            'member_discount_rate': 0.15,
            'recommendation_count': 590,
            'image_urls': [
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80'
            ]
        },

        # --- [5] 경북 (6개) ---
        {
            'name': '울릉도 해안누리길 일주 & 독도 평화 바다 유람선',
            'description': '태고의 신비를 간직한 울릉도의 화산 비경 해안길을 걷고 대한민국 동쪽 끝 독도를 직접 밟아보는 평생의 버킷리스트 투어.',
            'region': RegionEnum.GYEONGBUK.value,
            'theme': theme_map['RESORT'],
            'original_price': 180000,
            'member_discount_rate': 0.20,
            'recommendation_count': 1520,
            'image_urls': [
                'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1508873696983-2df5293cb32b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '경주 불국사 & 황리단길 야경 감성 힐링 산책',
            'description': '신라 천년의 역사 유적지와 트렌디한 황리단길 카페 골목, 동궁과 월지의 환상적인 야경을 감상하는 경북 힐링 명소입니다.',
            'region': RegionEnum.GYEONGBUK.value,
            'theme': theme_map['RESORT'],
            'original_price': 75000,
            'member_discount_rate': 0.15,
            'recommendation_count': 1190,
            'image_urls': [
                'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1538485399081-7191377e8241?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '포항 호미곶 상생의 손 일출 & 환호공원 스페이스워크',
            'description': '한반도에서 가장 먼저 해가 뜨는 호미곶 바다 일출을 보고, 공중에 떠 있는 롤러코스터 계단 스페이스워크를 걷습니다.',
            'region': RegionEnum.GYEONGBUK.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 55000,
            'member_discount_rate': 0.10,
            'recommendation_count': 960,
            'image_urls': [
                'https://images.unsplash.com/photo-1508873696983-2df5293cb32b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '안동 하회마을 전통 탈춤 관람 & 유교문화 한옥 고택 스테이',
            'description': '낙동강이 S자로 감싸 흐르는 하회마을에서 유서 깊은 양반 가옥을 체험하고 하회별신굿탈놀이를 관람합니다.',
            'region': RegionEnum.GYEONGBUK.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 85000,
            'member_discount_rate': 0.15,
            'recommendation_count': 870,
            'image_urls': [
                'https://images.unsplash.com/photo-1538485399081-7191377e8241?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '청송 주산지 왕버들 물안개 숲 & 솔기온천 스파 웰니스',
            'description': '물속에 뿌리를 내린 신비로운 왕버들과 아침 물안개의 비경을 감상하고, 미끌미끌한 알칼리 솔기온천에서 피로를 풉니다.',
            'region': RegionEnum.GYEONGBUK.value,
            'theme': theme_map['RESORT'],
            'original_price': 72000,
            'member_discount_rate': 0.15,
            'recommendation_count': 640,
            'image_urls': [
                'https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '문경새재 황톳길 맨발 트레킹 & 오미자 와인동굴 투어',
            'description': '영남대로 과거길 문경새재 흙길을 맨발로 걸으며 자연을 느끼고, 와인터널에서 붉은 오미자 스파클링 와인을 시음합니다.',
            'region': RegionEnum.GYEONGBUK.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 49000,
            'member_discount_rate': 0.10,
            'recommendation_count': 580,
            'image_urls': [
                'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80'
            ]
        },

        # --- [6] 제주 (6개) ---
        {
            'name': '제주 비자림 숲길 & 함덕 해변 프라이빗 힐링 투어',
            'description': '천년의 숲 비자림에서 피톤치드를 마시고, 에메랄드빛 함덕 서우봉 해변에서 즐기는 여유로운 제주 휴양 코스입니다.',
            'region': RegionEnum.JEJU.value,
            'theme': theme_map['RESORT'],
            'original_price': 120000,
            'member_discount_rate': 0.20,
            'recommendation_count': 1680,
            'image_urls': [
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '제주 우도 전기차 일주 & 해녀와 함께하는 해산물 물질',
            'description': '산호초 백사장이 빛나는 섬 속의 섬 우도를 전기차로 시원하게 달리고, 현직 해녀와 함께 바다 물질 체험을 합니다.',
            'region': RegionEnum.JEJU.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 95000,
            'member_discount_rate': 0.15,
            'recommendation_count': 1450,
            'image_urls': [
                'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1508873696983-2df5293cb32b?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '협재 해수욕장 선셋 요트 투어 & 차귀도 야생 돌고래 탐선',
            'description': '비양도를 배경으로 노을 지는 서쪽 바다에서 샴페인을 곁들인 선셋 세일링과 차귀도 앞바다 야생 돌고래를 만납니다.',
            'region': RegionEnum.JEJU.value,
            'theme': theme_map['RESORT'],
            'original_price': 110000,
            'member_discount_rate': 0.20,
            'recommendation_count': 1390,
            'image_urls': [
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '한라산 영실 탐방로 절경 트레킹 & 흑돼지 미식 바비큐',
            'description': '오백나한 기암괴석과 병풍바위가 웅장하게 둘러싼 영실코스를 가볍게 트레킹하고 제주 청정 흑돼지 바비큐를 즐깁니다.',
            'region': RegionEnum.JEJU.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 88000,
            'member_discount_rate': 0.15,
            'recommendation_count': 1220,
            'image_urls': [
                'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '서귀포 쇠소깍 전통 나룻배 카약 & 외돌개 해안 올레길',
            'description': '용암이 굳어 형성된 기묘한 계곡 쇠소깍에서 투명 카약을 타고 남쪽 서귀포 푸른 바다의 해안 절벽 올레길을 걷습니다.',
            'region': RegionEnum.JEJU.value,
            'theme': theme_map['RESORT'],
            'original_price': 65000,
            'member_discount_rate': 0.15,
            'recommendation_count': 1080,
            'image_urls': [
                'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=800&q=80'
            ]
        },
        {
            'name': '조천 곶자왈 에코랜드 숲속 기차 & 피톤치드 족욕 스파',
            'description': '화산 송이 곶자왈 원시림을 증기기관차를 타고 둘러보며 천연 허브 온천수에 발을 담그는 전 연령 맞춤 힐링 코스.',
            'region': RegionEnum.JEJU.value,
            'theme': theme_map['EXPERIENCE'],
            'original_price': 58000,
            'member_discount_rate': 0.10,
            'recommendation_count': 890,
            'image_urls': [
                'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80',
                'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=800&q=80'
            ]
        }
    ]

    sample_review_comments = [
        ("기대 이상으로 만족스러웠던 여행!", "가족들과 함께 다녀왔는데 코스가 정말 알차고 힐링 제대로 하고 왔습니다. 회원 할인받아서 가성비도 최고였어요!"),
        ("경치가 정말 장관이네요.", "사진보다 실물이 훨씬 아름답습니다. 가이드분도 친절하시고 일정이 무리 없어 부모님 모시고 가기 딱 좋습니다."),
        ("다음에 또 방문하고 싶어요.", "숙소와 연계된 코스도 좋고 특히 체험 프로그램이 인상 깊었습니다. 다음엔 친구들과 또 예약할게요!"),
        ("회원 혜택이 쏠쏠합니다.", "다른 여행사보다 회원 할인율이 높아서 기분 좋게 다녀왔습니다. 강력 추천합니다!"),
        ("잊지 못할 추억이 생겼습니다.", "답답한 도시를 벗어나 맑은 공기 마시며 즐겁게 힐링했습니다. 후기 믿고 갔는데 대만족이에요.")
    ]

    for p_info in products_data:
        json_urls = json.dumps(p_info['image_urls'], ensure_ascii=False)
        first_img = p_info['image_urls'][0]

        product = TourProduct.query.filter_by(name=p_info['name']).first()
        if not product:
            product = TourProduct(
                name=p_info['name'],
                description=p_info['description'],
                region=p_info['region'],
                theme_id=p_info['theme'].id,
                original_price=p_info['original_price'],
                member_discount_rate=p_info['member_discount_rate'],
                recommendation_count=p_info['recommendation_count'],
                image_url=first_img,
                image_urls=json_urls
            )
            db.session.add(product)
            db.session.flush()

            # 상품별로 1~3개의 다채로운 후기 자동 등록
            num_reviews = random.randint(1, 3)
            for idx in range(num_reviews):
                reviewer = created_users[(idx + product.id) % len(created_users)]
                title, content = sample_review_comments[(idx + product.id) % len(sample_review_comments)]
                rating = 5 if idx == 0 else random.choice([4, 5])
                review = Review(
                    user_id=reviewer.id,
                    product_id=product.id,
                    title=f"[{product.region}] {title}",
                    content=content,
                    rating=rating
                )
        else:
            product.image_urls = json_urls
            product.image_url = first_img

    # 4. 6대 권역별 회원 전용 연계 추천 숙박 시설 (민박 18개 + 호텔 18개 = 총 36개)
    accommodations_data = [
        # --- [1] 서울/경기 ---
        {'name': '가평 잣향기 힐링 한옥민박', 'acc_type': '민박', 'region': RegionEnum.SEOUL_GYEONGGI.value, 'price_per_night': 65000, 'member_discount_rate': 0.10, 'rating': 4.9, 'features': '바비큐장, 한옥온돌, 독채, 조식제공', 'image_url': 'https://images.unsplash.com/photo-1538485399081-7191377e8241?auto=format&fit=crop&w=600&q=80', 'description': '잣나무 숲속 맑은 공기와 고즈넉한 전통 한옥의 따스함을 즐길 수 있는 힐링 민박입니다.'},
        {'name': '양평 물소리길 감성 숲속민박', 'acc_type': '민박', 'region': RegionEnum.SEOUL_GYEONGGI.value, 'price_per_night': 70000, 'member_discount_rate': 0.10, 'rating': 4.8, 'features': '개별테라스, 불멍화로, 북한강뷰, 와이파이', 'image_url': 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?auto=format&fit=crop&w=600&q=80', 'description': '두물머리와 세미원 인근 물소리와 숲속 피톤치드가 가득한 감성 쉼터입니다.'},
        {'name': '파주 헤이리 아트빌리지 예술가민박', 'acc_type': '민박', 'region': RegionEnum.SEOUL_GYEONGGI.value, 'price_per_night': 75000, 'member_discount_rate': 0.15, 'rating': 4.8, 'features': '도자기공방, 예술가갤러리, 웰컴티', 'image_url': 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80', 'description': '헤이리 예술마을 중심에 위치해 예술가들의 감성과 작품을 직접 체험할 수 있습니다.'},
        {'name': '가평 리버사이드 럭셔리 호텔', 'acc_type': '호텔', 'region': RegionEnum.SEOUL_GYEONGGI.value, 'price_per_night': 150000, 'member_discount_rate': 0.15, 'rating': 4.9, 'features': '인피니티풀, 리버뷰, 피트니스, 뷔페조식', 'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=600&q=80', 'description': '북한강변 최고급 시설과 야외 인피니티 온수풀을 갖춘 프리미엄 호텔입니다.'},
        {'name': '수원 노블레스 비즈니스 & 스파 호텔', 'acc_type': '호텔', 'region': RegionEnum.SEOUL_GYEONGGI.value, 'price_per_night': 120000, 'member_discount_rate': 0.15, 'rating': 4.7, 'features': '루프탑바, 사우나, 화성야경뷰, 발렛파킹', 'image_url': 'https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=600&q=80', 'description': '수원화성 야경을 한눈에 조망할 수 있는 루프탑과 편안한 휴식을 제공하는 호텔입니다.'},
        {'name': '포천 아트스파 리조트 호텔', 'acc_type': '호텔', 'region': RegionEnum.SEOUL_GYEONGGI.value, 'price_per_night': 135000, 'member_discount_rate': 0.10, 'rating': 4.8, 'features': '천연온천수, 스파가든, 키즈룸, 산책로', 'image_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=600&q=80', 'description': '지하 천연 암반 온천수로 온 가족이 힐링할 수 있는 포천 대표 리조트 호텔입니다.'},

        # --- [2] 강원 ---
        {'name': '평창 대관령 언덕 통나무민박', 'acc_type': '민박', 'region': RegionEnum.GANGWON.value, 'price_per_night': 70000, 'member_discount_rate': 0.10, 'rating': 4.9, 'features': '목장전망, 벽난로, 유기농조식, 바비큐', 'image_url': 'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=600&q=80', 'description': '해발 700m 대관령 초원이 시원하게 내려다보이는 아늑한 핀란드식 통나무 민박입니다.'},
        {'name': '강릉 경포호수 고요한 솔향민박', 'acc_type': '민박', 'region': RegionEnum.GANGWON.value, 'price_per_night': 60000, 'member_discount_rate': 0.10, 'rating': 4.8, 'features': '소나무숲, 자전거대여, 솔향다도, 주차완비', 'image_url': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80', 'description': '수령 100년 이상의 소나무 숲에 둘러싸여 솔바람 소리와 함께 휴식할 수 있습니다.'},
        {'name': '인제 자작나무숲 황토민박', 'acc_type': '민박', 'region': RegionEnum.GANGWON.value, 'price_per_night': 65000, 'member_discount_rate': 0.15, 'rating': 4.8, 'features': '황토구들방, 숲속쉼터, 장작불멍, 산채조식', 'image_url': 'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=600&q=80', 'description': '천연 황토와 참나무 장작 구들장으로 건강한 하룻밤을 선사하는 웰니스 힐링 민박입니다.'},
        {'name': '강릉 씨사이드 오션뷰 호텔', 'acc_type': '호텔', 'region': RegionEnum.GANGWON.value, 'price_per_night': 180000, 'member_discount_rate': 0.20, 'rating': 4.9, 'features': '동해일출뷰, 스카이라운지, 야외풀, 다이닝', 'image_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=600&q=80', 'description': '동해바다 수평선 위로 떠오르는 장엄한 일출을 객실 침대에서 바로 감상할 수 있습니다.'},
        {'name': '평창 알펜시아 마운틴 호텔', 'acc_type': '호텔', 'region': RegionEnum.GANGWON.value, 'price_per_night': 160000, 'member_discount_rate': 0.15, 'rating': 4.8, 'features': '슬로프뷰, 사우나, 패밀리스위트, 루지연계', 'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=600&q=80', 'description': '대관령 청정 자연 속 사계절 액티비티와 최고급 휴양을 동시에 누리는 호텔입니다.'},
        {'name': '속초 설악 헤리티지 리조트 호텔', 'acc_type': '호텔', 'region': RegionEnum.GANGWON.value, 'price_per_night': 145000, 'member_discount_rate': 0.15, 'rating': 4.8, 'features': '울산바위뷰, 온천스파, 바비큐테라스, 카페', 'image_url': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=600&q=80', 'description': '설악산 웅장한 기암괴석 병풍 뷰와 천연 온천 스파를 만끽할 수 있는 리조트입니다.'},

        # --- [3] 충청 ---
        {'name': '단양 남한강변 절벽바위민박', 'acc_type': '민박', 'region': RegionEnum.CHUNGCHEONG.value, 'price_per_night': 55000, 'member_discount_rate': 0.10, 'rating': 4.8, 'features': '강변데크, 패러글라이딩픽업, 모닥불, 무료조식', 'image_url': 'https://images.unsplash.com/photo-1508873696983-2df5293cb32b?auto=format&fit=crop&w=600&q=80', 'description': '도담삼봉 인근 남한강 여울소리를 들으며 바비큐와 패러글라이딩을 즐길 수 있습니다.'},
        {'name': '태안 안면도 소나무 노을민박', 'acc_type': '민박', 'region': RegionEnum.CHUNGCHEONG.value, 'price_per_night': 65000, 'member_discount_rate': 0.10, 'rating': 4.8, 'features': '갯벌체험도구, 일몰전망, 개별바비큐, 야외정원', 'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80', 'description': '꽃지해수욕장 도보 거리, 황금빛 낙조를 바라보며 편안히 쉬어가는 서해 감성 민박입니다.'},
        {'name': '부여 백제달빛 고택 한옥민박', 'acc_type': '민박', 'region': RegionEnum.CHUNGCHEONG.value, 'price_per_night': 60000, 'member_discount_rate': 0.10, 'rating': 4.9, 'features': '전통한옥, 궁남지인접, 다도체험, 툇마루', 'image_url': 'https://images.unsplash.com/photo-1538485399081-7191377e8241?auto=format&fit=crop&w=600&q=80', 'description': '백제의 숨결이 깃든 고풍스러운 목조 한옥에서 즐기는 특별한 시간 여행입니다.'},
        {'name': '제천 청풍호 레이크 리조트 호텔', 'acc_type': '호텔', 'region': RegionEnum.CHUNGCHEONG.value, 'price_per_night': 140000, 'member_discount_rate': 0.15, 'rating': 4.8, 'features': '청풍호수뷰, 케이블카인접, 글램핑풀, 패밀리룸', 'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=600&q=80', 'description': '내륙의 바다 청풍호를 한눈에 굽어보는 환상적인 호수 전망 프리미엄 호텔입니다.'},
        {'name': '보령 대천 머드오션 호텔', 'acc_type': '호텔', 'region': RegionEnum.CHUNGCHEONG.value, 'price_per_night': 130000, 'member_discount_rate': 0.10, 'rating': 4.7, 'features': '해수욕장도보1분, 오션뷰발코니, 스파욕조, 펍', 'image_url': 'https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=600&q=80', 'description': '대천 백사장 바로 앞, 서해 파도 소리와 짚트랙 액티비티를 함께 즐기는 호텔입니다.'},
        {'name': '아산 온양 프리미엄 온천 호텔', 'acc_type': '호텔', 'region': RegionEnum.CHUNGCHEONG.value, 'price_per_night': 125000, 'member_discount_rate': 0.15, 'rating': 4.8, 'features': '천연유황온천, 실내수영장, 조식뷔페, 피트니스', 'image_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=600&q=80', 'description': '왕실의 휴양지 온양 온천수로 온몸의 피로를 녹여내는 웰니스 스파 호텔입니다.'},

        # --- [4] 전라 ---
        {'name': '전주 한옥마을 교동 달빛민박', 'acc_type': '민박', 'region': RegionEnum.JEONLA.value, 'price_per_night': 65000, 'member_discount_rate': 0.15, 'rating': 4.9, 'features': '전통한옥체험, 한복대여할인, 조식토스트, 정원', 'image_url': 'https://images.unsplash.com/photo-1538485399081-7191377e8241?auto=format&fit=crop&w=600&q=80', 'description': '전주 한옥마을 중심, 따뜻한 온돌방과 정갈한 마당 정원이 어우러진 명품 민박입니다.'},
        {'name': '담양 죽림향기 대숲민박', 'acc_type': '민박', 'region': RegionEnum.JEONLA.value, 'price_per_night': 58000, 'member_discount_rate': 0.10, 'rating': 4.8, 'features': '대나무숲산책로, 죽로차제공, 개별바비큐, 피톤치드', 'image_url': 'https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&w=600&q=80', 'description': '초록빛 대나무 숲길과 바람 소리가 머무는 청량한 힐링 쉼터입니다.'},
        {'name': '신안 증도 갯벌체험 힐링민박', 'acc_type': '민박', 'region': RegionEnum.JEONLA.value, 'price_per_night': 62000, 'member_discount_rate': 0.10, 'rating': 4.7, 'features': '퍼플섬인접, 소금밭뷰, 자전거대여, 해산물바비큐', 'image_url': 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=600&q=80', 'description': '유네스코 청정 갯벌과 보랏빛 다리가 있는 퍼플섬 인근의 평화로운 섬마을 민박입니다.'},
        {'name': '여수 해상 베네치아 마린 호텔', 'acc_type': '호텔', 'region': RegionEnum.JEONLA.value, 'price_per_night': 170000, 'member_discount_rate': 0.20, 'rating': 4.9, 'features': '여수밤바다뷰, 루프탑수영장, 요트투어연계, 조식뷔페', 'image_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=600&q=80', 'description': '선상 불꽃놀이와 낭만 가득한 여수 밤바다를 파노라마로 조망하는 오션 호텔입니다.'},
        {'name': '순천만 에코 스테이 호텔', 'acc_type': '호텔', 'region': RegionEnum.JEONLA.value, 'price_per_night': 125000, 'member_discount_rate': 0.15, 'rating': 4.8, 'features': '갈대밭전망, 친환경어메니티, 자전거대여, 정원라운지', 'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=600&q=80', 'description': '대한민국 생태 수도 순천만의 갈대 군락과 국가정원을 편안하게 여행할 수 있습니다.'},
        {'name': '보성 그린티힐 리조트 호텔', 'acc_type': '호텔', 'region': RegionEnum.JEONLA.value, 'price_per_night': 135000, 'member_discount_rate': 0.15, 'rating': 4.8, 'features': '녹차밭파노라마뷰, 편백사우나, 테라스바비큐, 티라운지', 'image_url': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=600&q=80', 'description': '초록빛 계단식 차밭의 장관을 배경으로 피톤치드 편백 스파를 즐길 수 있습니다.'},

        # --- [5] 경북 ---
        {'name': '안동 하회마을 부용대 한옥민박', 'acc_type': '민박', 'region': RegionEnum.GYEONGBUK.value, 'price_per_night': 70000, 'member_discount_rate': 0.10, 'rating': 4.9, 'features': '중요민속마을독채, 유교다도체험, 툇마루, 낙동강뷰', 'image_url': 'https://images.unsplash.com/photo-1538485399081-7191377e8241?auto=format&fit=crop&w=600&q=80', 'description': '천년의 역사를 간직한 하회마을에서 선비의 풍류와 고택의 여유를 누립니다.'},
        {'name': '경주 황리단길 돌담 감성민박', 'acc_type': '민박', 'region': RegionEnum.GYEONGBUK.value, 'price_per_night': 68000, 'member_discount_rate': 0.15, 'rating': 4.9, 'features': '황리단길도보3분, 야외불멍존, 커피머신, 감성인테리어', 'image_url': 'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=600&q=80', 'description': '신라 고분의 신비로움과 현대적인 트렌드가 공존하는 황리단길 대표 감성 민박입니다.'},
        {'name': '문경새재 옛길 도자기민박', 'acc_type': '민박', 'region': RegionEnum.GYEONGBUK.value, 'price_per_night': 55000, 'member_discount_rate': 0.10, 'rating': 4.8, 'features': '황톳길입구, 도자기체험할인, 개별정원, 계곡물소리', 'image_url': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80', 'description': '과거길 문경새재 흙길을 맨발로 걷고 오미자 와인과 함께 편안히 쉴 수 있습니다.'},
        {'name': '경주 보문호수 팰리스 호텔', 'acc_type': '호텔', 'region': RegionEnum.GYEONGBUK.value, 'price_per_night': 165000, 'member_discount_rate': 0.15, 'rating': 4.9, 'features': '보문호수전망, 스파온천풀, 한식뷔페, 키즈클럽', 'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=600&q=80', 'description': '벚꽃 피는 보문호수변 특급 시설과 온천 스파를 자랑하는 랜드마크 호텔입니다.'},
        {'name': '포항 영일대 해상 스카이 호텔', 'acc_type': '호텔', 'region': RegionEnum.GYEONGBUK.value, 'price_per_night': 140000, 'member_discount_rate': 0.10, 'rating': 4.8, 'features': '스페이스워크뷰, 인피니티풀, 일출전망대, 라운지바', 'image_url': 'https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=600&q=80', 'description': '호미곶 일출과 영일대 해상누각, 스페이스워크를 품은 도심형 오션 호텔입니다.'},
        {'name': '울릉도 코스모스 힐링 호텔', 'acc_type': '호텔', 'region': RegionEnum.GYEONGBUK.value, 'price_per_night': 220000, 'member_discount_rate': 0.20, 'rating': 5.0, 'features': '독도유람선선착장인접, 절벽해안뷰, 전용셔틀, 최고급다이닝', 'image_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=600&q=80', 'description': '동해 끝 태고의 신비를 간직한 울릉도 웅장한 절벽과 코발트빛 바다를 조망합니다.'},

        # --- [6] 제주 ---
        {'name': '제주 비자림 돌담 프라이빗 민박', 'acc_type': '민박', 'region': RegionEnum.JEJU.value, 'price_per_night': 80000, 'member_discount_rate': 0.15, 'rating': 4.9, 'features': '제주현무암독채, 감귤밭정원, 바비큐그릴, 자쿠지', 'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80', 'description': '천년의 숲 비자림 인근, 돌담으로 둘러싸인 아늑한 독채에서 즐기는 제주 힐링입니다.'},
        {'name': '서귀포 쇠소깍 나루터 감성민박', 'acc_type': '민박', 'region': RegionEnum.JEJU.value, 'price_per_night': 75000, 'member_discount_rate': 0.10, 'rating': 4.8, 'features': '바다도보5분, 야외테라스, 웰컴과일, 넷플릭스', 'image_url': 'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=600&q=80', 'description': '쇠소깍 투명 카약 체험장 인접, 남쪽 푸른 바다의 해안 절벽을 마주하는 민박입니다.'},
        {'name': '우도 산호해변 별빛 오두막민박', 'acc_type': '민박', 'region': RegionEnum.JEJU.value, 'price_per_night': 85000, 'member_discount_rate': 0.15, 'rating': 4.9, 'features': '우도봉전망, 산호백사장뷰, 전기차충전, 낚시대대여', 'image_url': 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=600&q=80', 'description': '섬 속의 섬 우도의 산호 백사장을 앞마당처럼 누리는 특별한 감성 숙소입니다.'},
        {'name': '제주 함덕 에메랄드 오션 호텔', 'acc_type': '호텔', 'region': RegionEnum.JEJU.value, 'price_per_night': 175000, 'member_discount_rate': 0.20, 'rating': 4.9, 'features': '함덕서우봉뷰, 인피니티온수풀, 스카이라운지, 조식', 'image_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=600&q=80', 'description': '에메랄드빛 함덕 바다를 발아래 두고 따뜻한 인피니티 온수풀을 즐길 수 있습니다.'},
        {'name': '협재 선셋 베이 리조트 호텔', 'acc_type': '호텔', 'region': RegionEnum.JEJU.value, 'price_per_night': 190000, 'member_discount_rate': 0.20, 'rating': 4.9, 'features': '비양도노을뷰, 풀빌라스위트, 요트세일링연계, 전용스파', 'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=600&q=80', 'description': '비양도 너머로 붉게 물드는 서쪽 바다의 선셋을 조망하는 최고급 호텔입니다.'},
        {'name': '서귀포 올레 중문 헤리티지 호텔', 'acc_type': '호텔', 'region': RegionEnum.JEJU.value, 'price_per_night': 160000, 'member_discount_rate': 0.15, 'rating': 4.8, 'features': '야자수정원, 천연암반수풀, 올레길직결, 피트니스', 'image_url': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=600&q=80', 'description': '이국적인 야자수 정원과 중문 관광단지의 편의시설을 완벽하게 누리는 리조트입니다.'}
    ]

    for acc_info in accommodations_data:
        acc = Accommodation.query.filter_by(name=acc_info['name']).first()
        if not acc:
            acc = Accommodation(
                name=acc_info['name'],
                acc_type=acc_info['acc_type'],
                region=acc_info['region'],
                price_per_night=acc_info['price_per_night'],
                member_discount_rate=acc_info['member_discount_rate'],
                rating=acc_info['rating'],
                features=acc_info['features'],
                image_url=acc_info['image_url'],
                description=acc_info['description'],
                is_recommended=True
            )
            db.session.add(acc)
        else:
            acc.price_per_night = acc_info['price_per_night']
            acc.member_discount_rate = acc_info['member_discount_rate']
            acc.features = acc_info['features']
            acc.image_url = acc_info['image_url']
            acc.description = acc_info['description']

    db.session.commit()
    total_count = TourProduct.query.count()
    acc_count = Accommodation.query.count()
    print(f"[Seed] 성공! 총 {total_count}개 관광 상품 및 {acc_count}개 연계 추천 숙박 시설(민박/호텔) 데이터가 적재되었습니다.")

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_database()
