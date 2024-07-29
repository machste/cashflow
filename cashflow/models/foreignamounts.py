from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, Double, DateTime
from sqlalchemy.orm import relationship

from cashflow.models.meta import Base
from cashflow.models.currencies import Currency


class ForeignAmount(Base):
    __tablename__ = 'foreign_amounts'
    id = Column(Integer, primary_key=True)
    amount = Column(Double, nullable=False)
    currency_id = Column(ForeignKey(Currency.id), nullable=False)
    currency = relationship(Currency)
    rate = Column(Double, nullable=True)
    date = Column(DateTime, nullable=True)
