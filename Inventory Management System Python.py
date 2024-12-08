import os

# Constants for file paths
PRODUCTS_FILE = "products.txt"
SUPPLIERS_FILE = "suppliers.txt"
ORDERS_FILE = "orders.txt"

# File headers
PRODUCT_HEADERS = ["Product ID", "Name", "Description", "Price", "Stock"]
SUPPLIER_HEADERS = ["Supplier ID", "Name", "Contact"]
ORDER_HEADERS = ["Order ID", "Product ID", "Quantity", "Order Date"]


# Utility functions
def initialize_file(file_path, headers):
    """Ensure a file exists and has a header."""
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, "w") as f:
            f.write(" | ".join(headers) + "\n")


def load_data(file_path):
    """Load data from a file into a list of lists."""
    try:
        with open(file_path, "r") as file:
            return [line.strip().split(" | ") for line in file.readlines()]
    except FileNotFoundError:
        return []


def save_data(file_path, data):
    """Save a list of lists to a file."""
    with open(file_path, "w") as file:
        file.writelines([" | ".join(map(str, record)) + "\n" for record in data])


def display_records(records, headers):
    """Display tabular data."""
    print("\n" + " | ".join(headers))
    print("-" * 40)
    for record in records[1:]:  # Skip header
        print(" | ".join(map(str, record)))
    print("-" * 40)


def get_numeric_input(prompt, data_type=int):
    """Get numeric input with validation."""
    while True:
        try:
            return data_type(input(prompt).strip())
        except ValueError:
            print(f"Invalid input. Please enter a {data_type.__name__}.")


# Core functionality
def add_product():
    initialize_file(PRODUCTS_FILE, PRODUCT_HEADERS)
    product_id = input("Enter Product ID: ").strip()
    name = input("Enter Product Name: ").strip()
    description = input("Enter Product Description: ").strip()
    price = get_numeric_input("Enter Product Price: ", float)
    stock = get_numeric_input("Enter Product Stock: ", int)

    product_data = [product_id, name, description, price, stock]
    save_data(PRODUCTS_FILE, load_data(PRODUCTS_FILE) + [product_data])
    print("Product added successfully!")


def update_product():
    products = load_data(PRODUCTS_FILE)
    if len(products) <= 1:
        print("No products available to update.")
        return

    display_records(products, PRODUCT_HEADERS)
    product_id = input("Enter the Product ID to update: ").strip()

    for index, product in enumerate(products[1:], start=1):  # Skip header
        if product[0] == product_id:
            print(f"Current details: {product}")
            new_name = input("Enter New Name (leave blank to keep current): ") or product[1]
            new_description = input("Enter New Description (leave blank to keep current): ") or product[2]
            new_price = input("Enter New Price (leave blank to keep current): ").strip() or product[3]
            new_stock = input("Enter New Stock (leave blank to keep current): ").strip() or product[4]

            products[index] = [product[0], new_name, new_description, new_price, new_stock]
            save_data(PRODUCTS_FILE, products)
            print("Product updated successfully!")
            return

    print("Product ID not found.")


def add_supplier():
    initialize_file(SUPPLIERS_FILE, SUPPLIER_HEADERS)
    supplier_id = input("Enter Supplier ID: ").strip()
    name = input("Enter Supplier Name: ").strip()
    contact = input("Enter Supplier Contact: ").strip()

    supplier_data = [supplier_id, name, contact]
    save_data(SUPPLIERS_FILE, load_data(SUPPLIERS_FILE) + [supplier_data])
    print("Supplier added successfully!")


def place_order():
    initialize_file(ORDERS_FILE, ORDER_HEADERS)
    products = load_data(PRODUCTS_FILE)
    if len(products) <= 1:
        print("No products available for ordering.")
        return

    display_records(products, PRODUCT_HEADERS)
    order_id = input("Enter Order ID: ").strip()
    product_id = input("Enter Product ID: ").strip()
    quantity = get_numeric_input("Enter Quantity: ")
    order_date = input("Enter Order Date (DD-MM-YYYY): ").strip()

    for product in products[1:]:
        if product[0] == product_id:
            stock = int(product[4])
            if stock >= quantity:
                product[4] = str(stock - quantity)
                save_data(PRODUCTS_FILE, products)
                order_data = [order_id, product_id, quantity, order_date]
                save_data(ORDERS_FILE, load_data(ORDERS_FILE) + [order_data])
                print("Order placed successfully!")
                return
            else:
                print("Insufficient stock.")
                return

    print("Product ID not found.")


def view_inventory():
    products = load_data(PRODUCTS_FILE)
    if len(products) <= 1:
        print("No products available.")
        return
    display_records(products, PRODUCT_HEADERS)


def generate_reports():
    print("\n1. Low Stock Items\n2. Product Sales")
    choice = input("Enter your choice: ").strip()
    if choice == "1":
        generate_low_stock_report()
    elif choice == "2":
        generate_product_sales_report()
    else:
        print("Invalid choice.")


def generate_low_stock_report():
    products = load_data(PRODUCTS_FILE)
    threshold = get_numeric_input("Enter stock threshold: ")
    print("\nLow Stock Items:")
    print("ID | Name | Stock")
    print("-" * 30)
    for product in products[1:]:
        if int(product[4]) < threshold:
            print(f"{product[0]} | {product[1]} | {product[4]}")


def generate_product_sales_report():
    orders = load_data(ORDERS_FILE)
    sales = {}
    for order in orders[1:]:
        product_id, quantity = order[1], int(order[2])
        sales[product_id] = sales.get(product_id, 0) + quantity

    print("\nProduct Sales Report:")
    print("Product ID | Quantity Sold")
    print("-" * 30)
    for product_id, quantity in sales.items():
        print(f"{product_id} | {quantity}")


def display_menu():
    while True:
        print("\n" + "*" * 30)
        print("Inventory Management System")
        print("1. Add a New Product")
        print("2. Update Product Details")
        print("3. Add a New Supplier")
        print("4. Place an Order")
        print("5. View Inventory")
        print("6. Generate Reports")
        print("7. Exit")
        print("*" * 30)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_product()
        elif choice == "2":
            update_product()
        elif choice == "3":
            add_supplier()
        elif choice == "4":
            place_order()
        elif choice == "5":
            view_inventory()
        elif choice == "6":
            generate_reports()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# Initialize and run the program
if __name__ == "__main__":
    display_menu()

