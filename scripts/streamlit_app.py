import streamlit as st
import openai
import os
from datetime import datetime
import random
import time

# Configuración de la página
st.set_page_config(
    page_title="MiVendedor.AI - Como tener el mejor vendedor, pero virtual",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Algunas frases random para hacer más humano
FRASES_CARGANDO = [
    "Pensando como respondería mi abuela que tenía almacén...",
    "Consultando con el vendedor virtual más simpático del barrio...",
    "Armando una respuesta que no suene a robot...",
    "Buscando la forma más amable de decirte esto...",
    "Activando modo 'vendedor con 20 años de experiencia'..."
]

EMOJIS_RANDOM = ["🛍️", "👕", "👗", "👔", "🧥", "👖", "👟", "🎽"]

def configurar_openai():
    """
    Acá configuramos OpenAI. Si no tenés API key, no te preocupes,
    te explico cómo conseguir una gratis.
    """
    try:
        # Primero intentamos con variable de entorno
        api_key = os.getenv("OPENAI_API_KEY")
        
        # Si no hay variable de entorno, usamos session_state para mantener la key
        if not api_key:
            if 'api_key' not in st.session_state:
                st.session_state.api_key = ""
            
            with st.sidebar:
                st.markdown("### 🔑 Necesitás una API Key")
                st.markdown("""
                **¿No tenés una?** No pasa nada:
                1. Andá a [OpenAI](https://platform.openai.com)
                2. Creá una cuenta (es gratis)
                3. Pedí tu API key
                4. Pegala acá abajo 👇
                """)
                
                # Acá está el fix principal: key único y usando session_state
                api_key_input = st.text_input(
                    "Tu API Key:", 
                    type="password",
                    placeholder="sk-...",
                    value=st.session_state.api_key,
                    key="openai_api_key_input"  # Key único para evitar conflictos
                )
                
                # Guardamos en session_state para que persista
                if api_key_input:
                    st.session_state.api_key = api_key_input
                    api_key = api_key_input
        
        if api_key:
            openai.api_key = api_key
            return True
        return False
        
    except Exception as e:
        st.error(f"Uh, algo salió mal: {str(e)}")
        return False

def obtener_respuesta_ia(consulta_cliente):
    """
    Acá es donde pasa la magia. Le preguntamos a la IA y esperamos
    que nos dé una respuesta que no suene a manual de instrucciones.
    """
    try:
        # Este prompt lo escribí pensando en cómo habla mi primo que tiene local
        prompt_sistema = """
        Sos Martín, tenés 35 años y hace 8 años que tenés una tienda de ropa en el centro. 
        Empezaste vendiendo en ferias y ahora tenés tu local. Conocés a tus clientes, 
        sabés qué les gusta y siempre tratás de ayudar.
        
        Tu forma de ser:
        - Hablás natural, como habla cualquier argentino
        - Sos honesto: si algo no lo sabés, lo decís
        - Te gusta hacer sentir cómodo al cliente
        - No usás palabras rebuscadas ni frases de marketing
        - Si alguien pregunta algo raro, lo tomás con humor
        
        Tu tienda:
        - Vendés ropa para toda la familia (desde bebés hasta abuelos)
        - Los envíos los hacés por moto, llegan en 1 o 2 días máximo
        - Si algo no les gusta, lo pueden cambiar tranquilos (30 días)
        - Abrís todos los días: lunes a sábado hasta las 8, domingos hasta las 6
        - Aceptás de todo: efectivo, tarjeta, transferencia, hasta Mercado Pago
        - Los clientes que vienen seguido tienen descuentos (porque vos los conocés)
        
        Importante: Respondé como si fueras realmente Martín hablando con un cliente.
        Nada de "estimado cliente" ni boludeces así. Hablá normal.
        """
        
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": consulta_cliente}
            ],
            max_tokens=400,
            temperature=0.9  # Bien creativo para que suene natural
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Perdón, se me colgó el sistema. Probá de nuevo en un ratito. (Error técnico: {str(e)})"

