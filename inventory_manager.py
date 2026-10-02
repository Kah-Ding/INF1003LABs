INVENTORY_FILE = "lab_inventory/inventory.json"
LINE = "-" * 48


def to_json(inventory):
    if not inventory:
        return "[]"
    lines = []
    for item in inventory:
        product_id = item["id"].replace("\\", "\\\\").replace('"', '\\"')
        name = item["name"].replace("\\", "\\\\").replace('"', '\\"')
        lines.append(
            f'    {{"id": "{product_id}", "name": "{name}", '
            f'"price": {item["price"]:.2f}, "stock": {item["stock"]}}}'
        )
    return "[\n" + ",\n".join(lines) + "\n]\n"


def from_json(text):
    data = eval(text, {"__builtins__": {}}, {"true": True, "false": False, "null": None})
    inventory = []
    for item in data:
        inventory.append({
            "id": str(item["id"]),
            "name": str(item["name"]),
            "price": float(item["price"]),
            "stock": int(item["stock"]),
        })
    return inventory


def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as file:
            text = file.read()
    except FileNotFoundError:
        print("inventory.json not found.")
        print("Starting with an empty inventory.")
        return []

    print("inventory.json found.")
    try:
        inventory = from_json(text) if text.strip() else []
        print("Inventory loaded successfully.")
        return inventory
    except Exception:
        print("inventory.json could not be read.")
        print("Starting with an empty inventory.")
        return []


def save_inventory(inventory):
    try:
        with open(INVENTORY_FILE, "w") as file:
            file.write(to_json(inventory))
        return True
    except OSError:
        print(f"Unable to save to {INVENTORY_FILE}.")
        return False


def find_product(inventory, product_id):
    for item in inventory:
        if item["id"].upper() == product_id.upper():
            return item
    return None


def get_price(prompt):
    while True:
        value = input(prompt).strip()
        try:
            price = float(value)
            if price < 0:
                print("Price cannot be negative.")
            else:
                return price
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def get_stock(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        if value.startswith("-"):
            print("Negative values are not allowed.")
        else:
            print("Invalid input. Please enter a whole number.")


def display_all(inventory):
    print("\nCurrent Inventory")
    print(LINE)
    if not inventory:
        print("No products in inventory.")
    for item in inventory:
        print(f"ID: {item['id']} | Name: {item['name']} | "
              f"Price: ${item['price']:.2f} | Stock: {item['stock']}")
    print(LINE)


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if find_product(inventory, product_id):
        print(f"Product ID {product_id} already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    price = get_price("Price: ")
    stock = get_stock("Stock Quantity: ")

    inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    item = find_product(inventory, product_id)
    if not item:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {item['name']}")
    print(f"Current Stock: {item['stock']}")
    item["stock"] = get_stock("New Stock Quantity: ")
    print("Stock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    item = find_product(inventory, product_id)
    if not item:
        print("Product not found.")
        return

    print("Product Found")
    print(LINE)
    print(f"ID: {item['id']}")
    print(f"Name: {item['name']}")
    print(f"Price: ${item['price']:.2f}")
    print(f"Stock: {item['stock']}")
    print(LINE)


def save_option(inventory):
    print("\nSaving inventory...")
    if save_inventory(inventory):
        print("Inventory saved successfully to inventory.json.")


def exit_program(inventory):
    print("\nSaving inventory before exit...")
    if save_inventory(inventory):
        print("Inventory saved successfully.")
    print("Thank you for using Inventory Management System.")
    print("Program terminated.")


def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40 + "\n")

    inventory = load_inventory()

    actions = {
        "1": display_all,
        "2": add_product,
        "3": update_stock,
        "4": search_product,
        "5": save_option,
    }

    while True:
        show_menu()
        choice = input("Enter option: ").strip()
        if choice == "6":
            exit_program(inventory)
            break
        elif choice in actions:
            actions[choice](inventory)
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
