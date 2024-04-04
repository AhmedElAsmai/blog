from flask import Flask, render_template, url_for, request, redirect
import sqlite3
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    messages = db.messages() 
    return render_template('index.html',messages=messages)

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        authentication = db.authentication(username, password)
        
        if authentication:
            return redirect('/index')
    return render_template('login.html')

# @app.route('/register')
# def register():
#     return render_template('register.html')

class db_class:
    def messages(self, start_index=1, num_rows=20):
        
        with sqlite3.connect('blog.db') as conn:
            cursor = conn.cursor()       
            cursor.execute("SELECT * FROM messages LIMIT ? OFFSET ?", (num_rows, start_index - 1))  
            messages = cursor.fetchall()
            cursor.close()
        
        return messages
    
    def authentication(self, username, password):
        with sqlite3.connect('blog.db') as conn:
            cursor = conn.cursor()       
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))  
            user = cursor.fetchone()
            cursor.close()       

        return user
        

db = db_class()



