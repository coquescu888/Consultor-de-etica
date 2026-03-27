import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Ética Clásica", page_icon="🏛️", layout="wide")

# 2. INICIALIZACIÓN DEL ESTADO
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DISEÑO (CSS) ---
st.markdown("""
<style>
.stApp {
    background-image: url("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Vassily_Kandinsky%2C_1913_-_Composition_VII.jpg/1200px-Vassily_Kandinsky%2C_1913_-_Composition_VII.jpg");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}
.stApp::before {
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(255, 255, 255, 0.94); 
    z-index: -1;
}
h1, h2, h3 { color: #1a3a5a; font-family: 'Helvetica Neue', sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE API ---
# Intentamos obtener la llave de los secretos de Streamlit
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ No se encontró la llave 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# --- BARRA LATERAL ---
st.sidebar.title("🏛️ Academia de Atenas")
escuela = st.sidebar.selectbox(
    "Selecciona la Escuela Ética:",
    ["Aristotelismo (Liceo)", "Estoicismo (Stoa)", "Epicureísmo (El Jardín)"]
)

if escuela == "Aristotelismo (Liceo)":
    instruccion = "Eres un maestro del Liceo de Aristóteles. Responde con sabiduría práctica y el concepto de eudaimonía."
elif escuela == "Estoicismo (Stoa)":
    instruccion = "Eres un filósofo estoico. Responde basado en la virtud, la razón y lo que podemos controlar."
else:
    instruccion = "Eres un filósofo epicúreo. Responde buscando la ataraxia y el placer racional."

# Inicializar el modelo con la instrucción seleccionada
# --- CONFIGURACIÓN DEL MODELO (VERSIÓN ANTIFALLOS) ---
# Forzamos la búsqueda del modelo disponible
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", # Prueba sin 'models/' primero
        system_instruction=instruccion
    )
except Exception:
    # Si falla, intentamos con el nombre largo
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash", 
        system_instruction=instruccion
    )

# --- CUERPO PRINCIPAL ---
st.title("🏛️ Consultor de Ética Clásica")
st.markdown(f"Escuela activa: **{escuela}**")

col_dilema, col_respuesta = st.columns([1, 2])

with col_dilema:
    st.subheader("Tu Dilema")
    user_messages = [m for m in st.session_state.messages if m["role"] == "user"]
    if user_messages:
        st.info(f"🤔 **Última pregunta:**\n\n{user_messages[-1]['content']}")
    
    st.markdown("---")
    with st.expander("📖 Referencias"):
        st.write("* Ética a Nicómaco")
        st.write("* Meditaciones")
        st.write("* Carta a Meneceo")

with col_respuesta:
    # Mostrar historial
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de chat
    if prompt := st.chat_input("Plantea tu dilema aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Los filósofos están deliberando..."):
                # Aquí dejamos que el error aparezca si algo falla
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        st.rerun()
