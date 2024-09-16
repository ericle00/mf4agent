import json
import streamlit as st

from gui.styles.chatpage_headers import ChatPageHeader
from gui.keys.st_ss import ST_SS
                                     
from gui.layout.chatpage.chat_output import output_llm_content
     
                                                                                                
def display_chat_history(st_ss) -> None:
    """Displays the chat history from session state, formatting user and assistant messages accordingly."""
    # Display chat history
    for message in st_ss[ST_SS.CHAT_HISTORY_KEY]:
        content_serialized = message["content"]
        if message["role"] == "user":
            generated_user_query_header, user_query = json.loads(content_serialized)
            st.markdown(ChatPageHeader.GENERATED_USER_QUERY_HEADER.format(generated_user_query_header))
            with st.chat_message(message["role"]):
                st.code(user_query, language=None)
        if message["role"] == "assistant":
            with st.chat_message(message["role"]):
                output_llm_content(content_serialized)