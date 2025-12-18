from flask import Flask, request, render_template_string

app = Flask(__name__)

# Fake "database" (INTENTIONALLY BAD)
users = {
    "admin": "password123",
    "user": "letmein"
}

login_page = """
<h2>Insecure Login</h2>
<form method="POST">
  Username: <input name="username"><br>
  Password: <input name="password" type="password"><br><br>
  <button type="submit">Login</button>
</form>
<p style="color:red;">{{ message }}</p>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # INTENTIONALLY INSECURE LOGIC
        if username in users and users[username] == password:
            return f"<h1>Welcome, {username}!</h1><p>You are logged in.</p>"
        else:
            message = "Invalid username or password."

    return render_template_string(login_page, message=message)

if __name__ == "__main__":
    app.run(debug=True)
