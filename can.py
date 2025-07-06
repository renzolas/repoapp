import streamlit as st

# Título de la app
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Reserva de Canchas</h1>", unsafe_allow_html=True)

# Encabezado con formato atractivo
st.markdown("<h3 style='text-align: center; color: #FF5733;'>¡Bienvenido al sistema de reservas!</h3>", unsafe_allow_html=True)

# Crear un formulario de login
st.header("Iniciar sesión")

# Selector de perfil con botones de opción
perfil = st.radio("Selecciona tu perfil", ["Usuario", "Administrador"])

# Inputs para usuario y contraseña con estilo
username = st.text_input("Usuario", placeholder="Ingresa tu nombre de usuario").lower()  # Convertimos el input a minúsculas
password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")

# Credenciales para cada perfil
usuarios = {
    "user": "1234",  # Usuario normal
    "admin": "1234"  # Admin
}

# Variable para guardar el estado del login
login_successful = False

# Validación de login según el perfil seleccionado
if st.button("Iniciar sesión"):
    # Comprobamos si el usuario y la contraseña son correctos
    if perfil == "Usuario" and username == "user" and password == usuarios["user"]:
        st.success("¡Bienvenido Usuario!")
        login_successful = True
    elif perfil == "Administrador" and username == "admin" and password == usuarios["admin"]:
        st.success("¡Bienvenido Administrador!")
        login_successful = True
    else:
        st.error("Usuario o Contraseña Incorrectos.")
        # Limpiar los campos de texto para que el usuario pueda ingresar de nuevo
        username = st.text_input("Usuario", placeholder="Ingresa tu nombre de usuario", key="username")
        password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", key="password")

# Redirigir a una página interna para el Usuario (si está logueado)
if login_successful and perfil == "Usuario":
    # Página interna de selección de deporte para el Usuario
    st.subheader("Selecciona tu deporte")

    deporte = st.selectbox("Selecciona tu deporte", ["Fútbol", "Tenis", "Pádel"], index=0)

    # Lógica para mostrar las canchas según el deporte seleccionado
    if deporte == "Fútbol":
        st.header("Canchas de Fútbol Disponibles")
        courts = [
            {"name": "Cancha de Fútbol 1", "available_hours": "09:00, 10:00, 11:00"},
            {"name": "Cancha de Fútbol 2", "available_hours": "12:00, 13:00, 14:00"}
        ]
    elif deporte == "Tenis":
        st.header("Canchas de Tenis Disponibles")
        courts = [
            {"name": "Cancha de Tenis 1", "available_hours": "15:00, 16:00, 17:00"},
            {"name": "Cancha de Tenis 2", "available_hours": "18:00, 19:00, 20:00"}
        ]
    elif deporte == "Pádel":
        st.header("Canchas de Pádel Disponibles")
        courts = [
            {"name": "Cancha de Pádel 1", "available_hours": "09:00, 10:00, 11:00"},
            {"name": "Cancha de Pádel 2", "available_hours": "14:00, 15:00, 16:00"}
        ]
    
    # Mostrar las canchas disponibles según el deporte seleccionado
    for court in courts:
        st.subheader(f"Cancha: {court['name']}")
        st.write(f"Horarios disponibles: {court['available_hours']}")
