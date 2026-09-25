def load_inventory():
    inventory = []
    order_id = 1001
    try:
        with open("inventory.txt", "r") as file:
            for line in file:
                order_data = line.strip().split(", ")
                inventory.append(order_data)
    except FileNotFoundError:
        print("\nCurrent Inventory:\n NIL\n")
        return inventory, order_id

    print("\nCurrent Inventory:\n")
    for order in inventory:
        print(", ".join(order))
    if inventory:
        order_id = int(inventory[-1][0]) + 1
    print("\n")
    return inventory,order_id

def save_inventory(order):
    with open("inventory.txt", "a") as file:
        file.write(str(order))
    print("\nNew Order Added:")
    print(f"{order}\n")
    print("Order successfully saved to inventory.txt")

def get_valid_input():
    inventory=0
    failed=0
    tax_amount=0

    while True:
        stocks=0
        inventory, order_id = load_inventory()
        product_name=input("Enter the product name or type 'quit' to exit: ")
        if product_name.lower() != 'quit':
            stocks = input("Enter the current stock count: ")
            if stocks.isdigit():
                original_stocks =0
                for order in inventory:
                    if order[1].lower() == product_name.lower():
                        order_id = int(order[0])
                        product_name = order[1]
                        original_stocks=int(order[2])
                        break
                stocks=process_delivery(original_stocks,stocks)
                tax_amount=calculate_tax(stocks)
                print(f"Tax amount for this delivery: {tax_amount}")
                if stocks > 500:
                    print("Inventory limit exceeded! Inventory cannot exceed 500 units. Inventory:",stocks)
                    break
                else:
                    new_order=f"{order_id}, {product_name}, {stocks}, ${tax_amount}\n"
        else:
            if product_name == 'q' or product_name =="quit":
                save_inventory(new_order)
                generate_report(new_order,failed)
                break
            print("Invalid input. Please enter a numeric value.")
            failed += 1
            if "-" in stocks:
                print("Negative values are not allowed.")

def process_delivery(current_total,new_value):
    new_value=int(new_value)
    return current_total+new_value

def calculate_tax(amount):
    return round(float(amount) * 0.10, 2)

def generate_report(total_units,failed_attempts):
    print("Appended:", total_units,"\nNumber of failed/invalid entries: ", failed_attempts)

get_valid_input()