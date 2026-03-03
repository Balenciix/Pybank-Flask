from flask import Flask, render_template, request, redirect, url_for, session

# create the Flask app
app = Flask(__name__)

# this is needed to use sessions (to remember who is logged in)
app.secret_key = "pybank34193"

# copy your accounts dictionary here
accounts = {}


# This is our "database" - a dictionary that stores all accounts
# It lives in memory while the program is running
accounts = {}

def createAccount():
    print("--------- Create Account --------")

    # Ask user for username
    username = input("Please enter a username:")

    # if username already exists
    if username in accounts:
        print("Sorry, that username is already taken.")
    else:
        # ask for a PIN
        pin = int(input("Please enter a 4-digit PIN:"))

        # store new account in dictionary
        accounts[username] = {
            "pin": pin , 
            "balance": 0,
            "history": []
        }

        # Account creation successful!
        print("Your Account has been created! Welcome " + username) 


# to login into account
def login():
    print("-------- Login ---------")

    # ask user for their username
    username = input("Enter your username:")

    # checks if username exists in our accounts 
    if username not in accounts:
        print("Sorry, this username does not exist. Please create an account first.")
        return None
    
    # ask for their PIN
    pin = int(input("Please enter PIN:"))

    # check if pin matches what we have stored in accounts database
    if accounts[username]["pin"] != pin:
        print("Incorrect PIN, please try again.")
        return None
    
    # if everything is correct
    print("Login Successful! Welcome back, " + username + "!")
    return username



# to deposit money into account
def deposit(username):
    print("--------- Deposit ---------")

    depositAmt = float(input("How much would you like to deposit?: $"))

    # make sure the amount is greater than zero
    if depositAmt <= 0:
        print("Amount must be greater than zero.")
    else:
        # add their amount to their balance
        accounts[username]["balance"] = accounts[username]["balance"] + depositAmt

        # add a record to the accounts history list 
        accounts[username]["history"].append("Deposited $" + str(depositAmt))

        # show their new balance 
        print("Successfully deposited $" + str(depositAmt))
        print("Your new balance is $" + str(accounts[username]["balance"]))

# to withdraw money from account 
def withdraw(username):
    print("------ Withdraw ------")

    withdrawAmt = float(input("How much would you like to withdraw?"))

    # make sure amount is greater than zero.
    if withdrawAmt <= 0:
        print("Amount has to be greater than zero. Please try again.")
        
        # check if they have enough money in their account
    elif accounts[username]["balance"] < withdrawAmt:
        print("Insufficient funds. Your balance is currently $" + str(accounts[username]["balance"]))
    else:   # withdraw the amount requested
        accounts[username]["balance"] = accounts[username]["balance"] - withdrawAmt
        accounts[username]["history"].append("Withdrew $" + str(withdrawAmt))

        print("Successfully withdrew $" + str(withdrawAmt))
        print("Your new balance is $" + str(accounts[username]["balance"]))

# ------- FUNCTION 5: Check Balance --------

def checkBalence(username):
    print("------ Check Balance ------")

    # grabs balance from dictionary
    balanceAmt = accounts[username]["balance"]

    print("Your balance is $" + str(balanceAmt))


# ------ FUNCTION 6: Transaction History ------
def viewHistory(username):
    print("------ View History ------")

    # grabs history list from dictionary
    history = accounts[username]["history"]

    # checks if there's any transactions 
    if len(history) == 0:   # counts how many items are in a list. 0 = no list of transactions yet.
        print("No transactions yet.")

    # if there IS any transaction history - print it
    else:
        for transaction in history:
            print(transaction)



# ── ROUTES FOR FLASK ──

# Home page / Main Menu
@app.route("/")
def home():
    return render_template("index.html")


# Create Account
@app.route("/create", methods=["POST"])
def create():
    username = request.form.get("username")
    pin = request.form.get("pin")

    if username in accounts:
        return render_template("index.html", error="Username already taken.")

    accounts[username] = {
        "pin": pin,
        "balance": 0,
        "history": []
    }
    return render_template("index.html", msg="Account created! Welcome, " + username)


# Login
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    pin = request.form.get("pin")

    if username not in accounts:
        return render_template("index.html", error="Account not found.")

    if accounts[username]["pin"] != pin:
        return render_template("index.html", error="Incorrect PIN.")

    # save the logged in user to the session
    session["username"] = username
    return redirect(url_for("dashboard"))


# Dashboard (Account Menu)
@app.route("/dashboard")
def dashboard():
    # check if someone is logged in
    if "username" not in session:
        return redirect(url_for("home"))

    username = session["username"]
    balance = accounts[username]["balance"]
    history = accounts[username]["history"]
    return render_template("dashboard.html", username=username, balance=balance, history=history)


# Deposit
@app.route("/deposit", methods=["POST"])
def deposit():
    username = session["username"]
    amount = float(request.form.get("amount"))

    if amount <= 0:
        return redirect(url_for("dashboard"))

    accounts[username]["balance"] = accounts[username]["balance"] + amount
    accounts[username]["history"].append("Deposited $" + str(amount))
    return redirect(url_for("dashboard"))


# Withdraw
@app.route("/withdraw", methods=["POST"])
def withdraw():
    username = session["username"]
    amount = float(request.form.get("amount"))

    if amount <= 0 or amount > accounts[username]["balance"]:
        return redirect(url_for("dashboard"))

    accounts[username]["balance"] = accounts[username]["balance"] - amount
    accounts[username]["history"].append("Withdrew $" + str(amount))
    return redirect(url_for("dashboard"))


# Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


# run the app
if __name__ == "__main__":
    app.run(debug=True)



