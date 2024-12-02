# Inventory Management System

# File paths
PRODUCTS_FILE = "products.txt"
SUPPLIERS_FILE = "suppliers.txt"
ORDERS_FILE = "orders.txt"


# Function to load data from a file
def load_data(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]
    except FileNotFoundError:
        return []


# Function to save data to a file
def save_data(file_path, data):
    with open(file_path, "w") as file:
        file.writelines([",".join(map(str, record)) + "\n" for record in data])


# Function to add a new product
def add_product():
    products = load_data(PRODUCTS_FILE)
    product_id = input("Enter Product ID: ")
    name = input("Enter Product Name: ")
    description = input("Enter Product Description: ")
    price = input("Enter Product Price: ")
    stock = input("Enter Product Stock: ")

    products.append([product_id, name, description, price, stock])
    save_data(PRODUCTS_FILE, products)
    print("Product added successfully!")


# Function to add a new supplier
def add_supplier():
    suppliers = load_data(SUPPLIERS_FILE)
    supplier_id = input("Enter Supplier ID: ")
    name = input("Enter Supplier Name: ")
    contact = input("Enter Supplier Contact: ")

    suppliers.append([supplier_id, name, contact])
    save_data(SUPPLIERS_FILE, suppliers)
    print("Supplier added successfully!")


# Function to display inventory
def view_inventory():
    products = load_data(PRODUCTS_FILE)
    if not products:
        print("No products available.")
        return
    print("\nCurrent Inventory:")
    print("ID | Name | Description | Price | Stock")
    print("-" * 40)
    for product in products:
        print(" | ".join(product))

def place_order():
    products = load_data(PRODUCTS_FILE)
    orders = load_data(ORDERS_FILE)

    # Display available products
    print("\nAvailable Products:")
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Stock: {product[4]}")

    # Get order details
    order_id = input("Enter Order ID: ")
    product_id = input("Enter Product ID: ")
    quantity = int(input("Enter Quantity: "))
    order_date = input("Enter Order Date (YYYY-MM-DD): ")

    # Validate product availability
    product_found = False
    for product in products:
        if product[0] == product_id:
            product_found = True
            stock = int(product[4])
            if stock >= quantity:
                product[4] = str(stock - quantity)  # Update stock
                orders.append([order_id, product_id, str(quantity), order_date])
                save_data(ORDERS_FILE, orders)
                save_data(PRODUCTS_FILE, products)
                print("Order placed successfully!")
            else:
                print("Insufficient stock to place the order.")
            break

    if not product_found:
        print("Product ID not found. Please try again.")

# Function to display the menu and handle user input
def display_menu():
    while True:
        print("\nInventory Management System")
        print("1. Add a New Product")
        print("2. Add a New Supplier")
        print("3. View Inventory")
        print("4. Place an Order")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            add_supplier()
        elif choice == "3":
            view_inventory()
        elif choice == "4":
            place_order()  # Call place_order function
        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# Initialize the program
display_menu()
