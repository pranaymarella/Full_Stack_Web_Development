import sys
import random
import string

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()

# used for creating and verifying tokens
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))


class Users(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    picture = Column(String, default='')
    email = Column(String, index=True)
    password_hash = Column(String(64))
    created_date = Column(DateTime(timezone=True), server_default=func.now())

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    # Generates tokens for Oauth flow
    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    # method to verify tokens
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user_id = data['id']
        return user_id


class Category(Base):
    __tablename__ = 'categories'
    name = Column(String(80), nullable=False, index=True)
    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime(timezone=True), server_default=func.now())

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'created': self.created_date
        }


class Items(Base):
    __tablename__ = 'item'
    name = Column(String(80), nullable=False, index=True)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    category = relationship(Category)
    category_id = Column(Integer, ForeignKey('categories.id'))
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    author = relationship(Users)
    author_id = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'category_id': self.category_id
        }


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
