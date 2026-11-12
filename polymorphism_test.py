from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

# Prediction (written before running):
#   P001 Laptop         (PhysicalProduct) -> "Requires physical shipping."
#   P002 Mouse          (PhysicalProduct) -> "Requires physical shipping."
#   D001 PacMan         (DigitalProduct)  -> "Digital product. No shipping required."
#   D002 Monster Hunter (DigitalProduct)  -> "Digital product. No shipping required."
# display_information() will also differ: physical products end with weight and
# shipping cost, digital products end with the download size.
PREDICTED_FULFILMENT = {
    "P001": "Requires physical shipping.",
    "P002": "Requires physical shipping.",
    "D001": "Digital product. No shipping required.",
    "D002": "Digital product. No shipping required.",
}
# Text each display_information() should end with (the specialised part).
PREDICTED_DISPLAY_ENDING = {
    "P001": "Weight: 2.0kg  | Shipping Cost: $10.00",
    "P002": "Weight: 0.6kg  | Shipping Cost: $3.00",
    "D001": "Download Size: 891.0MB",
    "D002": "Download Size: 6927.0MB",
}

def check(description: str, condition: bool) -> None:
    print(f"[{'PASS' if condition else 'FAIL'}] {description}")
    assert condition, description

def show_product_details(product: Product) -> None:
    """Works for any Product. It never asks which subclass it was given."""
    print(product.display_information())
    print(product.get_fulfilment_info())

supplier = Supplier("S001", "TechSupply Co", "TechSupply_Co@email.com")

print("=== 1. One Inventory, mixed Product types ===")
inventory = Inventory()
inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.0, 20, supplier, 2.0))
inventory.add_product(DigitalProduct("D001", "PacMan", 9.99, 20, supplier, 891.0))
inventory.add_product(PhysicalProduct("P002", "Mouse", 25.5, 30, supplier, 0.6))
inventory.add_product(DigitalProduct("D002", "Monster Hunter", 59.99, 20, supplier, 6927.0))
check("All four products are in the same collection", len(inventory.get_inventory()) == 4)

print("\n=== 2. ONE loop over the Product collection, no isinstance() ===")
for product in inventory.get_inventory():
    show_product_details(product)
    print()

print("=== 3. Compare with the prediction ===")
for product in inventory.get_inventory():
    product_id = product.get_product_id()
    check(f"{product_id} get_fulfilment_info() is '{PREDICTED_FULFILMENT[product_id]}'",
          product.get_fulfilment_info() == PREDICTED_FULFILMENT[product_id])
    check(f"{product_id} display_information() ends with '{PREDICTED_DISPLAY_ENDING[product_id]}'",
          product.display_information().endswith(PREDICTED_DISPLAY_ENDING[product_id]))

print("\n=== 4. Same method call, different behaviour ===")
messages = {product.get_fulfilment_info() for product in inventory.get_inventory()}
check("The same call produced exactly 2 different results (one per subclass)", len(messages) == 2)

print("""
Result: matches prediction. The loop only calls methods defined by Product
(display_information() and get_fulfilment_info()). Python picks the implementation
from each object's actual class, so the loop needs no type checks.

7.3 Polymorphism and LSP
------------------------
Polymorphism: show_product_details(product: Product) makes the same two calls for every
object. PhysicalProduct and DigitalProduct each override get_fulfilment_info() (and
display_information()), so the same call gives a different, correct result depending on
the object. The function was written once, against Product, and works unchanged for both
subclasses and for any subclass added later.

LSP: that only works because each subclass can safely stand in for Product. They keep
the promises Product makes: display_information() and get_fulfilment_info() return
strings, and inherited methods such as update_stock() keep their meaning. If a subclass
broke one of those promises (for example by raising an error from update_stock()), the
call would still be dispatched polymorphically but the calling code would break.
Polymorphism chooses WHICH implementation runs; LSP makes sure that any implementation
chosen is one the caller can trust.""")
