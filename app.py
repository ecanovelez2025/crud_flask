import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os

app = Flask(__name__)


# Configurar desde variables de entorno
app.config['MYSQL_HOST'] = os.getenv('MYSQLHOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQLUSER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQLPASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQLDATABASE', 'railway')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQLPORT', 3306))

mysql = MySQL(app)

# 📋 Mostrar todos los usuarios
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', users=data)

# ➕ Formulario para agregar usuario
@app.route('/add')
def add():
    return render_template('add.html')

# 💾 Guardar usuario
@app.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        mysql.connection.commit()
        return redirect(url_for('index'))

# ✏️ Editar usuario
@app.route('/edit/<id>')
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    data = cur.fetchone()
    cur.close()
    return render_template('edit.html', user=data)

# 🔄 Actualizar usuario
@app.route('/update/<id>', methods=['POST'])
def update(id):
    name = request.form['name']
    email = request.form['email']
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE users
        SET name=%s, email=%s
        WHERE id=%s
    """, (name, email, id))
    mysql.connection.commit()
    return redirect(url_for('index'))

# ❌ Eliminar usuario
@app.route('/delete/<id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


