import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import RNA

st.title("@st.memo demo")

st.markdown(f"""
This app queries the public [RNAcentral Postgres database](https://rnacentral.org/help/public-database).
""")

st.markdown("""
### Connecting to the database
We use `st.session_state` to create a singleton SQLAlchemy engine on our first run.
""")
with st.echo():
    if "sessionmaker" not in st.session_state:
        DB_URL = "postgresql://reader:NWDMCE5xdipIjRrp@hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs"
        engine = create_engine(DB_URL)
        st.session_state.sessionmaker = sessionmaker(engine)

st.markdown("""
### Querying the database
The `get_page` function queries the database and caches its results. Because
`@st.memo` cannot hash SQLAlchemy `sessionmaker` objects, we prefix the
`_sessionmaker` argument name with "_". 
""")

with st.echo():
    @st.memo
    def get_page(_sessionmaker, page_size: int, page: int) -> pd.DataFrame:
        """Retrieve rows from the RNA database, and cache them.

        Parameters
        ----------
        _sessionmaker : a SQLAlchemy session factory. Because this arg name is
            prefixed with "_", it won't be hashed.
        page_size : the number of rows in a page of result
        page : the page number to retrieve

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the retrieved rows. Mutating it won't affect
            the cache.
        """
        with _sessionmaker() as session:
            offset = page_size * page
            query = session.query(RNA).order_by(RNA.id).offset(offset).limit(page_size)
            return pd.read_sql(query.statement, query.session.bind)

st.markdown("""### Results""")
with st.echo():
    # Prompt for the results page
    page = int(st.number_input("Select a results page:", min_value=0, value=0, step=1))

    # Run the query and show the results
    results = get_page(st.session_state.sessionmaker, page_size=10, page=page)
    st.write(results)
