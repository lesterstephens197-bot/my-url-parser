import streamlit as st
import pandas as pd
from scraper import run_scraper


st.title(
    "THD Product Scraper"
)


file = st.file_uploader(
    "Upload THD URL Excel"
)


if file:

    df = pd.read_excel(file)

    st.write(df)


    if st.button("Start Scraping"):

        result = run_scraper(df)


        st.success(
            "Finished!"
        )


        st.download_button(
            "Download Excel",
            result
        )
