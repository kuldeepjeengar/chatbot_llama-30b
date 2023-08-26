
from hugchat import hugchat
from hugchat.login import Login
import streamlit as st
st.set_page_config(page_title="🤨KD_CHAT😎")
#st.title("Chat_bot")
# Log in to huggingface and grant authorization to huggingchat
sign = Login("*******", "********")
cookies = sign.login()

# Save cookies to the local directory
cookie_path_dir = "./cookies_snapshot"
sign.saveCookiesToDir(cookie_path_dir)

# Create a ChatBot
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"
chatbot.chat("how are you")

# Create a new conversation
id = chatbot.new_conversation()
chatbot.change_conversation(id)


# switch LLM
chatbot.switch_llm(0) # switch to OpenAssistant/oasst-sft-6-llama-30b-xor
chatbot.switch_llm(1) # switch to meta-llama/Llama-2-70b-chat-hf
st.title('🤨KD_CHAT😎')


if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])    
def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot                        
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)
hf_email="*********"
hf_pass="**********"
if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt) 
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_pdf().encode('utf-8')



# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, hf_email, hf_pass) 
            st.write(response) 
            st.download_button(label="Download_text",data=response)
            
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)   
 