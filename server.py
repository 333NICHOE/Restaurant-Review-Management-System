import mysql.connector as mariaDB

def dbConnection():
    try:
        connection = mariaDB.connect(
            user='root',
            password='admin',
            host='localhost',  
            port=3306,         
            database='TestDB'  
        )
        return connection
    except mariaDB.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None

def signUp(f_name, m_name, l_name, birthday, email, password):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return
    if checkEmailExists(email):
        print("Email already exists!")
        return
    try:
        cursor = connection.cursor()
        
        query = """
        INSERT INTO CUSTOMER (first_name, middle_name, last_name, birthday, age, email, password)
        VALUES (%s, %s, %s, %s, FLOOR(DATEDIFF(CURDATE(), %s) / 365.25), %s, %s)
        """
        
        cursor.execute(query, (f_name, m_name, l_name, birthday, birthday, email, password))
        connection.commit()
        print("Signup successful!")
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        connection.close()

def user_signIn(email, password):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return 'db_error'
    
    try:
        cursor = connection.cursor()
        
        # Check if email exists
        email_query = """
        SELECT email FROM CUSTOMER WHERE email = %s
        """
        cursor.execute(email_query, (email,))
        email_rows = cursor.fetchall()
        
        if not email_rows:
            return 'email_not_found'
        
        # Check if password is correct
        query = """
        SELECT email FROM CUSTOMER WHERE email = %s AND password = %s
        """
        cursor.execute(query, (email, password))
        rows = cursor.fetchall()
        
        if rows:
            return 'success'  # Sign-in successful
        else:
            return 'incorrect_password'  # Password incorrect
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return 'db_error'
    
    finally:
        cursor.close()
        connection.close()

def admin_signIn(email, password):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return 'db_error'
    
    try:
        cursor = connection.cursor()
        
        # Check if email exists
        email_query = """
        SELECT email FROM ADMIN WHERE email = %s
        """
        cursor.execute(email_query, (email,))
        email_rows = cursor.fetchall()
        
        if not email_rows:
            return 'email_not_found'
        
        # Check if password is correct
        query = """
        SELECT email FROM ADMIN WHERE email = %s AND password = %s
        """
        cursor.execute(query, (email, password))
        rows = cursor.fetchall()
        
        if rows:
            return 'success'  # Sign-in successful
        else:
            return 'incorrect_password'  # Password incorrect
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return 'db_error'
    
    finally:
        cursor.close()
        connection.close()

def checkEmailExists(email):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return False
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT email FROM CUSTOMER WHERE email = %s
        """
        
        cursor.execute(query, (email,))
        rows = cursor.fetchall()
        
        if rows:
            return True  # Email exists in the database
        else:
            return False  # Email does not exist in the database
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return False
    
    finally:
        cursor.close()
        connection.close()

#########################################################################################################
#                                          Getting Estabs and Food Items                                #
#########################################################################################################
def getAllEstablishments():
    connection = dbConnection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT establishment_id, name FROM FOOD_ESTABLISHMENT")
        establishments = cursor.fetchall()
        return establishments
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def getAllFoodItems():
    connection = dbConnection()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT food_id, name FROM FOOD_ITEM")
        food_items = cursor.fetchall()
        return food_items
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        connection.close()
#########################################################################################################
#                               Function for adding a food establishment                                #
#########################################################################################################
def addFoodEstablishment(name, barangay, postal_code, street_name, city, province, average_rating=0, average_price=0):
    connection = dbConnection()

    if connection is None:
        print("Failed to connect to database")
        return
    
    try:
        cursor = connection.cursor()

        query = """
        INSERT INTO FOOD_ESTABLISHMENT (name, barangay, postal_code, street_name, city, province, average_rating, average_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (name, barangay, postal_code, street_name, city, province, average_rating, average_price))
        connection.commit()
        
        print("Food Establishment added successfully!")

    except mariaDB.Error as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        connection.close()

