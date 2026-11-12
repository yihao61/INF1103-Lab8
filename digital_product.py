from product import Product
from supplier import Supplier

class DigitalProduct(Product):
    def __init__(self, _Product__id: str, _Product__name: str, _Product__price: float,
                 _Product__stock: int, _Product__supplier: Supplier, _DigitalProduct__download_size: float):
        super().__init__(_Product__id, _Product__name, _Product__price, _Product__stock, _Product__supplier)
        self.__download_size: float = _DigitalProduct__download_size

    def display_information(self) -> str:
        return f"{super().display_information()}     | Download Size: {self.__download_size}MB"

    def get_download_size(self) -> float:
        return self.__download_size

    def get_fulfilment_info(self) -> str:
        return "Digital product. No shipping required."