def main():
    # Inicializamos session_state para evitar problemas
    if 'respuesta_generada' not in st.session_state:
        st.session_state.respuesta_generada = False
    
    # Header con un poco más de onda
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🏪 MiVendedor.AI")
        st.markdown("*El vendedor que nunca se toma franco*")
    with col2:
        st.markdown(f"### {random.choice(EMOJIS_RANDOM)}")
    
    st.markdown("---")
    
    # Intro más personal
    st.markdown("""
    ### Hola! 👋 
    
    Te cuento qué onda con esto: hice esta aplicación porque me cansé de ver tiendas 
    que pierden clientes por no poder atender consultas fuera del horario. 
    
    **La idea es simple:** vos ponés una pregunta como si fueras un cliente, y la app 
    te devuelve una respuesta que podría dar cualquier buen vendedor. Nada de respuestas 
    robóticas ni frases hechas.
    
    Es perfecta para:
    - Probar cómo sonaría tu atención automática
    - Entrenar empleados nuevos  
    - Tener respuestas listas para las preguntas más comunes
    """)
    
    # Sidebar más relajado
    with st.sidebar:
        st.markdown("### 🤓 Datos técnicos")
        st.markdown("""
        **Proyecto final para:** Curso de IA  
        **Hecho con:** Python + Streamlit + OpenAI  
        **Tiempo invertido:** Demasiado (pero valió la pena)  
        **Cafés consumidos:** No preguntes  
        """)
        
        st.markdown("### ⚙️ Configuración")
        api_ok = configurar_openai()
        
        if api_ok:
            st.success("✅ Conectado y listo")
        else:
            st.info("👆 Configurá tu API key para empezar")
        
        st.markdown("### 🎯 Tips")
        st.markdown("""
        - Preguntá como si fueras un cliente real
        - Probá preguntas raras a ver qué pasa
        - Fijate si las respuestas suenan naturales
        """)
    
    # Sección principal con más onda
    st.markdown("## 💬 Hacé tu consulta")
    
    # Algunos ejemplos que se ven más reales
    with st.expander("🤔 ¿No sabés qué preguntar? Acá tenés ideas"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Preguntas típicas:**
            - ¿Tienen ropa de trabajo?
            - ¿Hacen descuentos por cantidad?
            - ¿Puedo apartar algo hasta el viernes?
            - ¿Tienen local físico o solo online?
            """)
        with col2:
            st.markdown("""
            **Preguntas más específicas:**
            - ¿Qué onda con los talles? ¿Vienen grandes?
            - ¿Si compro hoy, cuándo me llega?
            - ¿Tienen ropa para ir a un casamiento?
            - ¿Aceptan tarjeta de débito?
            """)
    
    # Campo de consulta - SEGUNDO FIX: key único para el text_area
    consulta = st.text_area(
        "Escribí tu consulta acá:",
        placeholder="Ej: Hola, ¿tienen camperas de cuero? Necesito una para mi novio que es medio gordito...",
        height=100,
        help="Escribí como le hablarías a cualquier vendedor",
        key="consulta_cliente_input"  # Key único para evitar conflictos
    )
    
    # Botón con un poco más de personalidad
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # TERCER FIX: key único para el botón
        if st.button(
            "🚀 Ver qué me responde Martín", 
            type="primary", 
            use_container_width=True,
            key="generar_respuesta_btn"
        ):
            if not consulta.strip():
                st.warning("⚠️ Escribí algo primero, no soy adivino 😅")
            elif not configurar_openai():
                st.error("❌ Necesito que configures la API key primero")
            else:
                # Loading con frases random
                frase_loading = random.choice(FRASES_CARGANDO)
                with st.spinner(frase_loading):
                    # Un poquito de delay para que se sienta más real
                    time.sleep(random.uniform(1, 2))
                    respuesta = obtener_respuesta_ia(consulta)
                
                # Guardamos la respuesta en session_state
                st.session_state.respuesta_generada = True
                st.session_state.ultima_respuesta = respuesta
                st.session_state.timestamp = datetime.now()
    
    # Mostrar respuesta si existe (CUARTO FIX: evitar regenerar en cada refresh)
    if st.session_state.respuesta_generada and 'ultima_respuesta' in st.session_state:
        st.success("✅ Listo, acá tenés la respuesta:")
        
        # La respuesta en un formato más lindo
        st.markdown("### 💬 Martín te responde:")
        
        # Un container más estilizado
        with st.container():
            st.markdown(f"""
            <div style="
                background-color: #f0f2f6; 
                padding: 20px; 
                border-radius: 10px; 
                border-left: 4px solid #1f77b4;
                margin: 10px 0;
            ">
                <p style="margin: 0; font-size: 16px; line-height: 1.6;">
                    {st.session_state.ultima_respuesta}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Info adicional más casual
        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"📅 Generado: {st.session_state.timestamp.strftime('%d/%m/%Y a las %H:%M')}")
        with col2:
            # QUINTO FIX: key único para el botón de like
            if st.button("👍 Me gustó la respuesta", key="like_respuesta_btn"):
                st.balloons()
                st.success("¡Genial! Me alegra que te haya servido")
    
    # Sección explicativa pero más divertida
    st.markdown("---")
    st.markdown("## 🤖 ¿Cómo funciona esta cosa?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 1️⃣ Vos preguntás
        Escribís lo que se te ocurra, como si estuvieras en el local hablando con el vendedor.
        """)
    
    with col2:
        st.markdown("""
        ### 2️⃣ La IA labura
        OpenAI (la misma tecnología de ChatGPT) procesa tu pregunta y piensa una respuesta.
        """)
    
    with col3:
        st.markdown("""
        ### 3️⃣ Martín responde
        Te devuelve una respuesta como si fuera un vendedor real con experiencia.
        """)
    
    # Una sección más personal sobre el proyecto
    st.markdown("---")
    st.markdown("## 🎓 Sobre este proyecto")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        Este es mi proyecto final para el curso de Inteligencia Artificial. La idea surgió 
        porque tengo varios amigos con locales que siempre se quejan de lo mismo: "pierdo 
        ventas porque no puedo atender WhatsApp todo el día".
        
        **¿Por qué "Martín"?** Porque necesitaba que el vendedor virtual tuviera personalidad. 
        Martín está basado en un amigo que tiene local y es el tipo más natural vendiendo que conozco.
        
        **¿Funciona bien?** Probalo vos mismo. A mí me sorprendió lo natural que suenan las respuestas.
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Stats del proyecto
        - **Líneas de código:** ~250
        - **Horas invertidas:** Muchas
        - **Versiones probadas:** 20+
        - **Nivel de satisfacción:** 😊
        """)
    
    # Footer más humano
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 30px;'>
        <p>🚀 <strong>Hecho con Python, Streamlit y mucha paciencia</strong></p>
        <p>Si te gustó o tenés alguna sugerencia, me encantaría saberlo</p>
        <p><em>Porque la tecnología tiene que hacer la vida más fácil, no más complicada</em></p>
        <br>
        <p style='font-size: 12px;'>
            💡 <strong>Tip:</strong> Si querés usar esto en tu negocio real, 
            solo tenés que cambiar la info de Martín por la tuya en el código
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
