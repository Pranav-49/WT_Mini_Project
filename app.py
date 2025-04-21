from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import config

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = pyodbc.connect(
        f"DRIVER={config.DRIVER};"
        f"SERVER={config.SERVER};"
        f"DATABASE={config.DATABASE};"
        f"Trusted_Connection={config.TRUSTED_CONNECTION};"
    )
    return conn

# Home route - Display customers
@app.route('/')
def index():
    search = request.args.get('search', '')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if search:
            cursor.execute("SELECT * FROM customers WHERE name LIKE ? OR vehicle LIKE ?", 
                           (f'%{search}%', f'%{search}%'))
        else:
            cursor.execute("SELECT * FROM customers")
        data = cursor.fetchall()
        conn.close()
        return render_template('index.html', customers=data)
    except Exception as e:
        return f"<h1>Database Error</h1><p>{e}</p>"

# Add customer route
@app.route('/add_customer.html', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        vehicle = request.form['vehicle']
        contact = request.form['contact']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO customers (name, vehicle, contact) VALUES (?, ?, ?)", 
                           (name, vehicle, contact))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        except Exception as e:
            return f"<h1>Database Error</h1><p>{e}</p>"
    return render_template('add_customer.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        vehicle = request.form['vehicle']
        contact = request.form['contact']
        try:
            cursor.execute("UPDATE customers SET name = ?, vehicle = ?, contact = ? WHERE id = ?",
                           (name, vehicle, contact, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        except Exception as e:
            return f"<h1>Database Error</h1><p>{e}</p>"

    cursor.execute("SELECT * FROM customers WHERE id = ?", (id,))
    customer = cursor.fetchone()
    conn.close()
    if customer:
        return render_template('edit_customer.html', customer=customer)
    else:
        return "<h1>Customer Not Found</h1>"

# Delete customer route
@app.route('/delete/<int:id>')
def delete_customer(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        return f"<h1>Database Error</h1><p>{e}</p>"

if __name__ == '__main__':
    app.run(debug=True)