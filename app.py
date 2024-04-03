from flask import Flask, render_template, url_for, request
import sqlite3
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    db = db_class()
    messages = db.messages() 
    return render_template('index.html',messages=messages)


class db_class:
    def messages(self, start_index=1, num_rows=20):
        with sqlite3.connect('blog.db') as conn:
            cursor = conn.cursor()       
            cursor.execute("SELECT * FROM messages LIMIT ? OFFSET ?", (num_rows, start_index - 1))  
            messages = cursor.fetchall()
            cursor.close()
        
        return messages
   



