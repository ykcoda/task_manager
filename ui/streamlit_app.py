import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Task Manager AI", page_icon="🤖")
st.title("Task Manager AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask the assistant..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"message": prompt},
                    timeout=60,
                )
                response.raise_for_status()
                reply = response.json()
            except requests.exceptions.ConnectionError:
                reply = "Could not connect to the API. Make sure the FastAPI service is running."
            except requests.exceptions.HTTPError as e:
                reply = f"API error: {e}"
            except Exception as e:
                reply = f"Unexpected error: {e}"

        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
