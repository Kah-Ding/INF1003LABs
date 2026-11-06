inventory=0
stocks=0
failed=0

while True:
    print(f"Current inventory: {inventory}")
    stocks = input("Enter the current stock count or type quit to exit: ")
    if stocks.isdigit():
        inventory += int(stocks)
        if inventory > 500:
            print("Inventory limit exceeded! Inventory cannot exceed 500 units. Inventory:",inventory)
            break
        print("Inventory has been updated.")
    else:
        if stocks == 'q' or stocks =="quit":
            print("Total Units Processed:", inventory,"\nNumber of failed/invalid entries: ", failed)
            break
        print("Invalid input. Please enter a numeric value.")
        failed += 1
        if "-" in stocks:
            print("Negative values are not allowed.")