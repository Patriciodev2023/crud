from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_mysqldb import MySQL
import os

app = Flask(__name__, template_folder='.')  # Configura la carpeta de plantillas en el mismo directorio
# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'computadoras'

mysql = MySQL(app)
@app.route('/styles.css')
def css():
    return send_from_directory(os.getcwd(), 'styles.css')

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM piezas")
    piezas = cur.fetchall()
    cur.close()
    return render_template('index.html', piezas=piezas)

@app.route('/add', methods=['POST'])
def add():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO piezas (nombre, descripcion, precio, cantidad) VALUES (%s, %s, %s, %s)",
                (nombre, descripcion, precio, cantidad))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM piezas WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE piezas 
        SET nombre = %s, descripcion = %s, precio = %s, cantidad = %s
        WHERE id = %s
    """, (nombre, descripcion, precio, cantidad, id))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
