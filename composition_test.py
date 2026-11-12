from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from order import Order
from orderline import OrderLine

# Prediction (before running):
# If the same Product is added to two different Orders there will be
#   - 2 OrderLine objects (each Order creates its own line), and
#   - still only 1 Product object (both lines just refer to it).
# Order -> OrderLine is composition (the Order creates and owns its lines).
# OrderLine -> Product is only a reference, so the Product is shared.

def check(description, condition):
    print(f"[{'PASS' if condition else 'FAIL'}] {description}")
    assert condition, description

supplier = Supplier("S001", "TechSupply Co", "TechSupply_Co@email.com")
laptop = PhysicalProduct("P001", "Laptop", 1200.0, 20, supplier, 2.0)
mouse = PhysicalProduct("P002", "Mouse", 25.5, 30, supplier, 0.6)
game = DigitalProduct("D001", "PacMan", 9.99, 20, supplier, 891.0)

print("=== 1. Create an Order and add products with add_order_line() ===")
order1 = Order("O1")
order1.add_order_line(laptop, 1)
order1.add_order_line(mouse, 2)
order1.add_order_line(game, 3)
check("Order created 3 order lines", len(order1.get_order_lines()) == 3)
check("Every line is an OrderLine owned by the Order",
      all(isinstance(line, OrderLine) for line in order1.get_order_lines()))

print("\n=== 2. Display each order line and calculate the total ===")
for line in order1.get_order_lines():
    print(line.display_information())
expected_total = 1200.0 * 1 + 25.5 * 2 + 9.99 * 3
print(f"Order total: ${order1.calculate_total():.2f}")
check("Total equals the sum of all subtotals", abs(order1.calculate_total() - expected_total) < 1e-9)
check("Total equals the sum of each OrderLine's own subtotal",
      order1.calculate_total() == sum(l.calculate_subtotal() for l in order1.get_order_lines()))

print("\n=== 3. Add the SAME Product to a different Order ===")
order2 = Order("O2")
order2.add_order_line(laptop, 4)
line_in_1 = order1.get_order_lines()[0]
line_in_2 = order2.get_order_lines()[0]
print(f"OrderLine in O1: id={id(line_in_1)}  OrderLine in O2: id={id(line_in_2)}")
print(f"Product in O1's line: id={id(line_in_1.get_product())}  "
      f"Product in O2's line: id={id(line_in_2.get_product())}")
check("Each Order created its OWN OrderLine (2 different OrderLine objects)", line_in_1 is not line_in_2)
check("Both lines refer to the SAME Product object (only 1 Product exists)",
      line_in_1.get_product() is line_in_2.get_product() is laptop)
check("Lines are independent (quantities differ)",
      line_in_1.get_quantity() == 1 and line_in_2.get_quantity() == 4)
check("Each order has its own total", order1.calculate_total() != order2.calculate_total())
print(f"O1 total: ${order1.calculate_total():.2f} | O2 total: ${order2.calculate_total():.2f}")

print("\n=== 4. Remove an order line through an Order method ===")
check("remove_order_line() removes the line", order1.remove_order_line("P002") is True)
check("Order 1 now has 2 lines", len(order1.get_order_lines()) == 2)
check("Removing an unknown product returns False", order1.remove_order_line("X999") is False)
check("Removing a line from O1 did not touch O2", len(order2.get_order_lines()) == 1)
check("The removed line's Product still exists and works", mouse.get_name() == "Mouse")
print(f"O1 total after removal: ${order1.calculate_total():.2f}")

print("\n=== 5. Delete the Order itself ===")
del order2
check("Product survives the deletion of an Order", laptop.get_name() == "Laptop")
check("Other Order is unaffected", order1.calculate_total() > 0)

print("\n=== 6. Only the Order manages its OrderLines ===")
print("Order has add_order_line(product, quantity) which CREATES the line itself.")
check("Order has no method that accepts a ready-made OrderLine",
      not hasattr(order1, "add_existing_order_line"))
check("OrderLine only knows its product and quantity, not which Order owns it",
      not any(isinstance(v, Order) for v in vars(line_in_1).values()))

print("""
Result: matches prediction. Two Orders -> 2 OrderLine objects, 1 shared Product.
An OrderLine should not be managed independently or moved to another Order because it
has no meaning outside its Order (it is just 'this much of a product on THIS order').
It is created by the Order and dies with it. Moving it would let two Orders share one
line, so changing the quantity on one order would silently change the other. Each
Order creates its own line instead, which keeps orders independent.""")
