import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Ética Clásica", page_icon="🏛️", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CONFIGURACIÓN DE API ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la llave en Secrets")
    st.stop()

# --- BARRA LATERAL ---
st.sidebar.title("🏛️ Academia de Atenas")
escuela = st.sidebar.selectbox(
    "Selecciona la Escuela:",
    ["Aristotelismo (Liceo)", "Estoicismo (Stoa)", "Epicureísmo (El Jardín)"]
)

# Definir la instrucción según la escuela
if escuela == "Aristotelismo (Liceo)":
    inst = "Eres Aristóteles. Responde con el Justo Medio."
elif escuela == "Estoicismo (Stoa)":
    inst = "Eres un Estoico. Responde sobre lo que puedes controlar."
else:
    inst = "Eres Epicuro. Responde sobre la ataraxia."

# --- CUERPO PRINCIPAL ---
st.title("🏛️ Consultor de Ética Clásica")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Plantea tu dilema..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # CONFIGURACIÓN DEL MODELO JUSTO ANTES DE USARLO
        # Esta es la forma más compatible con la versión v1beta
        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=inst
            )
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error de Google: {e}")
            st.info("Intenta cambiar el nombre del modelo a 'models/gemini-1.5-flash' en el código si esto persiste.")
