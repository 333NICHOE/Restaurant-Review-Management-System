import food_establishment  # Import the module for managing food establishments
import food_item  # Import the module for managing food items
import reports # Import the module for displaying reports

def admin_menu():
    while True:
        print("\n------------Admin Menu------------")
        print("[1] Manage Food Establishments")
        print("[2] Manage Food Items")
        print("[3] Reports")
        print("[0] Logout")
        
        choice = input("Select an option: ")
        
        if choice == '0':
            print("Logging out...")
            break
        elif choice == '1':
            food_establishment.home()  # Redirect to the food establishment management menu
        elif choice == '2':
            food_item.home()  # Redirect to the food item management menu
        elif choice == '3':
            reports.home() # Redirect to print reports
        else:
            print("Invalid option. Please try again.")
