import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import RNA

st.title("🥒 memo + singleton demo")

st.markdown(f"""
Browse RNA sequences from the public [RNAcentral Postgres database](https://rnacentral.org/help/public-database).
- `@st.experimental_singleton` stores a singleton SQLAlchemy database connection
- The pickle-based `@st.experimental_memo` decorator caches query results.
""")

st.markdown("""
### Connecting to the database
We use `@st.experimental_singleton` to create a single SQLAlchemy engine that will be shared 
across all sessions and runs.
""")

with st.expander("Toggle code"):
    with st.echo():
        @st.experimental_singleton
        def get_db_sessionmaker() -> sessionmaker:
            # This is a publicly-accessible read-only database. We wouldn't
            # normally stick db creds in our code :)
            DB_URL = "postgresql://reader:NWDMCE5xdipIjRrp@hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs"
            engine = create_engine(DB_URL)
            return sessionmaker(engine)

st.markdown("""
### Querying the database
The `get_page` function queries the database and caches its results. Because
`@st.experimental_memo` cannot hash SQLAlchemy `sessionmaker` objects, we prefix the
`_sessionmaker` argument name with "_". 
""")

with st.expander("Toggle code"):
    with st.echo():
        @st.experimental_memo
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
                query = (
                    session
                        .query(RNA.id, RNA.seq_short, RNA.seq_long, RNA.len, RNA.upi)
                        .order_by(RNA.id)
                        .offset(page_size * page)
                        .limit(page_size)
                )
                return pd.read_sql(query.statement, query.session.bind)

st.markdown("""
### Results
We retrieve and display a single 1000-row "page" at a time. Pages that are
already cached will return more quickly, because they don't require a database
query.
""")

PAGE_SIZE = 1000

# Prompt for the results page
page = int(st.number_input(
    f"Select page ({PAGE_SIZE} results/page):", min_value=0)
)

# Run the query and show the results
results = get_page(get_db_sessionmaker(), page_size=PAGE_SIZE, page=page)
st.write(results)

# (It's safe to mutate results - it won't affect the cache.)
