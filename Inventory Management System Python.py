import os

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
    # Check if file exists and contains a header
    if not os.path.exists(PRODUCTS_FILE) or os.path.getsize(PRODUCTS_FILE) == 0:
        # File doesn't exist or is empty, so write the header
        with open(PRODUCTS_FILE, "w") as f:
            f.write("Product ID, Name, Description, Price, Stock\n")

    # Append a new product
    product_id = input("Enter Product ID: ")
    name = input("Enter Product Name: ")
    description = input("Enter Product Description: ")
    price = float(input("Enter Product Price: "))
    stock = int(input("Enter Product Stock: "))

    with open(PRODUCTS_FILE, "a") as f:
        f.write(f"{product_id}, {name}, {description}, {price}, {stock}\n")

    print("Product added successfully!")

def update_product():
    
    products = load_data(PRODUCTS_FILE)

    if len(products) <= 1:  # Check if there's no data or only the header row
        print("No products available to update.")
        return

    # Display available products
    print("\nAvailable Products:")

    # Get the Product ID to update
    product_found = False
    print("ID | Name | Description | Price | Stock")
    
    for product in products[1:]:      # Skip the header row (products[0])
        print(f"{product[0]} | {product[1]} | {product[2]} | {product[3]} | {product[4]}")

    product_id = input("\nEnter the Product ID of the product you want to update: ")

    for index, product in enumerate(products):
        if product[0] == product_id:
            print(f"Current details: {product}")
            new_name = input("Enter New Product Name (leave blank to keep current): ") or product[1] 
            new_description = input("Enter New Product Description (leave blank to keep current): ") or product[2]
            new_price = float(input("Enter New Product Price (leave blank to keep current): ")) or product[3]
            new_stock = int(input("Enter New Product Stock (leave blank to keep current): ")) or product[4]

            # Update the product details
            products[index] = [product[0], new_name, new_description, new_price, new_stock]
            save_data(PRODUCTS_FILE, products)
            print("Product details updated successfully!")

    if not product_found:
        print("Product ID not found. Please try again.")

# Function to add a new supplier
def add_supplier():
    # Check if file exists and contains a header
    if not os.path.exists(SUPPLIERS_FILE) or os.path.getsize(SUPPLIERS_FILE) == 0:
        # File doesn't exist or is empty, so write the header
        with open(SUPPLIERS_FILE, "w") as f:
            f.write("Supplier ID | Name | Contact\n")

    # Append a new supplier
    supplier_id = input("Enter Supplier ID: ")
    name = input("Enter Supplier Name: ")
    contact = input("Enter Supplier Contact: ")

    with open(SUPPLIERS_FILE, "a") as f:
        f.write(f"{supplier_id} | {name} | {contact}\n")

    print("Supplier added successfully!")

# Function to place order
def place_order():
    # Check if file exists and contains a header
    if not os.path.exists(ORDERS_FILE) or os.path.getsize(ORDERS_FILE) == 0:
        # File doesn't exist or is empty, so write the header
        with open(ORDERS_FILE, "w") as f:
            f.write("Order ID | Product ID | Quantity | Order Date\n")

    # Display available products
    products = load_data(PRODUCTS_FILE)
    if not products:
        print("No products available for ordering.")
        return

    print("\nAvailable Products:")
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Stock: {product[4]}")

    # Get order details
    order_id = input("Enter Order ID: ")
    product_id = input("Enter Product ID: ")
    quantity = int(input("Enter Quantity: "))
    order_date = input("Enter Order Date (YYYY-MM-DD): ")

    # Validate product availability
    # product[0] = Product ID
    # product[1] = Name
    # product[2] = Description
    # product[3] = Price
    # product[4] = Stock

    product_found = False
    for product in products:
        if product[0] == product_id:
            product_found = True
            stock = int(product[4])
            if stock >= quantity:
                product[4] = str(stock - quantity)  # Update stock
                save_data(PRODUCTS_FILE, products)  # Save updated inventory

                # Append the new order to the file
                with open(ORDERS_FILE, "a") as f:
                    f.write(f"{order_id}, {product_id}, {quantity}, {order_date}\n")

                print("Order placed successfully!")
            else:
                print(f"Insufficient stock. Only {stock} units available.")
            break

    if not product_found:
        print("Product ID not found. Please try again.")

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

