from flask import Flask, render_template, url_for, request, redirect
import sqlite3

logged_in = False                                                           #LOG IN!!!!!!!

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    if logged_in == True:
        messages = db.messages() 
        return render_template('index.html',messages=messages)
    return redirect('/login')

@app.route('/login',methods=['GET', 'POST'])
def login():
    global logged_in
    logged_in = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        authentication = db.authentication(username, password)
        
        if authentication:
            logged_in = True
            return redirect('/index')
    return render_template('login.html')


@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if db.registration(username, password):
            return redirect('/login')
    return render_template('register.html')

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
    
    def registration(self, username, password):
        with sqlite3.connect('blog.db') as conn:
            cursor = conn.cursor()       
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()[0]
            if existing_user > 0:
                return False
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            cursor.close()       
            return True
        

        

db = db_class()



