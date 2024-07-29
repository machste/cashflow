from sqlalchemy import Column, ForeignKey, func
from sqlalchemy import Integer, Double, Date, DateTime, Text, Boolean
from sqlalchemy.orm import relationship

from cashflow.models.meta import Base
from cashflow.models.user import User
from cashflow.models.categories import Category
from cashflow.models.foreignamounts import ForeignAmount


class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    report_date = Column(DateTime, nullable=False, server_default=func.now())
    reporter_id = Column(ForeignKey(User.id), nullable=False)
    reporter = relationship(User, foreign_keys=[reporter_id])
    date = Column(Date, nullable=False)
    amount = Column(Double, nullable=False, server_default='0.0')
    foreign_amount_id = Column(ForeignKey(ForeignAmount.id), nullable=True)
    foreign_amount = relationship(ForeignAmount)
    category_id = Column(ForeignKey(Category.id), nullable=False)
    category = relationship(Category)
    payer_id = Column(ForeignKey(User.id), nullable=False)
    payer = relationship(User, foreign_keys=[payer_id])
    private = Column(Boolean, nullable=False, server_default='FALSE')
    comment = Column(Text)