#########################################################################################################
#                               Function for updating a food establishment                             #
#########################################################################################################
def updateFoodEstablishment(establishment_id, name, barangay, postal_code, street_name, city, province):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return
    
    try:
        cursor = connection.cursor()
        
        query = """
        UPDATE FOOD_ESTABLISHMENT
        SET name = %s, barangay = %s, postal_code = %s, street_name = %s, city = %s, province = %s
        WHERE Establishment_id = %s
        """
        
        cursor.execute(query, (name, barangay, postal_code, street_name, city, province, establishment_id))
        connection.commit()
        
        print("Food Establishment updated successfully!")
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        connection.close()

#########################################################################################################
#                               Function for deleting a food establishment                              #
#########################################################################################################
def deleteFoodEstablishment(establishment_id):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return
    
    try:
        cursor = connection.cursor()

        # Get all food items associated with the establishment
        cursor.execute("SELECT Food_id FROM FOOD_ITEM WHERE establishment_id = %s", (establishment_id,))
        food_items = cursor.fetchall()

        # Delete each food item and its associated reviews
        for food_item in food_items:
            deleteFoodItem(food_item[0])

        # Delete reviews associated with the establishment
        cursor.execute("DELETE FROM FOOD_REVIEW WHERE establishment_id = %s", (establishment_id,))

        # Delete the food establishment
        cursor.execute("DELETE FROM FOOD_ESTABLISHMENT WHERE Establishment_id = %s", (establishment_id,))
        
        connection.commit()
        print("Food Establishment and associated data deleted successfully!")
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        connection.close()

#########################################################################################################
#                               Function for searching a food establishment                             #
#########################################################################################################
def searchFoodEstablishment(search_term):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return []
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT * FROM FOOD_ESTABLISHMENT
        WHERE name LIKE %s OR city LIKE %s OR province LIKE %s
        """
        
        like_term = f"%{search_term}%"
        cursor.execute(query, (like_term, like_term, like_term))
        results = cursor.fetchall()
        
        return results
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return []
    
    finally:
        cursor.close()
        connection.close()

#########################################################################################################
#                       Function for getting the average price of an establishment                      #
#########################################################################################################
def updateAveragePrice(establishment_id, cursor):
    try:
        # Update the average price in the FOOD_ESTABLISHMENT table
        update_query = """
        UPDATE FOOD_ESTABLISHMENT 
        SET average_price = COALESCE((SELECT AVG(price) FROM FOOD_ITEM WHERE establishment_id = %s), 0)
        WHERE establishment_id = %s
        """
        cursor.execute(update_query, (establishment_id, establishment_id))

        print("Average price for establishment updated successfully!")
    except mariaDB.Error as e:
        print(f"Error in updating average price: {e}")



#########################################################################################################
#                                Function for displaying the establishments                             #
#########################################################################################################
def get_all_food_establishments():
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return []
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT * FROM FOOD_ESTABLISHMENT
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        return results
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return []
    
    finally:
        cursor.close()
        connection.close()

#########################################################################################################
#                                Function for checking if establishment exists                          #
#########################################################################################################
def isEstablishmentExists(establishment_id):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return False
    
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM FOOD_ESTABLISHMENT WHERE Establishment_id = %s"
        cursor.execute(query, (establishment_id,))
        result = cursor.fetchone()
        
        return result[0] > 0  # Returns True if establishment exists, otherwise False
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


#########################################################################################################
#                                   Function for adding the food item                                   #
#########################################################################################################
def addFoodItem(establishment_id, name, price, description, food_type,specific_type):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return
    
    try:
        cursor = connection.cursor()
        
        query = """
        INSERT INTO FOOD_ITEM (establishment_id, name, price, description, food_type)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (establishment_id, name, price, description, food_type))

        # Get the last inserted food_id
        cursor.execute("SELECT LAST_INSERT_ID()")
        food_id = cursor.fetchone()[0]
        
        # Insert into the specific table based on food_type
        if food_type == 'Meat':
            specific_query = "INSERT INTO MEAT (food_id, meat_type) VALUES (%s, %s)"
            cursor.execute(specific_query, (food_id, specific_type))
        elif food_type == 'Vegetable':
            specific_query = "INSERT INTO VEGETABLE (food_id, vegetable_type) VALUES (%s, %s)"
            cursor.execute(specific_query, (food_id, specific_type))
        elif food_type == 'Dessert':
            specific_query = "INSERT INTO DESSERT (food_id, dessert_type) VALUES (%s, %s)"
            cursor.execute(specific_query, (food_id, specific_type))
        updateAveragePrice(establishment_id, cursor)
        connection.commit()
        # Update the average price after adding a new food item
        
        
        print("Food Item added successfully!")
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        connection.close()
#########################################################################################################
#                                   Function for deleting the food item                                 #
#########################################################################################################
def deleteFoodItem(food_id):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return
    
    try:
        cursor = connection.cursor()

        # Get the establishment_id and food_type for the food item
        cursor.execute("SELECT establishment_id, food_type FROM FOOD_ITEM WHERE Food_id = %s", (food_id,))
        result = cursor.fetchone()
        
        if result is None:
            print("Food item not found.")
            return

        establishment_id, food_type = result

        # Delete associated reviews
        cursor.execute("DELETE FROM FOOD_REVIEW WHERE food_id = %s", (food_id,))

        # Determine the specific table based on food_type and delete the record
        if food_type == 'Meat':
            cursor.execute("DELETE FROM MEAT WHERE food_id = %s", (food_id,))
        elif food_type == 'Vegetable':
            cursor.execute("DELETE FROM VEGETABLE WHERE food_id = %s", (food_id,))
        elif food_type == 'Dessert':
            cursor.execute("DELETE FROM DESSERT WHERE food_id = %s", (food_id,))
        else:
            print("Unknown food type.")
            return

        # Delete the food item from FOOD_ITEM table
        cursor.execute("DELETE FROM FOOD_ITEM WHERE Food_id = %s", (food_id,))
        # Update the average price
        updateAveragePrice(establishment_id, cursor)
        connection.commit()
        
        
        
        print("Food Item deleted successfully!")
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        connection.close()

