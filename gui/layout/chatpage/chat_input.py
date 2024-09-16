import json
import streamlit as st

from gui.chatbot.chatbot_wrapper import ChatbotGUIAgentWrapper
from gui.styles.chatpage_headers import ChatPageHeader

from gui.layout.chatpage.chat_output import output_llm_content

from gui.keys.st_ss import ST_SS

                                    
def render_chat_input(st_ss) -> None:
    """Renders a chat input field, processes user input, and generates a response from the chatbot, updating the chat history."""
        # Ask user for question
    if user_query := st.chat_input("Input your question!"):
        if st_ss["selected_mf4_file"] != "None":
            chatbot_wrapper = ChatbotGUIAgentWrapper(st_ss=st_ss)
            
            # Generate header from user query
            generated_user_query_header = chatbot_wrapper.generate_header_from_user_query(user_query)
            user_content_serialized = json.dumps([generated_user_query_header, user_query])
            
            # User container
            st.markdown(ChatPageHeader.GENERATED_USER_QUERY_HEADER.format(generated_user_query_header))
            with st.chat_message(name="user"):
                st.code(user_query, language=None)

            # Assistant container
            with st.chat_message("assistant"):
                # Create chatbot object
                llm_output_serialized = chatbot_wrapper.ask(user_query)
                    
                # Extract llm answer, executed code and plot if any
                output_llm_content(llm_output_serialized)

                # Append user query and answer to chat history
                st_ss[ST_SS.CHAT_HISTORY_KEY].append({"role": "user", "content": user_content_serialized})  
                st_ss[ST_SS.CHAT_HISTORY_KEY].append({"role": "assistant", "content": llm_output_serialized})
        else:
            st.error("🚨 You forgot to select a mf4 file! 🚨")