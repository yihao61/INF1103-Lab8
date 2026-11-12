class Inventory:
    def __init__(self, inventory=[]):
        self.__inventory = inventory

    def get_inventory(self):
        return self.__inventory

    def check_id_exists(self, product_id):
        for product in self.__inventory:
            if product.get_product_id() == product_id:
                return True
        return False

    def check_name_exists(self, product_name):
        for product in self.__inventory:
            if product.get_name() == product_name:
                return True
        return False
    
    def add_product(self, prod):
        self.__inventory.append(prod)
        print("\nProduct added successfully!")
        return

    def update_stock(self):
        print("\nUpdate Stock")
        idinp = input("Enter Product ID: ")
        for prod in self.__inventory:
            if idinp == prod.get_product_id():
                print(f"\nProduct Found:\nName: {prod.get_name()}\nCurrent Stock: {prod.get_stock()}\n")
                while True:
                    usrinp = input("New Stock Quantity: ")
                    try:
                        validn = int(usrinp)
                        prod.update_stock(validn)
                        print("\nStock updated successfully!")
                        break
                    except ValueError:
                        print("Invalid Stock Quantity Entered! Try Again.")
                return

        print("Product not found. Please check the ID and try again.")

    def search_product(self):
        found = False
        print("\nSearch Product")
        idinp = input("Enter Product ID: ")

        for prod in self.__inventory:
            if prod.get_product_id() == idinp:
                print("\nProduct Found!")
                print("------------------------------------------------------------------------------------------------------------------------------------------------")
                print(prod.display_information())
                print("------------------------------------------------------------------------------------------------------------------------------------------------")
                found = True

        if not found:
            print("Product not found")
        
        return

    def display_all(self):
        print("\nCurrent Inventory\n"
            "------------------------------------------------------------------------------------------------------------------------------------------------")
        for prod in self.__inventory:
            print(prod.display_information())
        print("------------------------------------------------------------------------------------------------------------------------------------------------")
        return


    

    