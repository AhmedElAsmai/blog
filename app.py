from flask import Flask, render_template, url_for, request, redirect
import sqlite3
import datetime

logged_in = True                                                        #[DEBUG]   LOG IN!!!!!!!
current_user = 'test'              #[DEBUG] turn off when debug off
app = Flask(__name__)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    global logged_in

    if logged_in == True:
        date = db.current_datetime()
        if request.method == 'POST':
            if 'date' in request.form:    
                date = request.form['date']
                messages = db.messages(date) 
                return render_template('index.html', messages=messages, date=date)
            
            if 'chatbox' in request.form:
                chat = request.form['chatbox']
                db.chatbox(chat)

        messages = db.messages(date)
        return render_template('index.html',messages=messages, date= date)
    return redirect('/login')

@app.route('/login',methods=['GET', 'POST'])
def login():
    global logged_in
    global current_user
    logged_in = False                                          
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        authentication = db.authentication(username, password)
        
        if authentication:
            logged_in = True
            current_user = username
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

#DB CLASS


class db_class:
    def messages(self, date):
        with sqlite3.connect('blog.db') as conn:
            cursor = conn.cursor()       
            cursor.execute(f"SELECT * FROM messages WHERE time < '{str(date)}' ORDER BY time DESC")
            messages = list(reversed(cursor.fetchall()))
            cursor.close()
            print(messages)
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

    def current_datetime(self):
        timestamp = datetime.datetime.now()
        self.formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S') #formats the date for SQL
        return self.formatted_timestamp

    def chatbox(self, chat):
        with sqlite3.connect('blog.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO messages (username, message, time) VALUES (?, ?, ?)", (current_user, chat, self.formatted_timestamp))
            conn.commit()
            cursor.close() 
        
        
db = db_class()



