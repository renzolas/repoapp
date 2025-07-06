import streamlit as st
from PIL import Image

# Título de la app
st.title("Sistema de Reserva de Canchas Deportivas")

# Agregar imagen de fondo
img = Image.open("fondo.jpg")  # Asegúrate de tener la imagen en la carpeta de tu proyecto
st.image(img, use_column_width=True)

# Encabezado con un diseño bonito
st.markdown("<h2 style='text-align: center; color: blue;'>¡Bienvenido al sistema de reservas!</h2>", unsafe_allow_html=True)

# Crear un formulario de login
st.header("Iniciar sesión")

# Selector de perfil con colores
perfil = st.selectbox("Selecciona tu perfil", ["Usuario", "Administrador"], index=0)

# Inputs para usuario y contraseña con estilo
username = st.text_input("Usuario", placeholder="Ingresa tu nombre de usuario")
password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")

# Credenciales para cada perfil
usuarios = {
    "user": "1234",  # Usuario normal
    "admin": "1234"  # Admin
}

# Validación de login según el perfil seleccionado
if st.button("Iniciar sesión"):
    if perfil == "Usuario" and username == "user" and password == usuarios["user"]:
        st.success("¡Bienvenido Usuario!")
        st.write("Puedes ver y reservar las canchas disponibles.")
    elif perfil == "Administrador" and username == "admin" and password == usuarios["admin"]:
        st.success("¡Bienvenido Administrador!")
        st.write("Puedes gestionar las canchas y las reservas.")
    elif username != "" and password != "":
        st.error("Usuario o Contraseña Incorrectos.")
    else:
        st.warning("Por favor ingresa tus credenciales.")

# Mostrar deportes y canchas disponibles (sólo si está logueado como Usuario)
if (username == "user" and password == "1234"):
    # Selección de deporte
    deporte = st.selectbox("Selecciona tu deporte", ["Fútbol", "Tenis", "Pádel"])

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



