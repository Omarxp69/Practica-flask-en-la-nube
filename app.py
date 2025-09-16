from flask import Flask,render_template,make_response,redirect,request,flash,url_for,session
import bcrypt
from conexion_db import insertar_usuario,obtener_usuario_por_username,obtener_todos_usuarios
from functools import wraps
import os
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))


def role_required(rol):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] != rol:
                flash("❌ Acceso denegado")
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' in session:
            # Si hay sesión iniciada, redirige según rol
            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        return f(*args, **kwargs)
    return decorated_function



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
@logout_required
def raiz():
    return redirect(url_for('login'))

@app.route('/registrar', methods=['GET','POST'])
@logout_required
def registrar():
    if request.method == 'POST':
        username = request.form.get('username')
        nombre = request.form.get('nombre')
        password = request.form.get('password')
        if not username or not nombre or not password:
            flash("❌ Debes llenar todos los campos")
            #print("Faltan datos")
            return redirect(url_for('registrar'))
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        #info_formulario = f"Usuario: {username}, Nombre: {nombre}"
        #usuarios.append(info_formulario)
        insertar_usuario(username, nombre, hashed_password.decode('utf-8'))
        #print(f"Hola {info_formulario}")
        return redirect(url_for('login'))
    return render_template('Entrada.html')

@app.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash("❌ Debes llenar todos los campos")
            print("Faltan datos")
            return redirect(url_for('login'))
        
        user = obtener_usuario_por_username(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['username'] = user[1]  # username
            session['role'] = user[4]      # role
            flash("✅ Login exitoso")
            #print(tuple(user))
            if user[4] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash("❌ Login fallido")
        return redirect(url_for('login'))
    return render_template('login.html')



@app.route('/admin')
@role_required('admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')


@app.route('/user')
@role_required('user')
def user_dashboard():
    return render_template('user_dashboard.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("✅ Has cerrado sesión correctamente")
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


