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


# ------ MAIN MENU ------
def mainMenu():
    print("Welcome to PyBank!")

    # keeps app running until user decides to exit
    while True:
        print("\n-- Main Menu --")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option (1-3):")

        if choice == "1":
            createAccount()

        elif choice == "2":
            username = login()

            # if login successfull, show account menu
            if username != None:
                accountMenu(username)

        elif choice == "3":
            print("Thanks for using PyBank. Goodbye!")
            break

        else: 
            print("Invalid option. Please choose 1, 2, or 3.")


# ------ ACCOUNT MENU ------

def accountMenu(username):

    # keep account menu running until user logs out
    while True:
        print("\n-- Account Menu --")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transaction History")
        print("5. Logout")

        choice = input("Please choose option (1-5):")

        if choice == "1":
            checkBalence(username)

        elif choice == "2":
            deposit(username)

        elif choice == "3":
            withdraw(username)

        elif choice == "4":
            viewHistory(username)
        
        elif choice == "5":
            print("Logged out successfully. Goodbye, " + username + "!")
            break

        else:
            print("Invalid option. Please choose from 1 through 5.")


# run the app 
mainMenu()




            














