from sqlalchemy import Column, Date, Float, Integer, String

from infra.database import Base


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    metric_description = Column(String)
    reference_date = Column(Date)
    acquisition_channel = Column(String)
    segment = Column(String)
    total = Column(Float)
