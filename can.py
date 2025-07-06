import streamlit as st
import time

# Título de la app
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Reserva de Canchas</h1>", unsafe_allow_html=True)

# Encabezado con formato atractivo
st.markdown("<h3 style='text-align: center; color: #FF5733;'>¡Bienvenido al sistema de reservas!</h3>", unsafe_allow_html=True)

# Inicializar session_state
if "intentos" not in st.session_state:
    st.session_state.intentos = 0  # Inicializamos los intentos
if "bloqueado" not in st.session_state:
    st.session_state.bloqueado = False  # Inicializamos el bloqueo
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False  # Mantener el estado de login

# Función para mostrar el login
def login():
    st.header("Iniciar sesión")

    # Selección de perfil con botones de opción
    perfil = st.radio("Selecciona tu perfil", ["Usuario", "Administrador"])

    # Inputs para usuario y contraseña con estilo
    username = st.text_input("Usuario", placeholder="Ingresa tu nombre de usuario").lower()  # Convertimos el input a minúsculas
    password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")

    # Credenciales para cada perfil
    usuarios = {
        "user": "1234",  # Usuario normal
        "admin": "1234"  # Admin
    }

    # Validación de login según el perfil seleccionado
    if st.button("Iniciar sesión"):
        if st.session_state.intentos >= 3:
            st.warning("Has alcanzado el límite de intentos fallidos. Por favor espera 1 minuto.")
            st.session_state.bloqueado = True
            time.sleep(60)  # Espera 1 minuto
            st.session_state.intentos = 0  # Reiniciar intentos después de bloquear
            st.session_state.bloqueado = False  # Desbloqueamos
            return
        if perfil == "Usuario" and username == "user" and password == usuarios["user"]:
            st.success("¡Bienvenido Usuario!")
            st.session_state.logged_in = True
            st.session_state.intentos = 0  # Reseteamos los intentos
        elif perfil == "Administrador" and username == "admin" and password == usuarios["admin"]:
            st.success("¡Bienvenido Administrador!")
            st.session_state.logged_in = True
            st.session_state.intentos = 0  # Reseteamos los intentos
        else:
            st.error("Usuario o Contraseña Incorrectos.")
            st.session_state.intentos += 1  # Aumentamos el contador de intentos

# Función para seleccionar deporte
def select_deporte():
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

    # Colocar el botón de "Cerrar sesión" al final de esta página
    if st.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.session_state.intentos = 0  # Resetear intentos cuando se cierre sesión
        st.success("Has cerrado sesión exitosamente")

# Función principal
def main():
    # Si el usuario no está logueado, mostrar el login
    if not st.session_state.logged_in:
        login()
    else:
        # Si el usuario está logueado, mostrar la página de selección de deporte
        select_deporte()

# Ejecutar la aplicación
main()
