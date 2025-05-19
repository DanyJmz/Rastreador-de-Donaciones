from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Donation(Base):
    __tablename__ = 'donations'
    id = Column(Integer, primary_key=True)
    donor = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    campaign = Column(String, nullable=False)
    timestamp = Column(Float, nullable=False)
    tx_hash = Column(String, nullable=False)

class Disbursement(Base):
    __tablename__ = 'disbursements'
    id = Column(Integer, primary_key=True)
    campaign = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    recipient = Column(String, nullable=False)
    timestamp = Column(Float, nullable=False)
    tx_hash = Column(String, nullable=False)

engine = create_engine('sqlite:///donations.db')
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)