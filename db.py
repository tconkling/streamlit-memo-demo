from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class RNA(Base):
    __tablename__ = "rna"

    id = Column(BigInteger)
    upi = Column(String, primary_key=True)
    timestamp = Column(DateTime)
    userstamp = Column(String)
    crc64 = Column(String)
    len = Column(Integer)
    seq_short = Column(String)
    seq_long = Column(Text)
    md5 = Column(String)
