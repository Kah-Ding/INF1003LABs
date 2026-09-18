def get_valid_input():
    inventory=0
    stocks=0
    failed=0
    tax_amount=0

    while True:
        stocks = input("Enter the current stock count or type quit to exit: ")
        if stocks.isdigit():
            inventory=process_delivery(inventory,stocks)
            tax_amount+=calculate_tax(stocks)
            print(f"Tax amount for this delivery: {tax_amount}")
            if inventory > 500:
                print("Inventory limit exceeded! Inventory cannot exceed 500 units. Inventory:",inventory)
                break
            print("Inventory has been updated.")
        else:
            if stocks == 'q' or stocks =="quit":
                generate_report(inventory,failed)
                break
            print("Invalid input. Please enter a numeric value.")
            failed += 1
            if "-" in stocks:
                print("Negative values are not allowed.")

def process_delivery(current_total,new_value):
    new_value=int(new_value)
    return current_total+new_value

def calculate_tax(amount):
    return int(amount)*0.10

def generate_report(total_units,failed_attempts):
    print("Total Units Processed:", total_units,"\nNumber of failed/invalid entries: ", failed_attempts)

get_valid_input()