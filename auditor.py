inventory=0
stocks=0

while True:
    stocks = input("Enter the current stock count or type quit to exit: ")
    if stocks.isdigit():
        inventory += int(stocks)
        print("Inventory has been updated.")
    else:
        if stocks == 'q' or stocks =="quit":
            break
        print("Invalid input. Please enter a numeric value.")
        if "-" in stocks:
            print("Negative values are not allowed.")