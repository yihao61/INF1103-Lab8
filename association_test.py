from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

# Prediction (before running):
# After `del supplier`, each Product should STILL display its supplier info.
# `del` only removes the variable name, not the object. The Products hold
# their own references, so the Supplier object stays alive until the last
# reference to it is gone.

print("=== 1. Create the Supplier independently ===")
supplier = Supplier("S001", "TechSupply Co", "sales@techsupply.com")
print(supplier.display_information())

print("\n=== 2. Create products using that Supplier ===")
physical = PhysicalProduct("P001", "Gaming Chair", 999.0, 10, supplier, 12.5)
digital = DigitalProduct("D001", "E-Book", 19.9, 50, supplier, 25)

print("\n=== 3. Display supplier information through each Product ===")
print(physical.display_information())
print(digital.display_information())
print("Physical product's supplier:", physical._Product__supplier.display_information())
print("Digital product's supplier: ", digital._Product__supplier.display_information())

print("\n=== 4. Confirm the objects are separate ===")
print("Supplier is not a Product:", not isinstance(supplier, (PhysicalProduct, DigitalProduct)))
print("Products share the same Supplier object:",
      physical._Product__supplier is digital._Product__supplier is supplier)
print("Supplier id():", id(supplier))
print("Physical id():", id(physical))
print("Digital id():  ", id(digital))

print("\n=== 5. Delete the supplier variable (del supplier) ===")
del supplier
try:
    supplier
except NameError:
    print("Variable 'supplier' no longer exists.")

print("\nProducts still show supplier info:")
print(physical.display_information())
print(digital.display_information())
print(physical._Product__supplier.display_information())

print("\n=== 6. Delete a Product; the Supplier is unaffected ===")
remaining_supplier = digital._Product__supplier
del physical
print("Physical product deleted. Digital product still works:")
print(digital.display_information())
print("Supplier still alive:", remaining_supplier.display_information())

print("\nResult: matches prediction. Product and Supplier are linked only by a")
print("reference (association), so each can exist independently of the other.")
