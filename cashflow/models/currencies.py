from sqlalchemy import Column, func
from sqlalchemy import Integer, Text, Double, DateTime

from cashflow.models.meta import Base


class Currency(Base):
    __tablename__ = 'currencies'
    id = Column(Integer, primary_key=True)
    code = Column(Text, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    rate = Column(Double, nullable=False, server_default='1.0')
    date = Column(DateTime, nullable=False, server_default=func.now())

    def __str__(self):
        return f'{self.code} (rate: {self.rate})'

