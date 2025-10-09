from flask import *
import random
import string
import subprocess
import threading
app = Flask(__name__)

invite_code="superdonk"

with open("keys.txt","w") as file:
    file.write("PSGacademy2123")

#login function approutes + signups
def generate_random_key(length=12):
    characters = string.ascii_letters + string.digits  # Includes a-z, A-Z, 0-9
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/')
def login():
    return render_template("login.html")
def refresh_keys():
    global valid_keys
    valid_keys = []
    try:
        with open("keys.txt", "r") as file:
            a = [line.strip() for line in file if line.strip()]  # Skip empty lines
        valid_keys = a  # Use list, not tuple
    except FileNotFoundError:
        valid_keys = []
    except Exception as e:
        print(f"Error reading keys.txt: {e}")

@app.route("/login_get",methods=["GET","POST"])
def login_func():
    if request.method=="POST":
        action=request.form.get("action")
        if action=="key_check":
            submitted_key = request.form.get("key").strip()
            refresh_keys()
            print("Valid keys:", valid_keys)
            if submitted_key in valid_keys:
                return render_template("dashboard.html")
            else:
                return render_template("login.html",error="Key is invalid")
        elif action=="take_signup":
            return render_template("signup.html")
        else: 
            return render_template("login.html", error="Invalid action")

@app.route("/sign_up",methods=["POST","GET"])
def signup():
    key=None
    error=None
    if request.method=="POST":
        action=request.form.get("action")
        if action=="gen_key":
            submited_key=request.form.get("invitecode")
            if submited_key==invite_code:
                key=generate_random_key()
                with open("keys.txt","a",encoding="utf-8") as file:
                    file.write(key + "\n")
                return render_template("signup.html",key=key)
            else:
                error="The invite code is not valid!"
                return render_template("signup.html",error=error)
        elif action=="ret_login":
            return render_template("login.html")
    elif request.method=="GET":
        return render_template("signup.html", key=None, error=None)


@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "startbuilder":
            noti = "Thank you for using UltraDonk - Builder started in background!"
            def run_builder():
                subprocess.run(["python", "builder.py"], creationflags=subprocess.CREATE_NO_WINDOW)
            
            # Create and start the thread
            builder_thread = threading.Thread(target=run_builder)
            builder_thread.daemon = True
            builder_thread.start()
            
            return render_template("dashboard.html", noti=noti)
        elif action=="see_clients":
            return render_template("clients.html") #add clients.html page  
    elif request.method=="GET":
        return render_template("dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)