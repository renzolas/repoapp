import streamlit as st

# Título de la app
st.title("Sistema de Reserva de Canchas Deportivas")

# Crear un formulario de login
st.header("Iniciar sesión")

# Inputs para usuario y contraseña
username = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")

# Validación básica de login
if st.button("Iniciar sesión"):
    if username == "admin" and password == "admin":
        st.success("¡Bienvenido Admin!")
    elif username != "" and password != "":
        st.success("¡Bienvenido Usuario!")
    else:
        st.error("Usuario o Contraseña Incorrectos.")

# Mostrar canchas disponibles (sólo si está logueado)
if username == "admin" or username == "user":
    st.header("Canchas Disponibles")
    courts = [
        {"name": "Cancha 1", "type": "Fútbol", "available_hours": "09:00, 10:00, 11:00"},
        {"name": "Cancha 2", "type": "Tenis", "available_hours": "14:00, 15:00, 16:00"},
        {"name": "Cancha 3", "type": "Pádel", "available_hours": "17:00, 18:00, 19:00"}
    ]
    
    for court in courts:
        st.subheader(f"Cancha: {court['name']}")
        st.write(f"Tipo: {court['type']}")
        st.write(f"Horarios disponibles: {court['available_hours']}")

