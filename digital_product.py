from product import Product

class DigitalProduct(Product):
    def __init__(self, _Product__id, _Product__name, _Product__price, _Product__stock, _Product__supplier, _DigitalProduct__download_size):
        super().__init__(_Product__id, _Product__name, _Product__price, _Product__stock, _Product__supplier)
        self.__download_size = _DigitalProduct__download_size

    def display_information(self):
        return f"{super().display_information()}     | Download Size: {self.__download_size}MB"

    def get_download_size(self):
        return self.__download_size

    def get_fulfilment_info(self):
        return "Digital product. No shipping required."