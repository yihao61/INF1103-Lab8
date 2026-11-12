import json
import os
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

def save_inventory(inv_list, filepath):
    print("\nSaving inventory.....")

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump([product.__dict__ for product in inv_list], file, indent=4)

    print("Inventory Saved.....\n")
    return

def load_inventory(filepath):
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