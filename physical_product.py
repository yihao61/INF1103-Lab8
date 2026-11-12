from product import Product
from supplier import Supplier
from can_be_shipped import CanBeShipped

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, _Product__id: str, _Product__name: str, _Product__price: float,
                 _Product__stock: int, _Product__supplier: Supplier, _PhysicalProduct__weight: float):
        super().__init__(_Product__id, _Product__name, _Product__price, _Product__stock, _Product__supplier)
        self.__weight: float = _PhysicalProduct__weight

    def display_information(self) -> str:
        return f"{super().display_information()} | Weight: {f'{self.__weight}kg':<6} | Shipping Cost: ${self.calculate_shipping_cost():.2f}"

    def get_weight(self) -> float:
        return self.__weight

    def calculate_shipping_cost(self) -> float:
        shipping_cost_per_kg = 5.0  # Example shipping cost per kg
        return abs(self.__weight) * shipping_cost_per_kg

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."
