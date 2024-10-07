import server
import prettytable 
import food_item

# Report 1: View all food establishments
def report_one():
    connection = server.dbConnection()

    cursor = connection.cursor()

    # Execute the query
    query = "SELECT * FROM food_establishment"
    cursor.execute(query)

    # Fetch all the rows
    rows = cursor.fetchall()

    if not rows:
        print("\nNo establishments found.")
        return
    
    # Fetch column names
    column_names = [desc[0] for desc in cursor.description]

    # Create PrettyTable object
    table = prettytable.PrettyTable()

    table.field_names = column_names

    # Print the results
    for row in rows:
        table.add_row(row)

    print (table)

    # Close the cursor and connection
    cursor.close()
    connection.close()

# Report 2: View all food reviews for an establishment or a food item; 
def report_two():
    connection = server.dbConnection()
    cursor = connection.cursor()

    # Prompt the user to choose between establishment review or food item review
    print("\n[1] Check establishment review")
    print("[2] Check food item review")
    choice = input("Select an option: ")

    if choice == '1':
        establishments = food_item.show_all_establishments()
        if establishments == 'No establishments found.':
            cursor.close()
            connection.close()
            return
        else:
            establishment_id = input("\nEnter establishment ID: ")
            query_test = "SELECT * FROM food_establishment WHERE establishment_id = %s"
            cursor.execute(query_test, (establishment_id,))

            rows_test = cursor.fetchall()
            if not rows_test:
                print("\nNo establishment found.")
                cursor.close()
                connection.close()
                return

            query = "SELECT * FROM food_review WHERE establishment_id = %s AND type_of_review = 'Food Establishment'"
            cursor.execute(query, (establishment_id,))

    elif choice == '2':
        items = food_item.show_all_food_items()
        if items == 'No food items found.':
            cursor.close()
            connection.close()
            return
        else:
            food_id = input("\nEnter food ID: ")
            query_test = "SELECT * FROM food_item WHERE food_id = %s"
            cursor.execute(query_test, (food_id,))

            rows_test = cursor.fetchall()
            if not rows_test:
                print("\nNo food item found.")
                cursor.close()
                connection.close()
                return
            
            query = "SELECT * FROM food_review WHERE food_id = %s"
            cursor.execute(query, (food_id,))
        
    else:
        print("\nInvalid option.")
        cursor.close()
        connection.close()
        return

    # Fetch all the rows
    rows = cursor.fetchall()

    if not rows:
        if choice == '1':
            print("\nNo review found for food establishment.")
        elif choice == '2':
            print("\nNo review found for food item.")
        cursor.close()
        connection.close()
        return
    
    # Fetch column names
    column_names = [desc[0] for desc in cursor.description]

    # Create PrettyTable object
    table = prettytable.PrettyTable()
    table.field_names = column_names

    # Add rows to the table
    for row in rows:
        table.add_row(row)

    print(table)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    
# Report 3: View all food items from an establishment
def report_three():
    connection = server.dbConnection()
    cursor = connection.cursor()

    establishment = food_item.show_all_establishments()
    if establishment == 'No establishments found.':
        cursor.close()
        connection.close()
        return
    else:
        establishment_id = input("\nEnter establishment ID: ")

    # Execute the query
    query = "SELECT * FROM food_item WHERE establishment_id = %s"
    cursor.execute(query, (establishment_id,))

    # Fetch all the rows
    rows = cursor.fetchall()

    if not rows:
        print("\nNo establishments found.")
        return

    # Fetch column names
    column_names = [desc[0] for desc in cursor.description]

    # Create PrettyTable object
    table = prettytable.PrettyTable()

    table.field_names = column_names

    # Print the results
    for row in rows:
        table.add_row(row)

    print (table)

    # Close the cursor and connection
    cursor.close()
    connection.close()

