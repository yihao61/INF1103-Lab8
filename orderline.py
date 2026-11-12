from product import Product

class OrderLine:
    """One product and the quantity of it requested in an order."""

    def __init__(self, product: Product, quantity: int):
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> str:
        return (f"{self.__product.get_name():<15} | Qty: {self.__quantity:<3} | "
                f"Unit Price: ${self.__product.get_price():<8.2f} | "
                f"Subtotal: ${self.calculate_subtotal():.2f}")
