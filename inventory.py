from product import Product

class Inventory:
    # Aggregation: the Inventory groups Product objects, but the products are
    # created elsewhere and can exist without the Inventory.
    # able to hold Physical or Digital products.
    def __init__(self, inventory: list[Product] | None = None):
        self.__inventory: list[Product] = inventory if inventory is not None else []

    def get_inventory(self) -> list[Product]:
        return self.__inventory

    def find_product(self, product_id: str) -> Product | None:
        """Return the matching Product, or None if it cannot be found."""
        for product in self.__inventory:
            if product.get_product_id() == product_id:
                return product
        return None

    def check_name_exists(self, product_name):
        for product in self.__inventory:
            if product.get_name() == product_name:
                return True
        return False
    
    def add_product(self, prod: Product):
        self.__inventory.append(prod)
        print("\nProduct added successfully!")
        return

    def remove_product(self, product_id: str) -> bool:
        """Remove the matching Product reference from the inventory.
        The Product object itself is not destroyed. Returns True if removed."""
        product = self.find_product(product_id)
        if product is None:
            print(f"Product ID: {product_id} not found.")
            return False
        self.__inventory.remove(product)
        print(f"Product {product_id} removed.")
        return True

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


    

    