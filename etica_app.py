import streamlit as st
import google.generativeai as genai

# 1. Configuración básica
st.set_page_config(page_title="Ética Clásica", layout="wide")

# 2. Estilo visual rápido
st.markdown("<style>.stApp { background-color: #f0f2f6; }</style>", unsafe_allow_html=True)

# 3. Conexión con Google (Simplificada al máximo)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Por favor, configura GOOGLE_API_KEY en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 4. Selección de Escuela
st.sidebar.title("🏛️ Academia")
escuela = st.sidebar.selectbox("Escuela:", ["Aristóteles", "Estoicos", "Epicuro"])
prompt_sistema = f"Eres un filósofo de la escuela {escuela}. Responde de forma breve y académica."

# 5. Chat
st.title("🏛️ Consultor de Ética")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("¿Cuál es tu dilema?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
       try:
            # Con la versión 0.5.4 de la librería, este nombre es el correcto
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content([prompt_sistema, prompt])
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
