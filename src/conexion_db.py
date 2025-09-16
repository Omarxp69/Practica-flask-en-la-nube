import mysql.connector
import os

# def get_connection():
#     conexion = mysql.connector.connect(
#     host="localhost",
#     user='root',
#     password='Guada_xp69@3',
#     database="pythonflask"
#     )
#     return conexion

# def get_connection():
#     conexion = mysql.connector.connect(
#     host="crossover.proxy.rlwy.net",
#     user='root',
#     password='gXzKWOUKgRfhZPechGJvDRfjikESKknh',
#     database="railway",
#     port=57103
#     )
#     return conexion

conexion = mysql.connector.connect(
    host=os.environ.get('MYSQLHOST'),
    user=os.environ.get('MYSQLUSER'),
    password=os.environ.get('MYSQLPASSWORD'),
    database=os.environ.get('MYSQLDATABASE'),
    port=int(os.environ.get('MYSQLPORT', 3306))
)




def insertar_usuario(username, name, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users(username, name, password) VALUES (%s, %s, %s)",
        (username, name, password)
    )
    conn.commit()
    cursor.close()
    conn.close()

def obtener_todos_usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    registros = cursor.fetchall()
    cursor.close()
    conn.close()
    return registros

def obtener_usuario_por_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user











