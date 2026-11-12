#parent class
from abc import ABC, abstractmethod
from supplier import Supplier

class Product(ABC):
    # The parameter names are the name-mangled attribute names so that a saved
    # JSON record can be passed straight into the constructor with **item.
    def __init__(self, _Product__id: str, _Product__name: str, _Product__price: float,
                 _Product__stock: int, _Product__supplier: Supplier):
        self.__id: str = _Product__id
        self.__name: str = _Product__name
        self.__price: float = _Product__price
        self.__stock: int = _Product__stock
        self.__supplier: Supplier = _Product__supplier

    def update_stock(self, quantity: int) -> None:
        if quantity >= 0: 
            self.__stock = quantity

    def get_product_id(self) -> str:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def display_information(self) -> str:
        return f"ID: {self.__id:<2} | Name: {self.__name:<15} | Price: ${self.__price:<8} | Stock: {self.__stock:<2} | {self.__supplier.get_name():<15} | {self.get_fulfilment_info()}"

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        return ""
