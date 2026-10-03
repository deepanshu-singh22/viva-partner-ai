import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="AI Viva & Exam Partner", page_icon="🎓")

st.title("🎓 AI Exam & Viva Partner")
st.caption("Built for my friend — 100% Local & Private Study Companion")

# Sidebar for Subject selection
subject = st.sidebar.selectbox(
    "Select Subject / Topic",
    ["Python & Data Structures", "Web Development", "Operating Systems", "General Computer Science"]
)

st.write(f"### Current Mode: {subject} Practice")
st.info("I am your AI Examiner! Ask me to quiz you, explain a tough concept, or give mock viva questions.")

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User prompt
if prompt := st.chat_input("Enter your answer or ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call local Ollama AI model
    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            system_prompt = f"You are a helpful and strict Viva examiner for {subject}. Ask concise viva questions, grade answers, and give short corrections."
            full_prompt = f"{system_prompt}\nUser: {prompt}"
            
            try:
                res = requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": "llama3.2", "prompt": full_prompt, "stream": False}
                )
                response_text = res.json()["response"]
            except Exception as e:
                response_text = "Error: Ollama is not running. Start Ollama in your terminal first."

            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})