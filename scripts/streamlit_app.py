import streamlit as st
import openai
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Atención al Cliente con IA - Tu Asistente Virtual",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para inicializar la API de OpenAI
def configurar_openai():
    """
    Configura la conexión con OpenAI.
    Si no tenés la API key como variable de entorno, podés ingresarla acá.
    """
    try:
        # Primero busca la API key en las variables de entorno
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            # Si no la encuentra, permite ingresarla en la barra lateral
            api_key = st.sidebar.text_input(
                "Ingresá tu API Key de OpenAI:", 
                type="password",
                help="Podés conseguir tu API key gratis en https://platform.openai.com/api-keys"
            )
        
        if api_key:
            openai.api_key = api_key
            return True
        return False
    except Exception as e:
        st.error(f"Ups, hubo un problema al configurar OpenAI: {str(e)}")
        return False

# Función para generar respuesta con IA
def obtener_respuesta_ia(consulta_cliente):
    """
    Le manda la consulta del cliente a GPT y trae la respuesta.
    
    Args:
        consulta_cliente (str): Lo que escribió el cliente
    
    Returns:
        str: La respuesta que generó la IA
    """
    try:
        # Prompt mejorado y más natural
        prompt_sistema = """
        Sos un vendedor experimentado de una tienda de ropa que atiende clientes hace años. 
        
        Tu personalidad:
        - Amable y cercano, pero siempre profesional
        - Te gusta ayudar y resolver problemas
        - Conocés bien los productos y la tienda
        - Hablás de manera natural, como cualquier vendedor argentino
        
        Información de tu tienda:
        - Vendés ropa para toda la familia: hombres, mujeres y chicos
        - Hacés envíos a domicilio (llegan en 1 o 2 días)
        - Si no les gusta algo, pueden devolverlo hasta 30 días después
        - Abrís de lunes a sábado de 9 a 20hs, domingos de 10 a 18hs
        - Aceptás efectivo, tarjetas y transferencias
        - Tenés un programa de clientes frecuentes con descuentos especiales
        
        Importante: Respondé siempre de manera útil y completa, pero sin sonar robótico. 
        Hablá como hablaría cualquier vendedor amable de Buenos Aires.
        """
        
        # Llamada a la API de OpenAI (versión actualizada)
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": f"Cliente pregunta: {consulta_cliente}"}
            ],
            max_tokens=350,
            temperature=0.8  # Un poco más creativo para sonar más natural
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Disculpá, hubo un problemita técnico y no pude procesar tu consulta. Error: {str(e)}"

# Función principal de la aplicación
def main():
    """
    Acá se arma toda la interfaz de la aplicación
    """
    
    # Título principal
    st.title("🛍️ Tu Asistente Virtual de Atención al Cliente")
    st.markdown("---")
    
    # Descripción más natural
    st.markdown("""
    ### ¿Qué hace esta aplicación?
    
    Imaginate tener un vendedor que nunca se cansa, que siempre está de buen humor y que puede 
    atender a tus clientes las 24 horas. Eso es exactamente lo que hace esta aplicación.
    
    Usamos **Inteligencia Artificial** para que cualquier consulta de tus clientes tenga una 
    respuesta rápida, amable y profesional. Perfecto para negocios que quieren brindar un 
    servicio de primera, sin importar la hora.
    """)
    
    # Barra lateral con info
    with st.sidebar:
        st.header("📋 Info del proyecto")
        st.markdown("""
        **¿Para quién es?**
        - Dueños de tiendas de ropa
        - Pequeños comercios
        - Cualquiera que quiera automatizar la atención
        
        **¿Qué tecnología usa?**
        - Streamlit (interfaz web)
        - OpenAI GPT (la inteligencia artificial)
        - Python (el lenguaje de programación)
        """)
        
        # Configuración de API
        st.header("⚙️ Configuración")
        api_ok = configurar_openai()
        
        if api_ok:
            st.success("✅ Todo listo para usar")
        else:
            st.warning("⚠️ Necesitás configurar tu API key para empezar")
    
    # Sección principal donde el usuario hace la consulta
    st.header("💬 Probá hacer una consulta")
    st.markdown("Escribí cualquier pregunta como si fueras un cliente de la tienda:")
    
    # Campo de texto para la consulta
    consulta = st.text_area(
        "Tu consulta:",
        placeholder="Por ejemplo: ¿Hacen envíos gratis? ¿Tienen talles grandes? ¿Puedo cambiar algo si no me queda bien?",
        height=120,
        help="Escribí lo que se te ocurra, como si estuvieras hablando con un vendedor"
    )
    
    # Botón para procesar - más centrado y llamativo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generar_respuesta = st.button(
            "🚀 Obtener respuesta automática", 
            type="primary",
            use_container_width=True
        )
    
    # Acá se procesa todo cuando aprietan el botón
    if generar_respuesta:
        if not consulta.strip():
            st.warning("⚠️ Escribí algo primero para que pueda ayudarte.")
        elif not configurar_openai():
            st.error("❌ Primero configurá tu API key en la barra lateral.")
        else:
            # Mostrar que está trabajando
            with st.spinner("🤖 Pensando la mejor respuesta..."):
                respuesta = obtener_respuesta_ia(consulta)
            
            # Mostrar el resultado
            st.success("✅ ¡Listo! Acá tenés la respuesta:")
            
            # La respuesta en una caja destacada
            st.markdown("### 💬 Respuesta del vendedor virtual:")
            st.info(respuesta)
            
            # Info adicional
            st.markdown(f"**Generado el:** {datetime.now().strftime('%d/%m/%Y a las %H:%M')}")
            
            # Opción para "copiar" (simulada porque Streamlit no puede acceder al portapapeles)
            if st.button("📋 Marcar como útil"):
                st.success("¡Genial! Nos alegra que te haya servido la respuesta")
    
    # Sección explicativa
    st.markdown("---")
    st.header("🤔 ¿Cómo funciona esto?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 1️⃣ Vos preguntás
        Escribís cualquier consulta que haría un cliente real en tu tienda.
        """)
    
    with col2:
        st.markdown("""
        ### 2️⃣ La IA piensa
        El sistema toma tu pregunta y la procesa con inteligencia artificial entrenada para atención al cliente.
        """)
    
    with col3:
        st.markdown("""
        ### 3️⃣ Obtenés la respuesta
        En segundos tenés una respuesta profesional, amable y lista para usar con tus clientes.
        """)
    
    # Sección de ejemplos
    st.markdown("---")
    st.header("💡 Algunos ejemplos para probar")
    
    ejemplos_col1, ejemplos_col2 = st.columns(2)
    
    with ejemplos_col1:
        st.markdown("""
        **Consultas sobre envíos:**
        - "¿Hacen envíos a todo el país?"
        - "¿Cuánto demora en llegar mi pedido?"
        - "¿El envío tiene costo?"
        """)
    
    with ejemplos_col2:
        st.markdown("""
        **Consultas sobre productos:**
        - "¿Tienen ropa para embarazadas?"
        - "¿Qué talles manejan?"
        - "¿Puedo ver fotos de los productos?"
        """)
    
    # Footer más personal
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🎓 <strong>Proyecto Final - Curso de Inteligencia Artificial</strong></p>
        <p>Hecho con mucho ☕ y un poco de IA para hacer la vida más fácil</p>
        <p><em>Porque la tecnología tiene que servir para ayudar a las personas</em></p>
    </div>
    """, unsafe_allow_html=True)

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
