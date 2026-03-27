import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser lo primero)
st.set_page_config(page_title="Ética Clásica", page_icon="🏛️", layout="wide")

# 2. INICIALIZACIÓN DEL ESTADO (Para evitar el AttributeError)
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DISEÑO Y FONDO KANDINSKY (CSS) ---
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
    background-color: rgba(255, 255, 255, 0.92); 
    z-index: -1;
}
h1, h2, h3 { color: #1a3a5a; font-family: 'Helvetica Neue', sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE API ---
# RECUERDA PONER TU LLAVE AQUÍ:
mi_llave = "AIzaSyCgfhjkefbA7PprBRjUvJ4ff4Am-cs_JB4" 
# --- CONFIGURACIÓN DE SEGURIDAD INTELIGENTE ---
try:
    # Primero intenta buscar en la nube (Streamlit Cloud)
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        # Si no hay secretos (estás en tu Mac), usa tu llave directa
        genai.configure(api_key="AIzaSyCgfhjkefbA7PprBRjUvJ4ff4Am-cs_JB4")
except Exception:
    # Si falla la búsqueda de secretos por completo, usa tu llave directa
    genai.configure(api_key="AIzaSyCgfhjkefbA7PprBRjUvJ4ff4Am-cs_JB4")

# --- BARRA LATERAL: ACADEMIA DE ATENAS Y GLOSARIO ---
st.sidebar.title("🏛️ Academia de Atenas")
escuela = st.sidebar.selectbox(
    "Selecciona la Escuela Ética:",
    ["Aristotelismo (Liceo)", "Estoicismo (Stoa)", "Epicureísmo (El Jardín)"]
)

st.sidebar.markdown("---")
st.sidebar.subheader(f"📚 Glosario: {escuela}")

if escuela == "Aristotelismo (Liceo)":
    instruccion = ("Eres un maestro del Liceo de Aristóteles. Responde basado en la Eudaimonía y el Justo Medio.")
    st.sidebar.info("**Eudaimonía:** Florecimiento humano.\n\n**Frónesis:** Sabiduría práctica.")
elif escuela == "Estoicismo (Stoa)":
    instruccion = ("Eres un filósofo estoico. Responde basado en lo que depende de nosotros y la Ataraxia.")
    st.sidebar.info("**Ataraxia:** Paz mental.\n\n**Logos:** Razón universal.")
else:
    instruccion = ("Eres un filósofo de Epicuro. Responde basado en la ausencia de dolor y el placer estable.")
    st.sidebar.info("**Aponía:** Sin dolor físico.\n\n**Ataraxia:** Sin angustia mental.")

# Configurar modelo
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", system_instruction=instruccion)

# --- CUERPO PRINCIPAL ---
st.title("🏛️ Consultor de Ética Clásica")
st.markdown(f"Escuela activa: **{escuela}**")

col_dilema, col_respuesta = st.columns([1, 2])

# --- COLUMNA 1: TU DILEMA ---
with col_dilema:
    st.subheader("Dilema Actual")
    # Buscamos el último mensaje del usuario
    user_messages = [m for m in st.session_state.messages if m["role"] == "user"]
    if user_messages:
        st.info(f"🤔 **Tu pregunta:**\n\n{user_messages[-1]['content']}")
    else:
        st.write("Aún no has planteado un dilema.")

    st.markdown("---")
    with st.expander("📖 Referencias Académicas"):
        st.write("* Ética a Nicómaco (Aristóteles)")
        st.write("* Meditaciones (Marco Aurelio)")
        st.write("* Carta a Meneceo (Epicuro)")

# --- COLUMNA 2: RESPUESTA ---
with col_respuesta:
    st.subheader("Reflexión Filosófica")
    
    # Contenedor para el historial de chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de chat
    if prompt := st.chat_input("Plantea tu dilema aquí..."):
        # Guardar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generar respuesta
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        # Refrescar para actualizar la Columna 1
        st.rerun()
