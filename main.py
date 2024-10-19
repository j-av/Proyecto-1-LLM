from core import run_llm
import streamlit as st
from streamlit_chat import message
import base64

# Función para cargar la imagen como fondo
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center -120px; /* Subir la imagen de fondo */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Llamada a la función para agregar la imagen de fondo
add_bg_from_local('fondo2.jpg')

# Mostrar el título con estilo personalizado
st.markdown("<h1 style='text-align: center; font-size: 3em; color: white;'>Dreamworks ChatBot</h1>", unsafe_allow_html=True)

prompt = st.text_input("Prompt", placeholder="Enter your prompt here")

if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

def create_sources_string(source_urls: set[str]) -> str:
    if not source_urls:
        return ""
    
    return ""

if prompt:
    with st.spinner("Generating response.."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )

    
    formatted_response = generated_response['result']

    st.session_state["user_prompt_history"].append(prompt)
    st.session_state["chat_answers_history"].append(formatted_response)
    st.session_state["chat_history"].append(("human", prompt))
    st.session_state["chat_history"].append(("ai", generated_response["result"]))

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(st.session_state["chat_answers_history"], st.session_state["user_prompt_history"]):
        message(user_query, is_user=True)
        message(generated_response)
