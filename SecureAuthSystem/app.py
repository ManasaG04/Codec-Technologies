from flask import Flask, render_template, request, redirect, session
import sqlite3, bcrypt, random, smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- DATABASE ----------------

def connect_db():
    return sqlite3.connect("auth.db")

conn = connect_db()
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
email TEXT UNIQUE,
password BLOB
)
""")
conn.commit()
conn.close()

# ---------------- EMAIL OTP ----------------

SENDER_EMAIL = "gundremanasa0304@gmail.com"
APP_PASSWORD = "orqiszjhiiqhjikx"

def send_otp_email(to_email, otp):
    msg = EmailMessage()
    msg.set_content(f"Your OTP Code is: {otp}")
    msg["Subject"] = "Secure Auth OTP"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return redirect("/login")

# -------- REGISTER --------
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form["username"]
        email=request.form["email"]
        password=bcrypt.hashpw(request.form["password"].encode(),bcrypt.gensalt())

        conn=connect_db()
        cur=conn.cursor()
        cur.execute("INSERT INTO users VALUES(NULL,?,?,?)",(username,email,password))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# -------- LOGIN --------
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]

        conn=connect_db()
        cur=conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=?",(email,))
        user=cur.fetchone()

        if user and bcrypt.checkpw(password.encode(),user[3]):
            otp=random.randint(100000,999999)
            session["otp"]=otp
            session["user"]=email
            send_otp_email(email,otp)
            return redirect("/otp")

        return "Invalid Login"

    return render_template("login.html")

# -------- OTP --------
@app.route("/otp", methods=["GET","POST"])
def otp():
    message = ""

    if request.method == "POST":
        user_otp = request.form.get("otp")

        # If user did not enter OTP
        if not user_otp:
            message = "⚠ Please enter the OTP"
        
        # If OTP is not a number
        elif not user_otp.isdigit():
            message = "⚠ OTP must contain only numbers"

        # If OTP is correct
        elif int(user_otp) == session.get("otp"):
            return redirect("/dashboard")

        # If OTP is wrong
        else:
            message = "❌ Invalid OTP"

    return render_template("otp.html", message=message)


# -------- DASHBOARD --------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html")

# -------- FORGOT --------
@app.route("/forgot",methods=["GET","POST"])
def forgot():
    if request.method=="POST":
        session["reset_email"]=request.form["email"]
        return redirect("/reset")

    return render_template("forgot.html")

# -------- RESET --------
@app.route("/reset",methods=["GET","POST"])
def reset():
    if request.method=="POST":
        newpass=bcrypt.hashpw(request.form["password"].encode(),bcrypt.gensalt())

        conn=connect_db()
        cur=conn.cursor()
        cur.execute("UPDATE users SET password=? WHERE email=?",(newpass,session["reset_email"]))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("reset.html")

# -------- LOGOUT --------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- RUN ----------------

if __name__=="__main__":
    app.run(debug=True)
