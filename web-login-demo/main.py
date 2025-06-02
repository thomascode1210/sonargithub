from flask import Flask, request, render_template_string, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Giả lập database bằng dictionary
users_db = {}

# HTML template đơn giản
template = '''
<!doctype html>
<title>{{ title }}</title>
<h1>{{ title }}</h1>
<form method="POST">
    {% if title == 'Sign Up' %}
    Username: <input type="text" name="username"><br>
    Email: <input type="email" name="email"><br>
    {% endif %}
    Password: <input type="password" name="password"><br>
    <input type="submit" value="{{ title }}">
</form>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul>
    {% for message in messages %}
      <li style="color: red;">{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
'''

@app.route('/')
def home():
    if 'username' in session:
        return f"Hello, {session['username']}! <br><a href='/logout'>Logout</a>"
    return "Welcome! <a href='/login'>Login</a> or <a href='/signup'>Sign Up</a>"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash("All fields are required!")
            return render_template_string(template, title="Sign Up")

        if username in users_db:
            flash("Username already exists.")
            return render_template_string(template, title="Sign Up")

        users_db[username] = {'email': email, 'password': password}
        flash("Signup successful! Please log in.")
        return redirect(url_for('login'))

    return render_template_string(template, title="Sign Up")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        username = request.form.get('username')

        user = users_db.get(username)

        if not user or user['password'] != password:
            flash("Invalid username or password.")
            return render_template_string(template, title="Login")

        session['username'] = username
        return redirect(url_for('home'))

    return render_template_string(template, title="Login")

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
