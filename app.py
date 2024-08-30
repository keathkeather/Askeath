import streamlit as st
import google.generativeai as genai
import os
import numpy as np
import random
import time
from dotenv import load_dotenv,dotenv_values
from chatPrompt import custom_prompts
st.markdown(
    """
    <style>
    .main {
        background-color: #FAF8ED;
    }
    .center-text{
        text-align: center;
        font-size: 40px;
        font-weight: bold;
    }
    .highlight{
        color : #F9B572
    }
    .chat-message{
        color: #F9B572;
    }
    .input-text{
        color:#faf8ed;
        }
    </style>
    """,
    unsafe_allow_html=True
)

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)



if "messages" not in st.session_state:
    st.session_state.messages = []



# Transform messages to the expected format
st.balloons()
st.markdown('<div class="center-text">Hello, I\'m <span class="highlight">Keath.<span>👨‍💻</div>', unsafe_allow_html=True)
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
st.markdown('<div class="center-text">', unsafe_allow_html=True)
if prompt := st.chat_input("Ask me anything about my creator :)"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Concatenate user input with custom prompts into a single string
    combined_prompts = "\n".join([prompt] + custom_prompts)

    # Generate content using the combined prompts
    with st.chat_message("assistant"):
        stream = model.generate_content(combined_prompts)
        response = stream.text

        # Display the response character by character with a delay
        response_container = st.empty()  # Create an empty container for the response
        displayed_text = ""
        for char in response:
            displayed_text += char
            response_container.markdown(displayed_text)
            time.sleep(0.02) 
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content":response})