#########################################################################################################
#                                   Function for updating the food item                                  #
#########################################################################################################
def updateFoodItem(food_id, price, description):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return
    
    try:
        cursor = connection.cursor()
        
        query = """
        UPDATE FOOD_ITEM
        SET price = %s, description = %s
        WHERE Food_id = %s
        """
        
        cursor.execute(query, (price, description, food_id))

        # Get the establishment_id for the food item
        cursor.execute("SELECT establishment_id FROM FOOD_ITEM WHERE Food_id = %s", (food_id,))
        establishment_id = cursor.fetchone()[0]
        # Update the average price
        updateAveragePrice(establishment_id, cursor)
        connection.commit()
        
        print("Food Item updated successfully!")
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        connection.close()

#########################################################################################################
#                                   Function for searching the food item                                #
#########################################################################################################
def searchFoodItem(search_term):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return []
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT * FROM FOOD_ITEM
        WHERE name LIKE %s OR Price LIKE %s OR Rating LIKE %s
        """
        
        like_term = f"%{search_term}%"
        cursor.execute(query, (like_term, like_term, like_term))
        results = cursor.fetchall()
        
        return results
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return []
    
    finally:
        cursor.close()
        connection.close()


#########################################################################################################
#                                                                                                       #
#                                        FOOD REVIEW FUNCTIONS                                          #
#                                                                                                       #
#########################################################################################################
def getFoodEstablishmentName():
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return False
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT name FROM FOOD_ESTABLISHMENT
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            return [row[0] for row in results]  # Extract names from the results
        else:
            return None 
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return False
    
    finally:
        cursor.close()
        connection.close()

def getFoodItemsByEstabId(establishment_id):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return False
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT name FROM FOOD_ITEM WHERE establishment_id = %s
        """
        
        cursor.execute(query, (establishment_id,))
        results = cursor.fetchall()
        
        if results:
            return [row[0] for row in results]  # Extract names from the results
        else:
            return None 
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return False
    
    finally:
        cursor.close()
        connection.close()
        

