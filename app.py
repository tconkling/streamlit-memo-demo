from math import ceil

import pandas as pd
import streamlit as st
from sqlalchemy import func

from db import RNA, create_sessionmaker

PAGE_SIZE = 20


@st.memo
def get_page(_SessionMaker, page_size: int, page: int) -> pd.DataFrame:
    with _SessionMaker() as session:
        offset = page_size * page
        query = session.query(RNA).offset(offset).limit(page_size)
        return pd.read_sql(query.statement, query.session.bind)

# @st.memo
# def get_num_pages(_SessionMaker, page_size: int) -> int:
#     with _SessionMaker as session:
#         num_rows = session.query(func.count(RNA.id))
#     return int(ceil(num_rows / page_size))


# Get or create our SQLAlchemy singleton
if "sessionmaker" not in st.session_state:
    st.session_state.sessionmaker = create_sessionmaker()

st.write("memo demo!")

# num_pages = get_num_pages(st.session_state.sessionmaker, PAGE_SIZE)
# st.write("num_pages", num_pages)

results = get_page(st.session_state.sessionmaker, PAGE_SIZE, 1)
st.write(results)
