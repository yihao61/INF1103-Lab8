import json
import os
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier

def save_inventory(inv_list, filepath):
    print("\nSaving inventory.....")

    with open(filepath, "w", encoding="utf-8") as file:
        # default=... serializes nested objects (e.g. Supplier) via their __dict__
        json.dump([product.__dict__ for product in inv_list], file, indent=4,
                  default=lambda obj: obj.__dict__)

    print("Inventory Saved.....\n")
    return

def save_suppliers(supplier_list, filepath):
    print("\nSaving suppliers.....")

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump([supplier.__dict__ for supplier in supplier_list], file, indent=4)

    print("Suppliers Saved.....\n")

def load_suppliers(filepath):
    suppliers = []

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

def load_inventory(filepath, supplier_list=None):
    """Load products. If a SupplierList is given, products share its Supplier
    objects (matched by id); unknown suppliers are added to it."""
    inv_list = []

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

if __name__ == "__main__":
    FILEPATH = "inventory.json"
    inventory = load_inventory(FILEPATH)
    print(inventory)