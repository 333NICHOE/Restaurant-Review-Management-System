import server

def show_all_establishments():
    establishments = server.getAllEstablishments()
    if establishments:
        print("-" * 45)
        print("------------Food Establishment List------------")
        print("-" * 45)
        for establishment in establishments:
            print("{:<15} {:<30}".format("["+str(establishment[0])+"]", establishment[1]))
        print("-" * 45)
    else:
        print("No establishments found.")

def validate_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        else:
            print("This field cannot be empty. Please try again.")

def validate_postal_code(prompt):
    while True:
        postal_code = input(prompt).strip()
        if postal_code.isdigit():
            return postal_code
        else:
            print("Postal code must be numeric. Please try again.")

def validate_id(prompt):
    while True:
        id_input = input(prompt).strip()
        if id_input.isdigit():
            return id_input
        else:
            print("ID must be numeric. Please try again.")

def add_food_establishment():
    try:
        show_all_establishments()
        name = validate_input("Enter Establishment Name: ")
        barangay = validate_input("Enter Barangay: ")
        postal_code = validate_postal_code("Enter Postal Code: ")
        street_name = validate_input("Enter Street Name: ")
        city = validate_input("Enter City: ")
        province = validate_input("Enter Province: ")

        average_rating = 0
        average_price = 0

        server.addFoodEstablishment(name, barangay, postal_code, street_name, city, province, average_rating, average_price)
    except Exception as e:
        print(f"Error: {e}")

def update_food_establishment():
    try:
        show_all_establishments()
        establishment_id = validate_id("Enter Establishment ID to update: ")
        name = validate_input("Enter new Establishment Name: ")
        barangay = validate_input("Enter new Barangay: ")
        postal_code = validate_postal_code("Enter new Postal Code: ")
        street_name = validate_input("Enter new Street Name: ")
        city = validate_input("Enter new City: ")
        province = validate_input("Enter new Province: ")

        server.updateFoodEstablishment(establishment_id, name, barangay, postal_code, street_name, city, province)
    except Exception as e:
        print(f"Error: {e}")

def delete_food_establishment():
    try:
        show_all_establishments()
        establishment_id = validate_id("Enter Establishment ID to delete (0 to go back): ")
        if establishment_id == '0':
            return
        server.deleteFoodEstablishment(establishment_id)
    except Exception as e:
        print(f"Error: {e}")

def search_food_establishment():
    try:
        search_term = validate_input("Enter search term - [NAME][PROVINCE][CITY][STREET][BARANGAY][POSTAL CODE] (0 to go back): ")
        if search_term == '0':
            return
        results = server.searchFoodEstablishment(search_term)
        if results:
            for result in results:
                print(result)
        else:
            print("No matching establishments found.")
    except Exception as e:
        print(f"Error: {e}")

def home():
    while True:
        print("------------Food Establishment------------")
        print("[1] Add Food Establishment")
        print("[2] Update Food Establishment")
        print("[3] Delete Food Establishment")
        print("[4] Search Food Establishment")
        print("[5] Display Food Establishments")
        print("[0] Back")
        
        try:
            choice = int(input("Select an option: "))
            if choice == 0:
                break
            elif choice == 1:
                print("Add Food Establishment selected.")
                add_food_establishment()
            elif choice == 2:
                print("Update Food Establishment selected.")
                update_food_establishment()
            elif choice == 3:
                print("Delete Food Establishment selected.")
                delete_food_establishment()
            elif choice == 4:
                print("Search Food Establishment selected.")
                search_food_establishment()
            elif choice == 5:
                print("Display Food Establishments selected.")
                show_all_establishments()
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
