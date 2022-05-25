from shared import *


# Load Records from database
@app.route('/aery/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            session["dataX"] = []
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or email/password incorrect
            msg = 'Incorrect email/password!'
    # Show the login form with message (if any)
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['email'])
    # User is not loggedin redirect to login page
    return render_template('login.html', msg=msg)

@app.route('/aery/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/aery/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))


    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/aery/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/')
def index():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/create')
def create():
    return render_template('register.html')


@app.route('/stem')
def stem():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('stem-page.html', username=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/abm')
def abm():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('abm-page.html', username=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/humss')
def humss():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('humss-page.html', username=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/gas')
def gas():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('gas-page.html', username=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/learning-style')
def test():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('learning-style-test.html', username=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/academic')
def test2():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('academic-grades.html', username=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/interest')
def test3():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('interest-test.html', username=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
