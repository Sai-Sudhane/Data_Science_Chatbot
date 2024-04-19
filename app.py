import google.generativeai as genai
import streamlit as st
from streamlit import set_page_config

set_page_config(page_title="Data Science Assistant", page_icon="💻")

st.markdown(
    "<h1 style='text-align: center; color: blue;'>Data Science Assistant🤖</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<h3 style='text-align: center; color: grey;'>I'm here to help you grow as a Data Scientist!</h3>",
    unsafe_allow_html=True,
)

key = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message Data Science Tutor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-pro-latest",
            system_instruction="""Consider yourself as a data scientist. Help the users by answering their queries related to data science! One main thing, dont answer for any queries apart from data science related things, if they ask convey them that you are only here to help them with data science""",
        )
        with st.spinner(text="Hold, Im generating contents for you😉..."):
            stream = model.generate_content(prompt)
            response = st.write(stream.text)
    st.session_state.messages.append({"role": "assistant", "content": stream.text})
