from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Konfigurasi koneksi ke MySQL
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # Ganti dengan username MySQL-mu
        password='',  # Ganti dengan password MySQL-mu
        database='flask_crud'
    )

# Route untuk menampilkan semua pengguna
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', users=users)

# Route untuk menambahkan pengguna baru
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
    return render_template('add_user.html')

# Route untuk mengupdate informasi pengguna
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = cursor.fetchone()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cursor.execute('UPDATE users SET name = %s, email = %s WHERE id = %s', (name, email, id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))

    cursor.close()
    connection.close()
    return render_template('update_user.html', user=user)

# Route untuk menghapus pengguna
@app.route('/delete/<int:id>', methods=['GET'])
def delete_user(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
