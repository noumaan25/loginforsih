from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            return "Login successful!"
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('User created successfully!')
        except sqlite3.IntegrityError:
            flash('Username already exists.')
        finally:
            conn.close()

        return redirect(url_for('login'))

    return render_template('new_user.html')

if __name__ == '__main__':
    app.run(debug=True)
