from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True) # ID
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(80), nullable=False)                                # 이름
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)   # email
    phone = db.Column(db.String(30), unique=True, nullable=False)                 # 전화번호
    role = db.Column(db.String(20), default='MEMBER')                             # MEMBER, ADMIN
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    reviews = db.relationship('Review', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    cart = db.relationship('Cart', backref='user', uselist=False, cascade='all, delete-orphan')
    likes = db.relationship('ProductLike', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_member(self):
        return self.is_authenticated

    def __repr__(self):
        return f"<User {self.username} ({self.name})>"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
