from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2  # pip install psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "Vanesa_Riaño"

DB_HOST = "localhost"
DB_NAME = "MOCK_DATA"
DB_USER = "postgres"
DB_PASS = "123456V"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST)


@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT gender, COUNT(gender) FROM mock_data GROUP BY gender ORDER BY gender ASC"
    cur.execute(s)  # Execute the SQL
    list_users = cur.fetchall()
    return render_template('index.html', list_users=list_users)

@app.route('/')
def Index1():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT gender, COUNT(gender) FROM mock_data GROUP BY gender ORDER BY gender ASC"
    cur.execute(s)  # Execute the SQL
    list_users = cur.fetchall()
    return render_template('index.html', list_users=list_users)

@app.route('/add_student', methods=['POST'])
def add_student():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        gender = request.form['gender']

        cur.execute("INSERT INTO mock_data ( first_name, last_name, email, gender) VALUES (%s,%s,%s,%s)",
                    (first_name, last_name, email, gender))
        conn.commit()
        flash('Estudiante registrado correctamente')
        return redirect(url_for('Index'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT * FROM mock_data WHERE id = {0}' .format(id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', student=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_student(id):
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        gender = request.form['gender']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE mock_data
            SET first_name = %s,
                last_name = %s,
                email = %s,
                gender = %s
            WHERE id = %s
        """, (first_name, last_name, email, gender, id))
        flash('Estudiante actualizado correctamente')
        conn.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('DELETE FROM mock_data WHERE id = {0}'.format(id))
    conn.commit()
    flash('Estudiante eliminado correctamente')
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
