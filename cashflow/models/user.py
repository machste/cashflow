import bcrypt
from sqlalchemy import Column, Integer, Text

from cashflow.models.meta import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    firstname = Column(Text, nullable=False)
    lastname = Column(Text)
    passwd_hash = Column(Text)
    role = Column(Text, nullable=False, server_default="basic")

    @property
    def display_name(self):
        dname = self.firstname
        if self.lastname is not None:
            dname += f' {self.lastname}'
        return dname

    def set_password(self, pwd):
        self.passwd_hash = bcrypt.hashpw(pwd.encode('utf8'), bcrypt.gensalt())
    
    def check_password(self, pwd):
        return bcrypt.checkpw(pwd.encode('utf8'), self.passwd_hash)
