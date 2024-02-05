from flask import Flask, render_template, request, session,redirect,url_for
import operations, check
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = 'abc12345'
bcrypt = Bcrypt(app)

@app.route('/', methods=['GET','POST'])
def login():
    message= ''
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        obj = operations.db_operations()
        hash_password = obj.confirm_password(email)
        if (bcrypt.check_password_hash(hash_password, password)):
            result = obj.login_user(email, hash_password)
            if result:
                username = obj.get_name(email,hash_password)
                session['username'] = username
                session['loggedin'] = True
                return render_template('main.html', username = session['username'])
            else:
                message = 'User does not exist'
    return render_template('index.html', msg=message)

@app.route('/registration', methods=['GET','POST'])
def registration():
    message = ''
    if request.method=='POST':
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        passowrd2 = request.form.get('second_pass','')
        obj = operations.db_operations()
        ch_obj = check.checks()
        result = ch_obj.check_password(password)
        email_result = obj.email_exists(email)
        if email_result or result =='short' or result == 'incorrect':
            if email_result:
                message= 'Account already registered with this email'
            elif result == 'short':
                message = 'Password should be at least 8 characters long'
            elif result =='incorrect':
                message = 'Password should be combination of numbers and alphabets'
            elif password != passowrd2:
                message = "Passwords do not match"
        else:
            hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
            response = obj.insert_data(username,email,hashed_password)
            if response:
                message='Successfully Registered'
            else:
                message= 'There is something wrong, please try again'
    return render_template('registration.html', msg = message)

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return render_template('index.html')

#home page after logging
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('main.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
