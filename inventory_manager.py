from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from inventory import Inventory
from supplier_list import SupplierList
import FileHandling
import re

FILEPATH = "inventory.json"
SUPPLIER_FILEPATH = "suppliers.json"
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

def is_valid_email_regex(value: str) -> bool:
    if not isinstance(value, str):
        return False
    return bool(re.fullmatch(EMAIL_PATTERN, value.strip()))

def get_valid_input():
    while True:
        try:
            user = input("\nEnter option: ")
            if user.lower() == "exit":
                print("Exiting program...")
                return 0
            
            value = int(user)
            if 0 <= value <= 7:
                return value

            print("Number Out of range! Please choose options 1-7 or 0 to exit.")
        except ValueError:
            print("Invalid Option entered, please try again.")       

def add_product(inventory, supplier_list):
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
            if inventory.find_product(prodtype[0].upper() + idinp) is not None:
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

        elif progress == 5:
            # Pick an existing supplier by id, or create a new one
            supidinp = input("Supplier ID (e.g. S001, leave blank to create new): ").strip()
            if supidinp == "":
                product_supplier = add_supplier(supplier_list)
            else:
                product_supplier = supplier_list.find_by_id(supidinp)
                if product_supplier is None:
                    print("Supplier not found. Use menu option 3 to add it, or leave blank to create new.")
                    continue
            progress+=1
        elif progress == 6:     # Ask user for download size or weight
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
                new_product = DigitalProduct(product_id, product_name, product_price, product_stock, product_supplier , product_download_size)
            else:
                new_product = PhysicalProduct(product_id, product_name, product_price, product_stock, product_supplier, product_weight)
            Adding = False

    # Add the new product to the inventory
    inventory.add_product(new_product)

def add_supplier(supplier_list):
    """Prompt for supplier details, add to supplier_list and return the Supplier."""
    print("Add New Supplier")
    while True:
        supidinp = "S" + input("Supplier's id: S").strip()
        if supplier_list.find_by_id(supidinp) is not None:
            print("Supplier ID already exists. Please pick a new one.")
            continue
        break

    supnameinp = input("Supplier's Name: ").strip()

    while True:
        supemailinp = input("Supplier's Email: ").strip()
        if is_valid_email_regex(supemailinp):
            break
        print("Invalid Email Entered. Please try again.")

    new_supplier = Supplier(supidinp, supnameinp, supemailinp)
    supplier_list.add_supplier(new_supplier)
    return new_supplier


def main():
    print("============================================================\n"
            "INVENTORY MANAGEMENT SYSTEM\n"
            "============================================================\n")

    supplier_list = SupplierList(FileHandling.load_suppliers(SUPPLIER_FILEPATH))
    inventory = Inventory(FileHandling.load_inventory(FILEPATH, supplier_list))
    exit_program = False

    print("\n----------- MENU -----------"
            "\n1. Display All Products"
            "\n2. Add Product"
            "\n3. Display All Suppliers"
            "\n4. Add Supplier"
            "\n5. Update Stock"
            "\n6. Search Product"
            "\n7. Save Inventory"
            "\n0. Exit"
            "\n----------------------------")

    while not exit_program:
        option = get_valid_input()
        match option:
            case 1:
                inventory.display_all()
            case 2:
                add_product(inventory, supplier_list)
            case 3:
                supplier_list.display_all()
            case 4:
                add_supplier(supplier_list)
            case 5:
                inventory.update_stock()
            case 6:
                inventory.search_product()
            case 7:
                FileHandling.save_inventory(inventory.get_inventory(), FILEPATH)
                FileHandling.save_suppliers(supplier_list.get_suppliers(), SUPPLIER_FILEPATH)
            case 0:
                exit_program = True

    FileHandling.save_inventory(inventory.get_inventory(), FILEPATH)
    FileHandling.save_suppliers(supplier_list.get_suppliers(), SUPPLIER_FILEPATH)
    print("Thank you for using Inventory Management System.")
    print("Program terminated.")



if __name__ == "__main__":
    main()