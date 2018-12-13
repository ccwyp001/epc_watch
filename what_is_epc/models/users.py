from ..extensions import db, SLBigInteger
from datetime import datetime
from flask_bcrypt import generate_password_hash


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(256))
    create_at = db.Column(db.DateTime(), default=datetime.utcnow)
    update_at = db.Column(db.DateTime(), default=datetime.utcnow)
    roles = db.Column(db.Integer, default=1)  # 0x0 reject 0x1 temp 0x2 real 0x4 admin

    def __repr__(self):
        return '<User %r>' % self.username

    def wechat_account(self):
        return '%d' % (self.id)

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, access_token):
        self._access_token = access_token

    @property
    def refresh_token(self):
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, refresh_token):
        self._refresh_token = refresh_token

    @classmethod
    def from_json(cls, json_data):
        username = json_data.get('username')
        password = json_data.get('password') or '123456'
        password = generate_password_hash(password)
        return Users(
            username=username,
            password=password)

    def display(self):
        return {'username': self.username,
                'roles': self.roles,
                'id': self.id
                }
