from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

DB_URL = "postgresql://reader:NWDMCE5xdipIjRrp@hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs"


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


def create_sessionmaker() -> sessionmaker:
    """Create a new SQLAlchemy sessionmaker that connects to our DB."""
    engine = create_engine(DB_URL)
    return sessionmaker(engine)
