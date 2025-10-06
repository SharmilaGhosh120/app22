import streamlit as st
import openai
from openai import OpenAI

# Set page config
st.set_page_config(page_title="AI Companion", page_icon="🤖", layout="wide")

# Initialize OpenAI client with API key from secrets
if "openai_api_key" not in st.secrets:
    st.error("OpenAI API key not found in Streamlit secrets. Please add 'OPENAI_API_KEY' to your .streamlit/secrets.toml file.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from OpenAI (using GPT-4o-mini as a cost-effective model; replace with 'gpt-4o' for better performance)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            full_response = "Sorry, I encountered an error. Please try again."

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar for info (optional: add user data collection if needed, but keeping it simple as per core request)
with st.sidebar:
    st.title("AI Companion Info")
    st.info("Powered by OpenAI's foundation models for a domain-agnostic AI experience.")
    st.markdown("---")
    st.info("""
    We collect basic details like your name, email, phone number, and any other information you choose to provide.
    We collect technical info like your IP address and browser type to help improve our platform.
    We use this data to create your account, process payments, respond to queries, and keep you informed.
    Your information stays safe with us—we don't sell or share it with anyone except trusted services like payment processors.
    We use cookies to understand how people use our site and make improvements. You can always block cookies in your browser settings.
    If you want to update or delete your information, just email us and we'll take care of it.
    """)
    # Optional form for basic user info (not stored here; in production, integrate with database)
    name = st.text_input("Your Name (optional)")
    email = st.text_input("Email (optional)")
    if st.button("Submit Info"):
        st.success("Info noted! (In a real app, this would be saved securely.)")