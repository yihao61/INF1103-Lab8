import json
import os
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from order import Order, OrderList
from product import Product
from supplier_list import SupplierList
from inventory import Inventory

def save_inventory(inv_list: list[Product], filepath: str) -> None:
    print("\nSaving inventory.....")

    with open(filepath, "w", encoding="utf-8") as file:
        # default=... serializes nested objects (e.g. Supplier) via their __dict__
        json.dump([product.__dict__ for product in inv_list], file, indent=4,
                  default=lambda obj: obj.__dict__)

    print("Inventory Saved.....\n")
    return

def save_suppliers(supplier_list: list[Supplier], filepath: str) -> None:
    print("\nSaving suppliers.....")

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump([supplier.__dict__ for supplier in supplier_list], file, indent=4)

    print("Suppliers Saved.....\n")

def load_suppliers(filepath: str) -> list[Supplier]:
    suppliers: list[Supplier] = []

    # Check if the file exists, if not create a blank file
    if not os.path.exists(filepath):
        print(f"{filepath} does not exists, creating a blank file...")
        with open(filepath, "w", encoding="utf-8") as file:
            pass
        return suppliers

    with open(filepath, "r", encoding="utf-8") as file:
        print(f"{filepath} found.")
        try:
            full_list = json.load(file)
        except json.JSONDecodeError:
            print(f"{filepath} is empty or corrupted. Starting with no suppliers.")
            return suppliers

    for item in full_list:
        suppliers.append(Supplier(
            item["_Supplier__supplier_id"],
            item["_Supplier__name"],
            item["_Supplier__contact_email"],
        ))

    print("Suppliers loaded successfully!" if suppliers else "No suppliers saved.")
    return suppliers

def load_inventory(filepath: str, supplier_list: SupplierList | None = None) -> list[Product]:
    """Load products. If a SupplierList is given, products share its Supplier
    objects (matched by id); unknown suppliers are added to it."""
    inv_list: list[Product] = []

    # Check if the file exists, if not create a blank file
    if not os.path.exists(filepath):
        print(f"{filepath} does not exists, creating a blank file...")
        with open(filepath, "w", encoding="utf-8") as file:
            pass
        return inv_list

    # Load the inventory from the file
    with open(filepath, "r", encoding="utf-8") as file:
        print(f"{filepath} found.")
        try:
            full_list = json.load(file)
        except json.JSONDecodeError:
            print(f"{filepath} is empty or corrupted. Starting with an empty inventory.")
            return inv_list


    for item in full_list:
        # Rebuild the Supplier object from its saved dict
        sup = item.get("_Product__supplier")
        if isinstance(sup, dict):
            existing = supplier_list.find_by_id(sup["_Supplier__supplier_id"]) if supplier_list else None
            if existing is None:
                existing = Supplier(sup["_Supplier__supplier_id"],
                                    sup["_Supplier__name"],
                                    sup["_Supplier__contact_email"])
                if supplier_list is not None:
                    supplier_list.get_suppliers().append(existing)
            item["_Product__supplier"] = existing

        if item.get("_DigitalProduct__download_size") is not None:
            inv_list.append(DigitalProduct(**item))
        else:
            inv_list.append(PhysicalProduct(**item))

    if not inv_list:
        print("Inventory is empty.")
    else:
        print("Inventory loaded successfully!")
    
    return inv_list

def save_orders(order_list: list[Order], filepath: str) -> None:
    """Save orders. Each line stores only the product id and quantity, because
    the Order does not own the Product."""
    print("\nSaving orders.....")

    data = [
        {
            "order_id": order.get_order_id(),
            "order_lines": [
                {"product_id": line.get_product().get_product_id(),
                 "quantity": line.get_quantity()}
                for line in order.get_order_lines()
            ],
        }
        for order in order_list
    ]
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Orders Saved.....\n")

def load_orders(filepath: str, inventory: Inventory) -> OrderList:
    """Load orders, linking each line to the matching Product in the inventory."""
    orders = OrderList()

    if not os.path.exists(filepath):
        print(f"{filepath} does not exists, creating a blank file...")
        with open(filepath, "w", encoding="utf-8") as file:
            pass
        return orders

    with open(filepath, "r", encoding="utf-8") as file:
        print(f"{filepath} found.")
        try:
            full_list = json.load(file)
        except json.JSONDecodeError:
            print(f"{filepath} is empty or corrupted. Starting with no orders.")
            return orders

    for item in full_list:
        order = Order(item["order_id"])
        for line in item["order_lines"]:
            product = inventory.find_product(line["product_id"])
            if product is None:
                print(f"Skipping unknown product {line['product_id']} in order {item['order_id']}.")
                continue
            order.add_order_line(product, line["quantity"])
        orders.get_orders().append(order)

    print("Orders loaded successfully!" if orders.get_orders() else "No orders saved.")
    return orders

if __name__ == "__main__":
    FILEPATH = "inventory.json"
    inventory = load_inventory(FILEPATH)
    print(inventory)