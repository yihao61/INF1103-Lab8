class SupplierList:
    def __init__(self, suppliers=None):
        self.__suppliers = suppliers if suppliers is not None else []

    def get_suppliers(self):
        return self.__suppliers

    def find_by_id(self, supplier_id):
        for supplier in self.__suppliers:
            if supplier.get_supplier_id() == supplier_id:
                return supplier
        return None

    def add_supplier(self, supplier):
        self.__suppliers.append(supplier)
        print("\nSupplier added successfully!")

    def display_all(self):
        line = "-" * 100
        print(f"{line}\nCurrent Suppliers\n{line}")
        for supplier in self.__suppliers:
            print(supplier.display_information())
        print(line)
