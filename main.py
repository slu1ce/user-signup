from flask import Flask, request, render_template, redirect

app = Flask(__name__)
app.config['DEBUG'] = True

MIN_CHAR = 3
MAX_CHAR = 20

app.username_error = ''
app.password_error = ''
app.password_match = ''
app.email_error = ''

@app.route('/', methods=['POST', 'GET'])
def index():
    if(request.method == 'POST'):
        reset_errors()
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if(valid_username(username) and valid_password(password, verify)):
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
        if len(username) >= MIN_CHAR and len(username) <= MAX_CHAR:
            return True

    app.username_error = 'username needs to be between {} and {} characters.'.format(MIN_CHAR, MAX_CHAR)
    return False


def valid_password(password, verify):
    print(password, ' == ', verify, password == verify)
    if password and is_string(password):
        password = str(password)
        if len(password) >= MIN_CHAR and len(password) <= MAX_CHAR:
            if password == verify:
                return True

    return False
    app.password_error = 'password needs to be between {} and {} characters.'.format(MIN_CHAR, MAX_CHAR)



def is_string(value):
    try:
        str(value)
        return True
    except ValueError:
        return False


app.run()