from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

# Aggregation: an Inventory groups Product objects, but the Products are
# created independently and can exist without any Inventory.
# Prediction: removing a Product from an Inventory only removes the
# inventory's reference. The Product object itself is unaffected.

def check(description, condition):
    print(f"[{'PASS' if condition else 'FAIL'}] {description}")
    assert condition, description

print("=== 1. Create a Product BEFORE any Inventory exists ===")
supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")
chair = PhysicalProduct("P001", "Gaming Chair", 999.0, 10, supplier, 12.5)
ebook = DigitalProduct("D001", "E-Book", 19.9, 50, supplier, 25)
print(chair.display_information())
check("Product works with no Inventory", chair.get_name() == "Gaming Chair")

print("\n=== 2. Add the Product to Inventory A ===")
inventory_a = Inventory()
inventory_b = Inventory()
inventory_a.add_product(chair)
inventory_a.add_product(ebook)
check("Inventory A holds the same object (not a copy)", inventory_a.find_product("P001") is chair)
check("Inventory A holds both Physical and Digital products", len(inventory_a.get_inventory()) == 2)
check("Inventory B is separate and empty", len(inventory_b.get_inventory()) == 0)

print("\n=== 3. Remove it from Inventory A; the Product is still usable ===")
inventory_a.remove_product("P001")
check("Inventory A no longer finds the product", inventory_a.find_product("P001") is None)
check("Inventory A still holds the other product", inventory_a.find_product("D001") is ebook)
check("Removed Product still has its data", chair.get_name() == "Gaming Chair" and chair.get_stock() == 10)
chair.update_stock(7)
check("Removed Product still works (update_stock)", chair.get_stock() == 7)
print(chair.display_information())

print("\n=== 4. Add the SAME Product object to Inventory B ===")
inventory_b.add_product(chair)
check("Inventory B holds the same object", inventory_b.find_product("P001") is chair)
check("Change made while detached is visible in B", inventory_b.find_product("P001").get_stock() == 7)

print("\n=== 5. A Product can be in more than one Inventory at once ===")
inventory_a.add_product(chair)
inventory_a.find_product("P001").update_stock(3)
check("A and B share one object", inventory_a.find_product("P001") is inventory_b.find_product("P001"))
check("Update through A is seen through B", inventory_b.find_product("P001").get_stock() == 3)

print("\n=== 6. Empty the inventories; Products are not destroyed ===")
for product_id in ["P001", "D001"]:
    inventory_a.remove_product(product_id)
inventory_b.remove_product("P001")
check("Inventory A is empty", len(inventory_a.get_inventory()) == 0)
check("Inventory B is empty", len(inventory_b.get_inventory()) == 0)
print(chair.display_information())
print(ebook.display_information())
check("Products still exist and work", chair.get_stock() == 3 and ebook.get_name() == "E-Book")
check("Supplier is still reachable through the Products",
      chair._Product__supplier is supplier and ebook._Product__supplier is supplier)

print("\n=== 7. Delete the Inventory objects themselves ===")
del inventory_a, inventory_b
print(chair.display_information())
check("Products survive deletion of the Inventories", chair.get_name() == "Gaming Chair")

print("\nResult: matches prediction. Inventory only holds references to Products, so")
print("removing a Product or emptying/deleting an Inventory never destroys the Product.")
