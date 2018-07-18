from flask import Flask, request, render_template, redirect

app = Flask(__name__)
app.config['DEBUG'] = True

app.username_error = ''
app.password_error = ''
app.password_match = ''
app.email_error = ''
app.LENGTH_ERROR = 'username needs to be between 3 and 20 characters.'

@app.route('/', methods=['POST', 'GET'])
def index():
    if(request.method == 'POST'):
        reset_errors()
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']

        if(valid_username(username) and valid_password(password, verify) and valid_email(email)):
            return redirect('/signedup?username={}'.format(username))
        else:
            return render_template('form.html', username_error=app.username_error,
            password_error=app.password_error, password_match = app.password_match, email_error = app.email_error)
    else:
        return render_template('form.html')


@app.route('/signedup')
def signup():
    username = request.args.get('username')
    return render_template('signedup.html', username=username)


# def login_success(username):
#     if(validate_username(username)):
#         return True
#     return False

def reset_errors():
    app.username_error = ''
    app.password_error = ''
    app.password_match = ''
    app.email_error = ''


def valid_username(username):
    if username and is_string(username):
        username = str(username)
        if is_correct_length(username):
            return True

    app.username_error = app.LENGTH_ERROR
    return False


def valid_password(password, verify):
    print(password, ' == ', verify, password == verify)
    if password and is_string(password):
        password = str(password)
        if is_correct_length(password):
            if password == verify:
                return True
            else:
                app.password_error = 'Passwords do not match!'
                return False

    app.password_error = app.LENGTH_ERROR
    return False

def valid_email(email):
    ''' Must contain a single @, a single dot, no space and is the correct length '''

    if email and is_string(email):
        if is_correct_length(email):
            if '@' in email and '.' in email and not ' ' in email:
                return True
        
    app.email_error = 'Must contain a single @, a single dot, no space and is the correct length'
    return False


def is_correct_length(string):
    MIN_CHAR = 3
    MAX_CHAR = 20

    if len(string) >= MIN_CHAR and len(string) <= MAX_CHAR:
        return True
    return False


def is_string(value):
    try:
        str(value)
        return True
    except ValueError:
        return False


app.run()