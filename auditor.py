inventory=0
stocks=0
while inventory==0:
    stocks = input("Enter the current stock count: ")
    if stocks.isdigit():
        print("Inventory is empty. Please restock.")
        stocks = int(input("Enter the new inventory count: "))