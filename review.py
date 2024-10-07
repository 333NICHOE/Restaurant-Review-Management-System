import server

def get_customer_id(email):
    return server.getCustomerIdByEmail(email)

def get_establishment_id(establishment_name):
    return server.getEstablishmentIdByName(establishment_name)

def get_item_id(item_name, establishment_id):
    return server.getItemIdByName(item_name, establishment_id)

def get_all_establishment():
    return server.getFoodEstablishmentName()

def get_establishment_items(establishment_id):
    return server.getFoodItemsByEstabId(establishment_id)

def get_all_user_review(customer_id):
    return server.getReviewsByCustomerId(customer_id)

def get_review(review_id):
    return server.getReviewByReviewId(review_id)

# function for adding review
def add_food_establishment_review(customer_id):
    try:
        establishment_names = get_all_establishment()
        if establishment_names is False:
            print("Failed to retrieve food establishment names.")
            return
        elif establishment_names is None:
            print("No food establishments found.")
            return
        else:
            print("\n----------Food Establishment Names--------")
            for name in establishment_names:
                print(name)
            print("----------Food Establishment Names--------\n")
        
        review_type = 'Food Establishment'

        while True:
            establishment_name = str(input("Enter Establishment Name To Review: "))
            if not establishment_name:
                print("Establishment Name Required!")
                continue
            establishment_id = get_establishment_id(establishment_name)
            if not establishment_id:
                print("Establishment Not Found!")
                continue
            break
        
        
        while True:
            title = str(input("Enter Review Title: "))
            if not title:
                print("Review Title Required!")
                continue
            break
        
        while True:
            suggestion = str(input("Enter Suggestion: "))
            if not suggestion:
                print("Suggestion Required!")
                continue
            break
        
        while True:
            rating_input = input("Enter Rating: ")
            if not rating_input:
                print("Rating Required!")
                continue
            try:
                rating = int(rating_input)
                if not 0 <= rating <= 5:
                    print("Rating must be between 0 and 5.")
                    continue
            except ValueError:
                print("Invalid Input! Please enter a valid number.")
                continue
            break
        server.addFoodEstablishmentReview(review_type, rating, title, suggestion, customer_id, establishment_id)
        return
    except Exception as e:
        print(e)

def add_food_item_review(customer_id):
    try:
        establishment_names = get_all_establishment()
        if establishment_names is False:
            print("Failed to retrieve food establishments.")
            return
        elif establishment_names is None:
            print("No food establishments found.")
            return
        else:
            print("\n----------Food Establishment Names--------")
            for name in establishment_names:
                print(name)
            print("----------Food Establishment Names--------\n")
        
        review_type = 'Food Item'

        while True:
            establishment_name = str(input("Enter Establishment Name: "))
            if not establishment_name:
                print("Establishment Name Required!")
                continue
            establishment_id = get_establishment_id(establishment_name)
            if not establishment_id:
                print("Establishment Not Found!")
                continue
            break
        
        food_names = get_establishment_items(establishment_id)
        
        if food_names is False:
            print("Failed to retrieve food items.")
            return
        elif food_names is None:
            print("No food food items found.")
            return
        else:
            print(f"\n-----Food Item/s in {establishment_name}-----")
            for name in food_names:
                print(name)
            print(f"-----Food Item/s in {establishment_name}-----\n")
        
        while True:
            item_name = str(input("Enter Item Name To Review: "))
            if not item_name:
                print("Item Name Required!")
                continue
            item_id = get_item_id(item_name, establishment_id)
            if not item_id:
                print("Item Not Found!")
                continue
            break
        
        while True:
            title = str(input("Enter Review Title: "))
            if not title:
                print("Review Title Required!")
                continue
            break
        
        while True:
            suggestion = str(input("Enter Suggestion: "))
            if not suggestion:
                print("Suggestion Required!")
                continue
            break
        
        while True:
            rating_input = input("Enter Rating: ")
            if not rating_input:
                print("Rating Required!")
                continue
            try:
                rating = int(rating_input)
                if not 0 <= rating <= 5:
                    print("Rating must be between 0 and 5.")
                    continue
            except ValueError:
                print("Invalid Input! Please enter a valid number.")
                continue
            break
        
        server.addFoodItemReview(review_type, rating, title, suggestion, customer_id, establishment_id, item_id)
        return
    except Exception as e:
        print(e)

