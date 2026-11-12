from product import Product
from orderline import OrderLine

class Order:
    """An order. Composition: the Order creates and owns its OrderLine objects.
    The Products those lines refer to are NOT owned by the Order."""

    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> list[OrderLine]:
        return self.__order_lines

    def add_order_line(self, product: Product, quantity: int) -> None:
        # The OrderLine is created here, inside the Order, never passed in.
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def calculate_total(self) -> float:
        # Ask each OrderLine for its own subtotal.
        return sum((line.calculate_subtotal() for line in self.__order_lines), 0.0)

    def display_all(self) -> None:
        lines = "-" * 100
        """Print this order's lines and total."""
        print(lines)
        print(f"Order ID: {self.__order_id}")
        for line in self.__order_lines:
            print(f"  {line.display_information()}")
        print(f"  Total: ${self.calculate_total():.2f}")
        print(lines)

class OrderList:
    """Holds the orders placed (like Inventory holds products)."""

    def __init__(self, orders: list[Order] | None = None):
        self.__orders: list[Order] = orders if orders is not None else []

    def get_orders(self) -> list[Order]:
        return self.__orders

    def find_order(self, order_id: str) -> Order | None:
        for order in self.__orders:
            if order.get_order_id() == order_id:
                return order
        return None

    def add_order(self, order: Order) -> None:
        self.__orders.append(order)
        print("\nOrder added successfully!")

    def display_all(self) -> None:
        # Each Order prints its own divider lines, so only a heading is needed here.
        print("\nAll Orders")
        if not self.__orders:
            print("-" * 100)
            print("No orders yet.")
            print("-" * 100)
        for order in self.__orders:
            order.display_all()
