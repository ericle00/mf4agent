import streamlit as st

                                                                      
def render():
    """
    Renders the entire application, including the sidebar style, markdown styles, and hiding anchor links in markdown.
    """
    render_hide_anchor_link_markdown()                                                                                          
    
                                                                                   
def render_hide_anchor_link_markdown():
    st.markdown("""   
    <style>
        [data-testid="stHeaderActionElements"] {
            display: none;
        }
    </style>
    """,  unsafe_allow_html=True)