def update_review(customer_id):
    try:
        reviews = get_all_user_review(customer_id)
        if reviews is False:
            print("Failed to retrieve reviews.")
            return
        elif reviews is None:
            print("No review found.")
            return
        else:
            print("\n------------------Reviews-----------------")
            print()
            for review in reviews:
                review_id, title, suggestion, rating, item_name, establishment_name = review
                print(f"Review ID: \t\t{review_id}")
                if not item_name:
                    print(f"Review Subject: \t{establishment_name}")
                else:
                    print(f"Review Subject: \t{item_name} of {establishment_name}")
                print(f"Review title: \t\t{title}")
                print(f"Review suggestion: \t{suggestion}")
                print(f"Review rating: \t\t{rating}")
                print()
            print("------------------Reviews-----------------\n")
        
        while True:
            review_id = str(input("Enter Review ID to Update: "))
            if not review_id:
                print("Review ID Required!")
                continue
            review = get_review(review_id)
            if not review:
                print("Review Not Found!")
                continue
            break
        
        while True:
            title = str(input("Update Review Title: "))
            if not title:
                print("Review Title Required!")
                continue
            break
        
        while True:
            suggestion = str(input("Update Suggestion: "))
            if not suggestion:
                print("Suggestion Required!")
                continue
            break
        
        while True:
            rating_input = input("Update Rating: ")
            if not rating_input:
                print("Rating Required!")
                continue
            try:
                rating = int(rating_input)
                if not 0 <= rating <= 5:
                    print("Rating must be between 0 and 5.")
                    continue
            except ValueError:
                print("Invalid Input! Please enter a valid number.")
                continue
            break
        
        server.updateReview(review_id, title, suggestion, rating)
        return
    except Exception as e:
        print(e)

def delete_review(customer_id):
    try:
        reviews = get_all_user_review(customer_id)
        if reviews is False:
            print("Failed to retrieve reviews.")
            return
        elif reviews is None:
            print("No review found.")
            return
        else:
            print("\n------------------Reviews-----------------")
            print()
            for review in reviews:
                review_id, title, suggestion, rating, item_name, establishment_name = review
                print(f"Review ID: \t\t{review_id}")
                if not item_name:
                    print(f"Review Subject: \t{establishment_name}")
                else:
                    print(f"Review Subject: \t{item_name} of {establishment_name}")
                print(f"Review title: \t\t{title}")
                print(f"Review suggestion: \t{suggestion}")
                print(f"Review rating: \t\t{rating}")
                print()
            print("------------------Reviews-----------------\n")
        
        while True:
            review_id = str(input("Enter Review ID to Delete: "))
            if not review_id:
                print("Review ID Required!")
                continue
            review = get_review(review_id)
            if not review:
                print("Review Not Found!")
                continue
            break
            
        server.deleteReview(review_id)
        return
    except Exception as e:
        print(e)

def home(customer_id):
    while True:
        print("------------------Review------------------")
        print("[1] Review Food Establishment")
        print("[2] Review Food Item")
        print("[3] Update Review")
        print("[4] Delete Review") 
        print("[0] Back")
        
        choice = input("Select an option: ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            add_food_establishment_review(customer_id)
        elif choice == '2':
            add_food_item_review(customer_id)
        elif choice == '3':
            update_review(customer_id)
        elif choice == '4':
            delete_review(customer_id)
        else:
            print("Invalid option. Please try again.")
        