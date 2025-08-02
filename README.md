.
---

````markdown
# 🏪 MiVendedor.AI

**MiVendedor.AI** es una app web hecha con **Python, Streamlit y OpenAI**, que simula a un vendedor real atendiendo consultas de clientes de forma natural, clara y con buena onda.

Fue desarrollada como parte del proyecto final del curso de Inteligencia Artificial, buscando aplicar los conocimientos del curso en una solución útil para situaciones reales.

---

## 🎯 ¿Para qué sirve?

La app está pensada para locales o negocios que quieren automatizar las respuestas a consultas típicas de los clientes (horarios, envíos, talles, formas de pago, etc.), pero **sin sonar robóticos** ni usar frases genéricas.

Vos escribís una consulta como si fueras un cliente, y la app responde como lo haría un vendedor de verdad. Esa es la idea: algo simple, directo y funcional.

---

## 👔 ¿Quién responde?

El que responde es **Martín**, un vendedor virtual con experiencia, que habla como cualquier persona en un local real: con naturalidad, claridad y respeto.

Fue pensado para sonar como alguien de confianza, que conoce bien su negocio y a sus clientes.

---

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **Streamlit** para la interfaz web
- **OpenAI (GPT-3.5-Turbo)** para generar las respuestas
- **dotenv** para manejar la clave de API

---

## 🚀 ¿Cómo se usa?

1. Cloná este repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/ginoskl-streamlit-ai-support.git
   cd ginoskl-streamlit-ai-support
````

2. Instalá las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutá la app:

   ```bash
   streamlit run scripts/streamlit_app.py
   ```

4. Ingresá tu [API Key de OpenAI](https://platform.openai.com/account/api-keys) cuando te lo pida, y empezá a probar.

---

## 🌐 Link a la app online

(Completá este link cuando la tengas publicada en Streamlit Cloud)

📎 [https://tuvendedor.streamlit.app](https://tuvendedor.streamlit.app)

---

## 📁 Estructura del proyecto

```
ginoskl-streamlit-ai-support/
├── requirements.txt
└── scripts/
    ├── config.py
    ├── config_personalizada.py
    └── streamlit_app.py
```

* `config.py`: configuración general del negocio
* `config_personalizada.py`: permite personalizar al vendedor y su tienda
* `streamlit_app.py`: archivo principal de la app

---

## ✏️ ¿Se puede adaptar?

Sí. Todo está pensado para que lo puedas modificar fácil.
Podés cambiar:

* El nombre del vendedor
* Cómo habla
* Qué productos ofrece
* Los datos del local

Todo eso está separado en archivos de configuración para que no tengas que tocar el código principal.

---

## 🤖 ¿Por qué hice esto?

Porque me pareció una buena forma de mostrar cómo la inteligencia artificial puede resolver un problema concreto: responder bien y rápido sin perder el trato humano.
La mayoría de los chats automáticos no suenan reales. Esto busca cambiar eso.

---

## 👤 Autor

Proyecto final realizado por **Gino Lionel Zampierón**
Curso de Inteligencia Artificial — 2025

---

```
