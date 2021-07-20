import pandas as pd
import streamlit as st

from db import RNA, create_sessionmaker


@st.memo
def get_results(_SessionMaker, row_count: int) -> pd.DataFrame:
    with _SessionMaker() as session:
        query = session.query(RNA).limit(row_count)
        results = pd.read_sql(query.statement, query.session.bind)
        return results


# Get or create our SQLAlchemy singleton
if "sessionmaker" not in st.session_state:
    st.session_state.sessionmaker = create_sessionmaker()

st.write("memo demo!")

results = get_results(st.session_state.sessionmaker, 10)
st.write(results)
