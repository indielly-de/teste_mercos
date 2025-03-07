from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String

from infra.database import Base


class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)
    id_transaction = Column(Integer, ForeignKey("transactions.id_transaction"))
    id_cost_center = Column(Integer)
    reference_date = Column(Date)
    acquisition_channel = Column(String(100))
    segment = Column(String(100))
    allocated_amount = Column(Numeric(15, 2))
