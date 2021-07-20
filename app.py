import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

from db import RNA

DB_URL = "postgresql://reader:NWDMCE5xdipIjRrp@hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs"

st.write("memo demo!")


engine = create_engine(DB_URL)
Session = sessionmaker(engine)
with Session() as session:
    query = session.query(RNA).limit(10)
    results = pd.read_sql(query.statement, query.session.bind)
    st.write(results)