def getCustomerIdByEmail(email):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return False
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT customer_id FROM CUSTOMER WHERE email = %s
        """
        
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        
        if result:
            return result[0]  # Extract names from the results
        else:
            return None 
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return False
    
    finally:
        cursor.close()
        connection.close()
        
def getEstablishmentIdByName(establishmment_name):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return False
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT establishment_id FROM FOOD_ESTABLISHMENT WHERE name = %s
        """
        
        cursor.execute(query, (establishmment_name,))
        result = cursor.fetchone()
        
        if result:
            return result[0]  # Extract names from the results
        else:
            return None 
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return False
    
    finally:
        cursor.close()
        connection.close()
        
def getItemIdByName(item_name, establishment_id):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return False
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT food_id FROM FOOD_ITEM WHERE name = %s AND establishment_id = %s
        """
        
        cursor.execute(query, (item_name, establishment_id))
        result = cursor.fetchone()
        
        if result:
            return result[0]  # Extract names from the results
        else:
            return None 
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return False
    
    finally:
        cursor.close()
        connection.close()
        
#########################################################################################################
#                                   Function for adding the food establishment review                   #
#########################################################################################################

def updateAverageFoodItemRating(food_id, cursor):
    try:
        
        update_query = """
        UPDATE FOOD_ITEM 
        SET rating = COALESCE((SELECT AVG(rating) FROM FOOD_REVIEW WHERE food_id = %s), 0)
        WHERE food_id = %s
        """
        cursor.execute(update_query, (food_id, food_id))
        #print("Average rating for food item updated successfully!")
        
    except mariaDB.Error as e:
        print(f"Error in updating average rating: {e}")

# AVERAGE THE FOOD_ESTABLISHMENT REVIEW
def updateAverageRating(establishment_id, cursor):
    try:
        
        update_query = """
        UPDATE FOOD_ESTABLISHMENT 
        SET average_rating = COALESCE((SELECT AVG(rating) FROM FOOD_REVIEW WHERE establishment_id = %s), 0)
        WHERE establishment_id = %s
        """
        cursor.execute(update_query, (establishment_id, establishment_id))
        #print("Average rating updated successfully!")
        
    except mariaDB.Error as e:
        print(f"Error in updating average rating: {e}")

# AVERAGE THE FOOD_ESTABLISHMENT REVIEW
def updateItemRating(food_id, cursor):
    try:
        
        update_query = """
        UPDATE FOOD_ITEM 
        SET rating = COALESCE((SELECT AVG(rating) FROM FOOD_REVIEW WHERE food_id = %s), 0)
        WHERE food_id = %s
        """
        cursor.execute(update_query, (food_id, food_id))
        #print("Average rating updated successfully!")
        
    except mariaDB.Error as e:
        print(f"Error in updating average rating: {e}")

def addFoodEstablishmentReview(review_type, rating, title, suggestion, customer_id, establishment_id):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return
    
    try:
        cursor = connection.cursor()
        
        query = """
        INSERT INTO FOOD_REVIEW (review_date, review_time, type_of_review, rating, title, suggestion, customer_id, establishment_id)
        VALUES (CURDATE(), CURTIME(), %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (review_type, rating, title, suggestion, customer_id, establishment_id))
        updateAverageRating(establishment_id, cursor)
        connection.commit()
        
        print("Review added successfully!")
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        connection.close()

def getReviewsByCustomerId(customer_id):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return False
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT 
            r.review_id,
            r.title,
            r.suggestion,
            r.rating,
            fi.name as item_name,
            fe.name as establishment_name
        FROM 
            FOOD_REVIEW r
        JOIN 
            CUSTOMER c ON r.customer_id = c.customer_id
        LEFT JOIN 
            FOOD_ITEM fi ON r.food_id = fi.food_id
        LEFT JOIN 
            FOOD_ESTABLISHMENT fe ON r.establishment_id = fe.establishment_id
        WHERE 
            r.customer_id = %s
        """
        
        cursor.execute(query, (customer_id,))
        results = cursor.fetchall()
        
        if results:
            return results
        else:
            return None 
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return False
    
    finally:
        cursor.close()
        connection.close()
        
def getReviewByReviewId(review_id):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return False
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT * FROM FOOD_REVIEW WHERE review_id = %s
        """
        
        cursor.execute(query, (review_id,))
        result = cursor.fetchone()
        
        if result:
            return result  
        else:
            return None 
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return False
    
    finally:
        cursor.close()
        connection.close()
        
