from src.admin import adminpanel



def main_display():
    print("Welcome to JK rental rentals")
    print("Choose an option  :")
    print("1. Admin Panel")
    print("2. Customer Panel")
    print("3. Exit")

def admin_display():
    print("Welcome to Admin Panel")
    print("Choose an option  : ")
    print("1. Add Vehicle")
    print("2. Remove Vehicle")
    print("3. View All Vehicles")
    print("4. Back to Main Menu")

def customer_display():
    print("Welcome to Customer Panel")
    print("Choose an option:")
    print("1. Register Customer")
    print("2. Display Available Vehicles")
    print("3. Rent a Vehicle")
    print("4. Return a Vehicle")
    print("5. Exit Customer Panel")

def main():
    vehicles ={}
    admin = adminpanel(vehicles)
    while True:
        main_display()
        user_choice = input("Enter your Choice 1/2/3: ")
        if user_choice == "1":
            while True:
                admin_display()
                admin_choice = input("Enter your Choice 1/2/3: ")
                if admin_choice == "1":
                    vid = input("Enter Vehicle ID: ")
                    vtype = input("Enter Vehicle Type: ")
                    vmodel = input("Enter Vehicle Model: ")
                    vyear = int(input("Enter Vehicle Year: "))
                    vrent = int(input("Enter Vehicle Rent: "))
                    admin.add_vehicle(vid, vtype, vmodel, vyear, vrent)
                elif admin_choice == "2":
                    admin.view_inventory()
                elif admin_choice == "3":
                    print("Displaying all vehicles...")
                elif admin_choice == "4":
                    print("Exiting Admin panel...")
                    break
                else:
                    print("Invalid input.")
        elif user_choice == "2":
            print("Welcome to customer panel")
        elif user_choice == "3":
            print("Thank you for using JK rentals")
        else:
            print("Invalid choice. !!!!")

if __name__ =="__main__":
    main()
