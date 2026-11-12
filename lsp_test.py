from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order

# 6.2 / 6.3 Liskov Substitution Principle (LSP) test.
# Every function below accepts a Product and never checks for a subclass.

def check(description: str, condition: bool) -> None:
    print(f"[{'PASS' if condition else 'FAIL'}] {description}")
    assert condition, description

def show_product_details(product: Product) -> None:
    """Uses only behaviour every Product promises."""
    print(product.display_information())
    print(product.get_fulfilment_info())

def exercise_product(product: Product) -> None:
    """Normal Product operations, written against the Product abstraction only."""
    original_stock = product.get_stock()

    # Expectation set by Product.update_stock(): a non-negative quantity replaces
    # the stock, a negative quantity is ignored.
    product.update_stock(7)
    check(f"{product.get_name()}: update_stock(7) sets stock to 7", product.get_stock() == 7)
    product.update_stock(-5)
    check(f"{product.get_name()}: update_stock(-5) is ignored (stock stays 7)", product.get_stock() == 7)
    product.update_stock(0)
    check(f"{product.get_name()}: update_stock(0) is accepted", product.get_stock() == 0)
    product.update_stock(original_stock)

    # Return types promised by Product.
    check(f"{product.get_name()}: display_information() returns str", isinstance(product.display_information(), str))
    check(f"{product.get_name()}: get_fulfilment_info() returns str", isinstance(product.get_fulfilment_info(), str))
    check(f"{product.get_name()}: get_price() is a number", isinstance(product.get_price(), (int, float)))
    check(f"{product.get_name()}: get_stock() returns int", isinstance(product.get_stock(), int))

supplier = Supplier("S001", "TechSupply Co", "TechSupply_Co@email.com")
laptop = PhysicalProduct("P001", "Laptop", 1200.0, 20, supplier, 2.0)
game = DigitalProduct("D001", "PacMan", 9.99, 20, supplier, 891.0)

print("=== 1. One function, both subclasses ===")
for product in (laptop, game):
    show_product_details(product)
    print()

print("=== 2. Same Product operations work on both ===")
for product in (laptop, game):
    exercise_product(product)

print("\n=== 3. Both can be added to an Inventory and used by its normal operations ===")
inventory = Inventory()
inventory.add_product(laptop)
inventory.add_product(game)
check("Inventory holds both types", len(inventory.get_inventory()) == 2)
check("find_product works for the physical product", inventory.find_product("P001") is laptop)
check("find_product works for the digital product", inventory.find_product("D001") is game)
check("check_name_exists works for both",
      inventory.check_name_exists("Laptop") and inventory.check_name_exists("PacMan"))
inventory.display_all()

print("\n=== 4. Both can be used in an Order (OrderLine only needs a Product) ===")
order = Order("O1")
order.add_order_line(laptop, 1)
order.add_order_line(game, 2)
order.display_all()
check("Order total is correct for mixed product types", abs(order.calculate_total() - (1200.0 + 2 * 9.99)) < 1e-9)

print("\n=== 5. remove_product works for both ===")
check("Remove physical", inventory.remove_product("P001") is True)
check("Remove digital", inventory.remove_product("D001") is True)
check("Inventory is empty", len(inventory.get_inventory()) == 0)

print("\n=== 6. Diagnose: a subclass that breaks the parent's expectation ===")
class BadDigitalProduct(DigitalProduct):
    def update_stock(self, quantity: int) -> None:
        raise NotImplementedError("Digital products have no stock")

bad = BadDigitalProduct("D999", "Bad Game", 1.0, 5, supplier, 1.0)
bad_inventory = Inventory()
bad_inventory.add_product(bad)
try:
    for product in bad_inventory.get_inventory():
        product.update_stock(10)   # normal Product code, valid input
    broke = False
except NotImplementedError:
    broke = True
check("BadDigitalProduct breaks code that only uses Product (LSP violation)", broke)

print("""
Written answers
---------------
Expectation preserved: Product.update_stock(quantity) sets the stock when quantity >= 0
and ignores a negative quantity. PhysicalProduct and DigitalProduct do not override it,
so both keep exactly that meaning and any code written for Product can rely on it.

Diagnosis: Yes, this violates LSP. Product accepts update_stock() for any valid
quantity, but the teammate's DigitalProduct rejects a valid input by raising an error,
so a Product-only caller such as Inventory crashes. I would change the subclass by
deleting the override, because digital products in this system do track a stock count
(for example licences or copies). If digital products truly had no stock, the fix would
be the parent class: move stock handling out of Product into a separate Stockable
abstraction, instead of adding subclass checks to Inventory.""")