# Function to generate low stock report
def generate_reports():
    print("\nReport Options:\n1. Low Stock Items\n2. Product Sales\n3. Supplier Orders")
    report_choice = input("Enter your choice: ")

    if report_choice == "1":
        generate_low_stock_report()
    elif report_choice == "2":
        generate_product_sales_report()
    elif report_choice == "3":
        generate_supplier_orders_report()
    else:
        print("Invalid choice. Returning to the main menu.")

def generate_low_stock_report():
    products = load_data(PRODUCTS_FILE)
    threshold = int(input("Enter stock threshold: "))
    print("\nLow Stock Items:")
    print("ID | Name | Stock")
    print("-" * 30)
    for product in products:
        if int(product[4]) < threshold:
            print(f"{product[0]} | {product[1]} | {product[4]}")
    print("-" * 30)


# Function to generate product sales report
def generate_product_sales_report():
    orders = load_data(ORDERS_FILE)
    product_sales = {}

    for order in orders:
        product_id = order[1]
        quantity = int(order[2])
        product_sales[product_id] = product_sales.get(product_id, 0) + quantity

    print("\nProduct Sales Report:")
    print("Product ID | Quantity Sold")
    print("-" * 30)
    for product_id, total_sold in product_sales.items():
        print(f"{product_id} | {total_sold}")
    print("-" * 30)

# Function to generate supplier orders report
def generate_supplier_orders_report():
    try:
        products = load_data(PRODUCTS_FILE)
        suppliers = load_data(SUPPLIERS_FILE)
        orders = load_data(ORDERS_FILE)

        if not products or not suppliers or not orders:
            print("Error: Missing or incomplete data in one or more files.")
            return

        # Create a product-to-supplier mapping
        product_to_supplier = {}
        for product in products[1:]:  # Skip the header row
            if len(product) < 2:  # Ensure product row has enough columns
                print(f"Warning: Malformed product entry skipped: {product}")
                continue
            product_id = product[0]
            supplier_id = product[1]  # Assuming the second column is supplier ID
            product_to_supplier[product_id] = supplier_id

        # Aggregate orders by supplier
        supplier_orders = {}
        for order in orders[1:]:  # Skip the header row
            if len(order) < 3:  # Ensure order row has enough columns
                print(f"Warning: Malformed order entry skipped: {order}")
                continue
            product_id = order[1]
            try:
                quantity = int(order[2])  # Ensure quantity is an integer
            except ValueError:
                print(f"Warning: Invalid quantity in order skipped: {order}")
                continue

            supplier_id = product_to_supplier.get(product_id, "Unknown")
            supplier_orders[supplier_id] = supplier_orders.get(supplier_id, 0) + quantity

        # Display the report
        print("\nSupplier Orders Report:")
        print("Supplier ID | Total Orders")
        print("-" * 30)
        for supplier_id, total_orders in supplier_orders.items():
            print(f"{supplier_id} | {total_orders}")
        print("-" * 30)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Function to display the menu and handle user input
def display_menu():
    while True:
        print("*" * 38)
        print("|  Inventory Management System       |")
        print("|  1. Add a New Product              |")
        print("|  2. Update Product Details         |")
        print("|  3. Add a New Supplier             |")
        print("|  4. Place an Order                 |")
        print("|  5. View Inventory                 |")
        print("|  6. Generate Reports               |")
        print("|  7. Exit                           |")
        print("*" * 38)
        choice = input("Enter your choice: ")

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
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Initialize the program
display_menu()