# Report 4: View all food items from an establishment that belong to a food type {meat | veg | dessert}
def report_four():
    connection = server.dbConnection()
    cursor = connection.cursor()

    establishment = food_item.show_all_establishments()
    if establishment == 'No establishments found.':
        cursor.close()
        connection.close()
        return
    else:
        establishment_id = input("\nEnter establishment ID: ")
        query_test = "SELECT * FROM food_establishment WHERE establishment_id = %s"
        cursor.execute(query_test, (establishment_id,))

        rows_test = cursor.fetchall()
        if not rows_test:
            print("\nNo establishments found.")
            cursor.close()
            connection.close()
            return
        
        food_type = input("Enter food type (meat/veg/dessert): ")

    # Prepare the SQL query with parameters
    query = """
    SELECT fi.*
    FROM food_item fi
    JOIN food_establishment fe ON fi.establishment_id = fe.establishment_id
    """
    
    # Modify the query based on selected food type
    if food_type.lower() == "meat":
        query = query + "JOIN meat m ON fi.food_id = m.food_id "
    elif food_type.lower() == "veg":
        query = query + "JOIN vegetable v ON fi.food_id = v.food_id "
    elif food_type.lower() == "dessert":
        query = query + "JOIN dessert d ON fi.food_id = d.food_id "
    else:
        print("Invalid food type.")
        return

    # Add establishment filter to the query
    query = query + "WHERE fi.establishment_id = %s"

    # Execute the query with parameters
    cursor.execute(query, (establishment_id,))

    # Fetch the results
    rows = cursor.fetchall()
    
   # Check if no rows are returned and print the appropriate message
    if not rows:
        print(f"No {food_type.lower()} items found.")
    else:
        # Fetch column names
        column_names = [desc[0] for desc in cursor.description]

        # Create PrettyTable object
        table = prettytable.PrettyTable()
        table.field_names = column_names

        # Populate the table with data
        for row in rows:
            table.add_row(row)

        print(table)

    # Close cursor and connection
    cursor.close()
    connection.close()

# Report 5: View all reviews made within a month for an establishment or a food item
def report_five():
    connection = server.dbConnection()
    cursor = connection.cursor()

    print("\n[1] Check establishment review")
    print("[2] Check food item review")
    choice = input("Select an option: ")

    if choice == '1':
        establishments = food_item.show_all_establishments()
        if establishments == 'No establishments found.':
            cursor.close()
            connection.close()
            return        
        else:
            establishment_id = input("Enter establishment ID: ")
            query_test = "SELECT * FROM food_establishment WHERE establishment_id = %s"
            cursor.execute(query_test, (establishment_id,))

            rows_test = cursor.fetchall()
            if not rows_test:
                print("\nNo establishment found.")
                cursor.close()
                connection.close()
                return
            query = "SELECT * FROM food_review WHERE establishment_id = %s AND type_of_review = 'Food Establishment' AND review_date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)"
            cursor.execute(query, (establishment_id,))
    elif choice == '2':
        items = food_item.show_all_food_items()
        if items == 'No food items found.':
            cursor.close()
            connection.close()
            return        
        else:
            food_id = input("\nEnter food ID: ")
            query_test = "SELECT * FROM food_item WHERE food_id = %s"
            cursor.execute(query_test, (food_id,))

            rows_test = cursor.fetchall()
            if not rows_test:
                print("\nNo food item found.")
                cursor.close()
                connection.close()
                return
            query = "SELECT * FROM food_review WHERE food_id = %s AND review_date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)"
            cursor.execute(query, (food_id,))
    else:
        print("\nInvalid option.")
        cursor.close()
        connection.close()
        return
    
    # Fetch all the rows
    rows = cursor.fetchall()

    if not rows:
        if choice == '1':
            print("\nNo review found for food establishment.")
        elif choice == '2':
            print("\nNo review found for food item.")
        cursor.close()
        connection.close()
        return
    
    # Fetch column names
    column_names = [desc[0] for desc in cursor.description]

    # Create PrettyTable object
    table = prettytable.PrettyTable()
    table.field_names = column_names

    # Print the results
    for row in rows:
        table.add_row(row)

    print(table)

    # Close the cursor and connection
    cursor.close()
    connection.close()

# Report 6: View all establishments with a high average rating (rating >= 4)
def report_six():
    connection = server.dbConnection()
    cursor = connection.cursor()

    # Execute the query
    query = "SELECT * FROM food_establishment WHERE average_rating >= 4"
    cursor.execute(query)
    
    # Fetch all the rows
    rows = cursor.fetchall()

    if not rows:
        print("\nNo establishments with average rating equal to or greater than 4.")
        cursor.close()
        connection.close()
        return
    
    # Fetch column names
    column_names = [desc[0] for desc in cursor.description]

    # Create PrettyTable object
    table = prettytable.PrettyTable()

    table.field_names = column_names

    # Print the results
    for row in rows:
        table.add_row(row)

    print (table)

    # Close the cursor and connection
    cursor.close()
    connection.close()

