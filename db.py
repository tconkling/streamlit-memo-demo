from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# CREATE TABLE rnacen.rna (
#     id bigint,
#     upi character varying(30) PRIMARY KEY,
#     timestamp timestamp without time zone,
#     userstamp character varying(60),
#     crc64 character(16),
#     len integer,
#     seq_short character varying(4000) CHECK (char_length(seq_short::text) >= 10),
#     seq_long text,
#     md5 character varying(64),
#     CONSTRAINT constraint_rna_seq_short_n CHECK (seq_short IS NULL OR (len - length(replace(seq_short::text, 'N'::text, ''::text)))::numeric <= round(0.1 * len::numeric)),
#     CONSTRAINT constraint_rna_seq_long_n CHECK (seq_long IS NULL OR (len - length(replace(seq_long, 'N'::text, ''::text)))::numeric <= round(0.1 * len::numeric))
# ) TABLESPACE pfmegrnargs;


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
