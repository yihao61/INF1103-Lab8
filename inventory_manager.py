from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
import FileHandling
FILEPATH = "inventory.json"

def get_valid_input():
    while True:
        try:
            user = input("\nEnter option: ")
            if user.lower() == "exit":
                print("Exiting program...")
                return 6
            
            value = int(user)
            if 1 <= value <= 6:
                return value

            print("Number Out of range! Please choose options 1-6.")
        except ValueError:
            print("Invalid Option entered, please try again.")       

def add_product(inventory):
    Adding = True
    progress = 0
    print("Add New Product")
    while Adding:
        if progress == 0:     # Ask user for product type  
            typeinp = input("Product Type (Digital/Physical): ").strip().lower()
            if typeinp in ["digital", "physical", "d", "p"]:
                prodtype = "Digital" if typeinp in ["digital", "d"] else "Physical"
                progress+=1
            else:
                print("Invalid Product Type! Please enter 'Digital' or 'Physical'.")
                continue
    
        elif progress == 1:       # Ask user for product ID
            idinp = input(f"Product ID({prodtype}): {prodtype[0].upper()}").strip()
            if inventory.check_id_exists(prodtype[0].upper() + idinp):                
                print("ID already exits. Please pick a new one.")
                continue
            
            product_id = prodtype[0].upper() + idinp
            progress+=1

        elif progress == 2:     # Ask user for product name
            nameinp = input("Product Name: ")
            if inventory.check_name_exists(nameinp):
                print("Name already exits. Please pick a new one.")
                continue
            
            product_name = nameinp
            progress+=1

        elif progress == 3:     # Ask user for price
            priceinp = input("Price: ")
            try:
                validp = float(priceinp)
            except ValueError:
                print("Not a number. Try Again")
                continue
    
            product_price = validp
            progress+=1

        elif progress == 4:     # Ask user for stock quantity
            stockinp = input("Stock Quantity: ")

            try:
                valids = int(stockinp)
            except ValueError:
                print("Not a integer. Try Again!")
                continue
    
            product_stock = valids
            progress+=1
            
        elif progress == 5:     # Ask user for download size or weight
            if prodtype == "Digital":
                downloadinp = input("Download Size (MB): ")
                try:
                    validd = float(downloadinp)
                except ValueError:
                    print("Not a number. Try Again!")
                    continue
                product_download_size = validd
            else:
                weightinp = input("Weight (kg): ")
                try:
                    validw = float(weightinp)
                except ValueError:
                    print("Not a number. Try Again!")
                    continue
                product_weight = validw
            progress+=1
        else:
            #create new digital product object
            if prodtype == "Digital":    
                new_product = DigitalProduct(product_id, product_name, product_price, product_stock, product_download_size)
            else:
                new_product = PhysicalProduct(product_id, product_name, product_price, product_stock, product_weight)
            Adding = False

    # Add the new product to the inventory
    inventory.add_product(new_product)

def main():
    print("============================================================\n"
            "INVENTORY MANAGEMENT SYSTEM\n"
            "============================================================\n")

    inventory = Inventory(FileHandling.load_inventory(FILEPATH))
    exit_program = False

    print("\n----------- MENU -----------"
            "\n1. Display All Products"
            "\n2. Add Product"
            "\n3. Update Stock"
            "\n4. Search Product"
            "\n5. Save Inventory"
            "\n6. Exit"
            "\n----------------------------")

    while not exit_program:
        option = get_valid_input()
        match option:
            case 1:
                inventory.display_all()
            case 2:
                add_product(inventory)
            case 3:
                inventory.update_stock()
            case 4:
                inventory.search_product()
            case 5:
                FileHandling.save_inventory(inventory.get_inventory(), FILEPATH)
            case 6:
                exit_program = True

    FileHandling.save_inventory(inventory.get_inventory(), FILEPATH)
    print("Thank you for using Inventory Management System.")
    print("Program terminated.")



if __name__ == "__main__":
    main()