# Report 7: View all food items from an establishment arranged according to price
def report_seven():
    connection = server.dbConnection()
    cursor = connection.cursor()

    establishments = food_item.show_all_establishments()
    if establishments == 'No establishments found.':
        cursor.close()
        connection.close()
        return
    else:
        establishment_id = input("\nEnter establishment ID: ")
        query = "SELECT * FROM food_item WHERE establishment_id = %s ORDER BY price;"
        cursor.execute(query, (establishment_id,))

    # Fetch all the rows
    rows = cursor.fetchall()

    if not rows:
        print("\nNo establishments found.")
        return
    
    # Fetch column names
    column_names = [desc[0] for desc in cursor.description]

    # Create PrettyTable object
    table = prettytable.PrettyTable()

    table.field_names = column_names

    # Print the results
    for row in rows:
        table.add_row(row)

    print (table)

    # Close the cursor and connection
    cursor.close()
    connection.close()

# Report 8: Search food items from any establishment based on a given price range and/or food type
def report_eight():
    connection = server.dbConnection()
    cursor = connection.cursor()

    establishments = food_item.show_all_establishments()
    if establishments == 'No establishments found.':
        cursor.close()
        connection.close()
        return
    else:
        establishment_id = input("\nEnter establishment ID: ")
        query_test = "SELECT * FROM food_establishment WHERE establishment_id = %s"
        cursor.execute(query_test, (establishment_id,))

        rows_test = cursor.fetchall()
        if not rows_test:
            print("\nNo establishments found.")
            cursor.close()
            connection.close()
            return
        
        food_type = input("Enter food type (meat/vegetable/dessert): ")
        if food_type != 'meat' and food_type != 'vegetable' and food_type != 'dessert':
            print('Invalid option.')
            cursor.close()
            connection.close()
            return

        if food_type == 'meat':
            query_test = "SELECT * FROM food_item WHERE food_type = %s"
            cursor.execute(query_test, (food_type,))
            rows_test = cursor.fetchall()

            if not rows_test:
                print("\nNo meat items found.")
                cursor.close()
                connection.close()
                return
            
        elif food_type == 'vegetable':
            query_test = "SELECT * FROM food_item WHERE food_type = %s"
            cursor.execute(query_test, (food_type,))
            rows_test = cursor.fetchall()

            if not rows_test:
                print("\nNo vegetable items found.")
                cursor.close()
                connection.close()
                return
            
        elif food_type == 'dessert':
            query_test = "SELECT * FROM food_item WHERE food_type = %s"
            cursor.execute(query_test, (food_type,))
            rows_test = cursor.fetchall()

            if not rows_test:
                print("\nNo dessert items found.")
                cursor.close()
                connection.close()
                return
            
        while True:
            try:
                min_price = float(input("Enter minimum price: "))
                break
            except ValueError:
                print('Invalid price. Please enter a valid number.')

        while True:
            try:
                max_price = float(input("Enter maximum price: "))
                break  
            except ValueError:
                print('Invalid price. Please enter a valid number.')


    # Execute the query
    query = "SELECT * FROM food_item WHERE establishment_id = %s AND price BETWEEN %s AND %s AND food_type = %s"
    cursor.execute(query, (establishment_id, min_price, max_price, food_type))

    # Fetch all the rows
    rows = cursor.fetchall()

    # Check if no rows are returned and print the appropriate message
    if not rows:
        print(f"\nNo {food_type.lower()} items found in that price range.")
    else:
        # Fetch column names
        column_names = [desc[0] for desc in cursor.description]

        # Create PrettyTable object
        table = prettytable.PrettyTable()
        table.field_names = column_names

        # Populate the table with data
        for row in rows:
            table.add_row(row)

        print(table)

    # Close cursor and connection
    cursor.close()
    connection.close()

def home ():
    while True:
        print("\n------------Reports Menu------------")
        print("[1] View all food establishments")
        print("[2] View all food reviews for an establishment or a food item")
        print("[3] View all food items from an establishment")
        print("[4] View all food items from an establishment that belong to a food type {meat | veg | dessert}")
        print("[5] View all reviews made within a month for an establishment or a food item")
        print("[6] View all establishments with a high average rating (rating >= 4)")
        print("[7] View all food items from an establishment arranged according to price")
        print("[8] Search food items from any establishment based on a given price range and/or food type")
        print("[0] Go Back")
        
        choice = input("Select an option: ")
        
        if choice == '0':
            break
        elif choice == '1':
            report_one()
        elif choice == '2':
            report_two()
        elif choice == '3':
            report_three()
        elif choice == '4':
            report_four()
        elif choice == '5':
            report_five()
        elif choice == '6':
            report_six()
        elif choice == '7':
            report_seven()
        elif choice == '8':
            report_eight()
        else:
            print("Invalid option. Please try again.")  