import streamlit as st

PROD_STYLE = """\
<style>
    /* Reduce large header */
    .stAppHeader[data-testid="stHeader"] {
        height: 1rem;
    }
    /* Reduce large padding top */
    .block-container {
        padding-top: 1rem;
    }
    /* Adjust main container width */
    .stMain .block-container[data-testid="stMainBlockContainer"] {
        max-width: min(2000px, 60%);
        min-width: min(1200px, 85%);
    }
    
    /* Hide status widget button */
    div[data-testid="stStatusWidget"] div button {
        display: none;
    }

    /* Reduce gap between filters */
    [data-testid="stPopoverBody"] .stVerticalBlock [data-testid=stVerticalBlock] {
        gap: 0.3rem;
    }
</style>
"""
APP_TITLE = "IntelliMail"
HEADER_TEXT = f"""\
<h1 style='text-align: center;'>
    {APP_TITLE}
    <span style='font-weight: normal; position: relative; top: -1.25em; font-size: 35%;'>
        &nbsp;&nbsp;&nbsp;AI-Powered ⚡
    </span>
</h1>
"""


def init_app():
    st.set_page_config(page_title=APP_TITLE, page_icon="📧")
    st.markdown(PROD_STYLE, unsafe_allow_html=True)
    st.markdown(HEADER_TEXT, unsafe_allow_html=True)
