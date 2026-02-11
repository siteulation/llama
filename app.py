import streamlit as st
import ollama

# --- Configuration ---
MODEL_NAME = "socialnetwooky/llama3.2-abliterated:3b"

st.set_page_config(page_title="Abliterated Chat", page_icon="🤖")
st.title("Llama 3.2 Abliterated")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me anything..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Stream the response from Ollama
        try:
            stream = ollama.chat(
                model=MODEL_NAME,
                messages=st.session_state.messages,
                stream=True,
            )
            
            for chunk in stream:
                content = chunk.get("message", {}).get("content", "")
                full_response += content
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error connecting to Ollama: {e}")
