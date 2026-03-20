from flask import Flask, request, jsonify, render_template, redirect
from db import get_connection

app = Flask(__name__)

# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')

# GET TASKS
@app.route('/tasks')
def get_tasks():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    return jsonify(tasks)

# ADD TASK
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks(title, description) VALUES (%s, %s)", (title, description))
    conn.commit()

    return redirect('/')

# DELETE TASK
@app.route('/delete')
def delete():
    id = request.args.get('id')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=%s", (id,))
    conn.commit()

    return "Deleted"

# COMPLETE TASK
@app.route('/complete')
def complete():
    id = request.args.get('id')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET status='COMPLETED' WHERE id=%s", (id,))
    conn.commit()

    return "Updated"

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)