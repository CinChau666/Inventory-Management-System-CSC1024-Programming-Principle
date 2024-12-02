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

def update_product():
    products = load_data(PRODUCTS_FILE)

    # Display available products
    print("\nAvailable Products:")
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Price: {product[3]}, Stock: {product[4]}")

    # Get the Product ID to update
    product_id = input("Enter Product ID to update: ")
    product_found = False

    for product in products:
        if product[0] == product_id:
            product_found = True
            print("\nCurrent Details:")
            print(f"Name: {product[1]}")
            print(f"Description: {product[2]}")
            print(f"Price: {product[3]}")
            print(f"Stock: {product[4]}")

            # Get updated details
            name = input("Enter new Name (leave blank to keep current): ") or product[1]
            description = input("Enter new Description (leave blank to keep current): ") or product[2]
            price = input("Enter new Price (leave blank to keep current): ") or product[3]
            stock = input("Enter new Stock (leave blank to keep current): ") or product[4]

            # Update the product details
            product[1], product[2], product[3], product[4] = name, description, price, stock
            save_data(PRODUCTS_FILE, products)
            print("Product updated successfully!")
            break

    if not product_found:
        print("Product ID not found. Please try again.")

# Function to add a new supplier
def add_supplier():
    suppliers = load_data(SUPPLIERS_FILE)
    suppliers.append(["Supplier ID " "|" " Name " "|" " Contact "])
    supplier_id = input("Enter Supplier ID: ")
    name = input("Enter Supplier Name: ")
    contact = input("Enter Supplier Contact: ")

    suppliers.append([f"{supplier_id} | {name} | {contact}"])
    
    save_data(SUPPLIERS_FILE, suppliers)
    print("Supplier added successfully!")

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




def generate_reports():
    print("\nReport Options:")
    print("1. Low Stock Items")
    print("2. Product Sales")
    print("3. Supplier Orders")
    report_choice = input("Enter your choice: ")

    if report_choice == "1":
        generate_low_stock_report()
    elif report_choice == "2":
        generate_product_sales_report()
    elif report_choice == "3":
        generate_supplier_orders_report()
    else:
        print("Invalid choice. Returning to the main menu.")


# Function to generate low stock report
def generate_reports():
    print("\nReport Options:")
    print("1. Low Stock Items")
    print("2. Product Sales")
    print("3. Supplier Orders")
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
    products = load_data(PRODUCTS_FILE)
    suppliers = load_data(SUPPLIERS_FILE)
    orders = load_data(ORDERS_FILE)

    # Create a product-to-supplier mapping
    product_to_supplier = {}
    for product in products:
        product_id = product[0]
        supplier_id = product[1]  # Assuming the second column is supplier ID
        product_to_supplier[product_id] = supplier_id

    # Aggregate orders by supplier
    supplier_orders = {}
    for order in orders:
        product_id = order[1]
        quantity = int(order[2])
        supplier_id = product_to_supplier.get(product_id, "Unknown")
        supplier_orders[supplier_id] = supplier_orders.get(supplier_id, 0) + quantity

    print("\nSupplier Orders Report:")
    print("Supplier ID | Total Orders")
    print("-" * 30)
    for supplier_id, total_orders in supplier_orders.items():
        print(f"{supplier_id} | {total_orders}")
    print("-" * 30)


# Function to display the menu and handle user input
def display_menu():
    while True:
        print("\nInventory Management System")
        print("1. Add a New Product")
        print("2. Update Product Details")
        print("3. Add a new Supplier")
        print("4. Place an Order")
        print("5. View Inventory")  
        print("6. Generate Reports")
        print("7. Exit")
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
