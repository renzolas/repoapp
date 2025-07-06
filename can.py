import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Configuración
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelos de Base de Datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    tipo_usuario = db.Column(db.String(10), nullable=False)  # admin o usuario

class Deporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

class Cancha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    id_deporte = db.Column(db.Integer, db.ForeignKey('deporte.id'), nullable=False)
    deporte = db.relationship('Deporte', backref=db.backref('canchas', lazy=True))

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_cancha = db.Column(db.Integer, db.ForeignKey('cancha.id'), nullable=False)
    fecha_reserva = db.Column(db.String(50), nullable=False)
    hora_reserva = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(10), default='confirmada')  # confirmada o cancelada

# Función para cargar usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Rutas
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.contraseña, contraseña):
            login_user(usuario)
            return redirect(url_for('select_sport'))
        else:
            flash("Credenciales inválidas", 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/select_sport', methods=['GET', 'POST'])
@login_required
def select_sport():
    if request.method == 'POST':
        deporte_id = request.form['deporte']
        return redirect(url_for('select_court', deporte_id=deporte_id))

    deportes = Deporte.query.all()
    return render_template('select_sport.html', deportes=deportes)

@app.route('/select_court/<int:deporte_id>', methods=['GET', 'POST'])
@login_required
def select_court(deporte_id):
    if request.method == 'POST':
        cancha_id = request.form['cancha']
        fecha_reserva = request.form['fecha']
        hora_reserva = request.form['hora']
        
        reserva = Reserva(id_usuario=current_user.id, id_cancha=cancha_id,
                          fecha_reserva=fecha_reserva, hora_reserva=hora_reserva)
        db.session.add(reserva)
        db.session.commit()
        flash('Reserva confirmada', 'success')
        return redirect(url_for('dashboard'))

    canchas = Cancha.query.filter_by(id_deporte=deporte_id).all()
    return render_template('select_court.html', canchas=canchas)

@app.route('/dashboard')
@login_required
def dashboard():
    reservas = Reserva.query.filter_by(id_usuario=current_user.id).all()
    return render_template('dashboard.html', reservas=reservas)

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)

# Archivos de plantillas HTML

html_login = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h2>Iniciar sesión</h2>
    <form action="/login" method="POST">
        <label for="email">Correo electrónico:</label>
        <input type="email" name="email" required><br><br>
        <label for="contraseña">Contraseña:</label>
        <input type="password" name="contraseña" required><br><br>
        <button type="submit">Iniciar sesión</button>
    </form>
    <p><a href="#">Olvidé mi contraseña</a></p>
</body>
</html>
"""

html_select_sport = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Selecciona un deporte</title>
</head>
<body>
    <h2>Selecciona un deporte</h2>
    <form action="/select_sport" method="POST">
        {% for deporte in deportes %}
            <button type="submit" name="deporte" value="{{ deporte.id }}">{{ deporte.nombre }}</button><br><br>
        {% endfor %}
    </form>
</body>
</html>
"""

html_select_court = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Selecciona una cancha</title>
</head>
<body>
    <h2>Selecciona una cancha</h2>
    <form action="/select_court/{{ deporte_id }}" method="POST">
        {% for cancha in canchas %}
            <button type="submit" name="cancha" value="{{ cancha.id }}">{{ cancha.nombre }} - {{ cancha.direccion }}</button><br><br>
        {% endfor %}
        <input type="date" name="fecha" required>
        <input type="time" name="hora" required><br><br>
        <button type="submit">Reservar</button>
    </form>
</body>
</html>
"""

html_dashboard = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mis Reservas</title>
</head>
<body>
    <h2>Mis Reservas</h2>
    <table>
        <tr>
            <th>Cancha</th>
            <th>Fecha</th>
            <th>Hora</th>
            <th>Estado</th>
        </tr>
        {% for reserva in reservas %}
            <tr>
                <td>{{ reserva.cancha.nombre }}</td>
                <td>{{ reserva.fecha_reserva }}</td>
                <td>{{ reserva.hora_reserva }}</td>
                <td>{{ reserva.estado }}</td>
            </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

