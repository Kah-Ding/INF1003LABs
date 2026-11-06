INVENTORY_FILE = "/app/lab_inventory/orders.txt"


def load_inventory():
    inventory = []
    orders=["1001, Wireless Mouse, 2\n",
    "1002, Keyboard, 1\n",
    "1003, USB Cable, 3\n"]    
    with open(INVENTORY_FILE, "a+") as file:
        if file.tell() == 0:
            file.writelines(orders)
        file.seek(0)
        for line in file:
            order_data = line.strip().split(", ")
            inventory.append(order_data)
    print("Current Orders:\n")
    for order in inventory:
        print(", ".join(order))
    order_id=int(inventory[-1][0].split(",")[0])+1
    print("\n")
    return inventory,order_id

def save_inventory(order):
    with open(INVENTORY_FILE, "a") as file:
        file.write(str(order))
    print(f"Order successfully saved to {INVENTORY_FILE}")

def get_valid_input():
    failed=0
    while True:
        inventory,order_id=load_inventory()
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
                    new_order=f"{order_id}, {product_name}, {stocks}\n"
            else:
                print("Invalid input. Please enter a numeric value.")
                failed += 1
                if "-" in stocks:
                    print("Negative values are not allowed.")
        else:
            if product_name == 'q' or product_name =="quit":
                print("\nNew Order Added:\n")
                print(new_order.rstrip()+"\n")
                save_inventory(new_order)
                generate_report(new_order,failed)
                break
            

def process_delivery(current_total,new_value):
    new_value=int(new_value)

    return current_total+new_value

def calculate_tax(amount):
    return float(amount)*0.10

def generate_report(total_units,failed_attempts):
    print("Total Units Processed:", total_units,"\nNumber of failed/invalid entries: ", failed_attempts)

get_valid_input()