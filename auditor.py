inventory=0
stocks=0

while True:
    choice=input("Enter '1' to update inventory, '2' to check inventory, or 'q' to quit: ")
    if choice == '1':
        stocks = input("Enter the current stock count: ")
        if stocks.isdigit():
            inventory = int(stocks)
            print("Inventory has been updated.")
    elif choice == '2':
        print(f"Current inventory: {inventory}")
    elif choice == 'q' or choice =="quit":
        break
    else:
        print("Invalid choice. Please try again.")