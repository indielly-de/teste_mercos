from sqlalchemy import Column, Date, Integer, Numeric, String

from infra.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id_transaction = Column(Integer, primary_key=True, index=True)
    cost_center_id = Column(Integer, nullable=False)
    payment_method_id = Column(Integer)
    due_date = Column(Date)
    amount = Column(Numeric(15, 2))
    payment_date = Column(Date)
    competence_date = Column(Date)
    periodicity = Column(String(50))
    result_center_id = Column(Integer)
