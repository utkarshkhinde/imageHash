from flask import Flask, render_template, request, redirect, url_for, session, send_file
import os
from AESCipher import AESCipher

app = Flask(__name__)
app.secret_key = "supersecretkey"   # needed for session

cipher = AESCipher("mysecretpassword")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# fake users database (you can replace with real DB later)
USERS = {
    "admin": "1234",
    "utkarsh": "pass123",
    "riya": "pass123",
    "payal": "pass123",
    "mam": "pass123"
}

@app.route("/")
def home():
    if "user" in session:
        return render_template("index.html", user=session["user"])
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in USERS and USERS[username] == password:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return "<h3>Invalid credentials. <a href='/login'>Try again</a></h3>"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/select")
def select_image_page():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("selectImage.html")

@app.route("/encrypt", methods=["POST"])
def encrypt_image():
    if "user" not in session:
        return redirect(url_for("login"))

    file = request.files["image"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    with open(filepath, "rb") as f:
        img_data = f.read()

    encrypted = cipher.encrypt(img_data)

    enc_file = filepath + ".enc"
    with open(enc_file, "wb") as f:
        f.write(encrypted)

    return send_file(enc_file, as_attachment=True)

@app.route("/decrypt", methods=["POST"])
def decrypt_image():
    if "user" not in session:
        return redirect(url_for("login"))

    file = request.files["image"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    with open(filepath, "rb") as f:
        encrypted_data = f.read()

    decrypted = cipher.decrypt(encrypted_data)

    dec_file = filepath.replace(".enc", "_decrypted.jpg")
    with open(dec_file, "wb") as f:
        f.write(decrypted)

    return send_file(dec_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

