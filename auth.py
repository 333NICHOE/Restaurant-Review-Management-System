import server
import re
import review
from datetime import datetime

def get_customer_id(email):
    return server.getCustomerIdByEmail(email)

def is_valid_email(email):
    # regex for validating an email address
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y/%m/%d')
        return True
    except ValueError:
        return False

def user_signIn():
    while True:
        email = input('\nEmail: ').strip()
        if not is_valid_email(email):
            print("Invalid email format.")
            continue
        break
    
    while True:
        password = input('Password: ').strip()
        if not len(password) >= 8:
            print("Password must be at least 8 characters long.")
            continue
        break
    
    result = server.user_signIn(email, password)
    customer_id = get_customer_id(email)
    
    if result == 'success':
        print("Sign In successful!")
        review.home(customer_id)
    elif result == 'email_not_found':
        print("Email not found. Please sign up.")
    elif result == 'incorrect_password':
        print("Incorrect password. Please try again.")
    else:
        print("An error occurred during sign in.")
    return

def admin_signIn():
    while True:
        email = input('\nEmail: ').strip()
        if not is_valid_email(email):
            print("Invalid email format.")
            continue
        break
    
    while True:
        password = input('Password: ').strip()
        if not len(password) >= 8:
            print("Password must be at least 8 characters long.")
            continue
        break
    
    if server.admin_signIn(email, password):
        # Redirect to admin menu
        import admin_menu
        admin_menu.admin_menu()
    else:
        return

def signUp():
    while True:
        first_name = input('\nFirst Name: ').strip()
        if not first_name:
            print("First Name cannot be empty.")
            continue
        break
    while True:
        middle_name = input('Middle Name: ').strip()
        if not middle_name:
            print("Middle Name cannot be empty.")
            continue
        break
    
    while True:
        last_name = input('Last Name: ').strip()
        if not last_name:
            print("Last Name cannot be empty.")
            continue
        break
    
    while True:
        birthday = input('Birthday(yyyy/mm/dd): ').strip()
        if not is_valid_date(birthday):
            print("Invalid birthday format. Please use yyyy/mm/dd")
            continue
        break
    
    while True:
        email = input('Email: ').strip()
        if not is_valid_email(email):
            print("Invalid email format.")
            continue
        break
    
    while True:
        password = input('Password: ').strip()
        if not len(password) >= 8:
            print("Password must be at least 8 characters long.")
            continue
        break
    
    server.signUp(first_name, middle_name, last_name, birthday, email, password)
    return

def start():
    while True:
        print("\n------------------Welcome-----------------")
        print("[1] User Sign In")
        print("[2] Admin Sign In")
        print("[3] Sign Up")
        print("[0] Exit")
        
        choice = input("Select an option: ").strip()
        
        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            user_signIn()
        elif choice == "2":
            admin_signIn()
        elif choice == "3":
            signUp()
        else:
            print("Invalid option. Please try again.")
