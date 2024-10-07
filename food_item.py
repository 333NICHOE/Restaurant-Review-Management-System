import server

def show_all_establishments():
    establishments = server.getAllEstablishments()
    if establishments:
        print("\nList of Establishments:")
        print("-" * 45)
        for establishment in establishments:
            print("{:<15} {:<30}".format("["+str(establishment[0])+"]", establishment[1]))
        print("-" * 45)
    else:
        print("No establishments found.")
        return("No establishments found.")
    
def show_all_food_items():
    food_items = server.getAllFoodItems()
    if food_items:
        print("\nList of Food Items:")
        print("-" * 40)
        for food_item in food_items:
            print("{:<10} {:<30}".format(food_item[0], food_item[1]))
        print("-" * 40)
    else:
        print("No food items found.")
        return("No food items found.")

def validate_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        else:
            print("This field cannot be empty. Please try again.")

def validate_price(prompt):
    while True:
        price = input(prompt).strip()
        try:
            float(price)
            return price
        except ValueError:
            print("Invalid price. Please enter a numeric value.")

def validate_establishment_id(prompt):
    while True:
        establishment_id = input(prompt).strip()
        if establishment_id.isdigit() and server.isEstablishmentExists(establishment_id):
            return establishment_id
        elif establishment_id == '0':
            return establishment_id
        else:
            print("Establishment ID does not exist or is invalid. Please enter a valid Establishment ID.")

def validate_food_id(prompt):
    while True:
        food_id = input(prompt).strip()
        if food_id.isdigit():
            return food_id
        elif food_id == '0':
            return food_id
        else:
            print("Food ID must be numeric. Please try again.")

def add_food_item():
    try:
        show_all_establishments()
        establishment_id = validate_establishment_id("Enter Establishment ID (0 to go back): ")
        if establishment_id == '0':
            return
        
        while True:
            print("Select Food Type:")
            print("[1] Meat")
            print("[2] Vegetable")
            print("[3] Dessert")
            print("[0] Back")
            food_type_choice = input("Enter choice (1, 2, 3, or 0 to go back): ").strip()
            
            if food_type_choice == '0':
                return
            elif food_type_choice == '1':
                food_type = 'Meat'
                specific_type = validate_input("Enter Meat Type: ")
                break
            elif food_type_choice == '2':
                food_type = 'Vegetable'
                specific_type = validate_input("Enter Vegetable Type: ")
                break
            elif food_type_choice == '3':
                food_type = 'Dessert'
                specific_type = validate_input("Enter Dessert Type: ")
                break
            else:
                print("Invalid choice. Please enter a valid option.")
        
        name = validate_input("Enter Food Name: ")
        price = validate_price("Enter Price: ")
        description = validate_input("Enter Food Description: ")

        server.addFoodItem(establishment_id, name, price, description, food_type, specific_type)
    except Exception as e:
        print(f"Error: {e}")

def update_food_item():
    try:
        show_all_food_items()
        while True:
            food_id = validate_food_id("Enter Food ID to update (0 to go back): ")
            if food_id == '0':
                return
            price = validate_price("Enter new Price: ")
            description = validate_input("Enter Food Description: ")

            server.updateFoodItem(food_id, price, description)
            break
    except Exception as e:
        print(f"Error: {e}")

def delete_food_item():
    try:
        show_all_food_items()
        while True:
            food_id = validate_food_id("Enter Food ID to delete (0 to go back): ")
            if food_id == '0':
                return
            server.deleteFoodItem(food_id)
            break
    except Exception as e:
        print(f"Error: {e}")

def search_food_item():
    while True:
        try:
            search_term = validate_input("Enter search term - [NAME][PROVINCE][CITY][STREET][BARANGAY][POSTAL CODE] (0 to go back): ")
            if search_term == '0':
                return
            results = server.searchFoodItem(search_term)
            
            if results:
                for result in results:
                    print(result)
            else:
                print("No matching food items found.")
        except Exception as e:
            print(f"Error: {e}")
            
def home():
    while True:
        print("----------------Food Item-----------------")
        print("[1] Add Food Item")
        print("[2] Update Food Item")
        print("[3] Delete Food Item") 
        print("[4] Search Food Item") 
        print("[0] Back")
        
        try:
            choice = int(input("Select an option: "))
            
            if choice == 0:
                break
            elif choice == 1:
                print("Add Food Item selected.")
                add_food_item()
            elif choice == 2:
                print("Update Food Item selected.")
                update_food_item()
            elif choice == 3:
                print("Delete Food Item selected.")
                delete_food_item()
            elif choice == 4:
                print("Search Food Item selected.")
                search_food_item()
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