def updateReview(review_id, title, suggestion, rating):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT establishment_id FROM FOOD_REVIEW WHERE review_id = %s", (review_id,))
        result = cursor.fetchone()

        if result is None:
            print("Review not found.")
            return False
        
        establishment_id = result[0]
        
        cursor.execute("SELECT food_id FROM FOOD_REVIEW WHERE review_id = %s", (review_id,))
        result = cursor.fetchone()

        if result:
            food_id = result[0]

        # Update the review
        query = """
        UPDATE FOOD_REVIEW 
        SET title = %s, suggestion = %s, rating = %s 
        WHERE review_id = %s
        """
        
        cursor.execute(query, (title, suggestion, rating, review_id))

        # After updating the review, update the average rating
        updateAverageRating(establishment_id, cursor)
        if food_id:
            updateItemRating(food_id, cursor)
        connection.commit()

        
        print("Review updated successfully.")

        return True
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return False
    
    finally:
        cursor.close()
        connection.close()

def deleteReview(review_id):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to the database.")
        return False
    
    try:
        cursor = connection.cursor()

        # Get the establishment_id for the review
        cursor.execute("SELECT establishment_id FROM FOOD_REVIEW WHERE review_id = %s", (review_id,))
        result = cursor.fetchone()
        
        if result is None:
            print("Review not found.")
            return False

        establishment_id = result[0]
        
        cursor.execute("SELECT food_id FROM FOOD_REVIEW WHERE review_id = %s", (review_id,))
        result = cursor.fetchone()

        if result:
            food_id = result[0]
        
        # Delete the review
        query = "DELETE FROM FOOD_REVIEW WHERE review_id = %s"
        cursor.execute(query, (review_id,))
        # Update the average rating
        updateAverageRating(establishment_id, cursor)
        if food_id:
            updateItemRating(food_id, cursor)
        connection.commit()
        
        
        print("Review deleted successfully!")
        return True
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return False
    
    finally:
        cursor.close()
        connection.close()
###############################################################
# Add food_item review
def addFoodItemReview(review_type, rating, title, suggestion, customer_id, establishment_id, item_id):
    try:
        connection = dbConnection()
        if connection is None:
            print("Failed to connect to the database.")
            return
        
        cursor = connection.cursor()
        
        query = """
        INSERT INTO FOOD_REVIEW (review_date, review_time, Type_of_review, rating, title, suggestion, customer_id, establishment_id, food_id)
        VALUES (CURDATE(), CURTIME(), %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (review_type, rating, title, suggestion, customer_id, establishment_id, item_id))
        updateAverageFoodItemRating(item_id, cursor)
        updateAverageRating(establishment_id, cursor)
        connection.commit()
        
        print("Review added successfully!")
        
    except mariaDB.Error as e:
        print(f"Error: {e}")
        
    finally:
        cursor.close()
        connection.close()

# Update food_item review
def updateFoodItemReview(review_id, title, suggestion, rating, ):
    connection = dbConnection()
    if connection is None:
        print("Failed to connect to database")
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT food_id FROM FOOD_REVIEW WHERE review_id = %s", (review_id,))
        result = cursor.fetchone()

        if result is None:
            print("Review not found.")
            return False
        
        food_id = result[0]

        query = """
                UPDATE FOOD_REVIEW
                SET title = %s, suggestionn = %s, rating = %s
                WHERE review_id = %s    
                """
        cursor.execute(query(title, suggestion, rating, review_id))
        updateAverageFoodItemRating(food_id, cursor)
        connection.commit()

        print("Review updated successfully.")

        return True
    
    except mariaDB.Error as e:
        print(f"Error: {e}")
        return False
    
    finally:
        cursor.close()
        connection.close()