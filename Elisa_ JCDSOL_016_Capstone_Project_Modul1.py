from tabulate import tabulate

# Inisiasi table data warehouse.
data_warehouse = {
    1: {"fuel_type": "pertalite", "stock": 5000, "location": "Gudang A", "demand": 3000, "delivery": 2000, "purchase_price": 7000, "selling_price": 7650},
    2: {"fuel_type": "pertamax", "stock": 3000, "location": "Gudang B", "demand": 1500, "delivery": 1000, "purchase_price": 9000, "selling_price": 9650},
    3: {"fuel_type": "solar", "stock": 7000, "location": "Gudang C", "demand": 4000, "delivery": 3500, "purchase_price": 5000, "selling_price": 5650},
    4: {"fuel_type": "dexlite", "stock": 2000, "location": "Gudang D", "demand": 1000, "delivery": 800, "purchase_price": 10500, "selling_price": 11250},
    5: {"fuel_type": "premium", "stock": 6000, "location": "Gudang E", "demand": 3500, "delivery": 3000, "purchase_price": 6500, "selling_price": 7150},
    6: {"fuel_type": "pertamax turbo", "stock": 1500, "location": "Gudang F", "demand": 800, "delivery": 700, "purchase_price": 12000, "selling_price": 12750},
    7: {"fuel_type": "bio solar", "stock": 4000, "location": "Gudang G", "demand": 2500, "delivery": 2000, "purchase_price": 5500, "selling_price": 6150},
    8: {"fuel_type": "avtur", "stock": 10000, "location": "Gudang H", "demand": 6000, "delivery": 5000, "purchase_price": 8000, "selling_price": 8650},
    9: {"fuel_type": "minyak tanah", "stock": 500, "location": "Gudang I", "demand": 300, "delivery": 200, "purchase_price": 4500, "selling_price": 5150},
    10: {"fuel_type": "gas lpg", "stock": 2500, "location": "Gudang J", "demand": 1500, "delivery": 1200, "purchase_price": 15000, "selling_price": 15750}
}

# Dua fungsi ini digunakan untuk error handling input untuk input Integer dan Float
def get_valid_int(prompt, allow_negative=False, default=None):
    while True:
        try:
            value = input(prompt)
            if value == '' and default is not None:
                return default  # Return default apabila input kosong
            value = int(value)
            if not allow_negative and value < 0:   # Handling nilai negatif
                print("Value cannot be negative.")
            else:
                return value   
        except ValueError:      # Handling apabila input bukan angka/numeric
            print("Invalid input, please enter a number.")

def get_valid_float(prompt, allow_negative=False, default=None):
    while True:
        try:
            value = input(prompt)
            if value == '' and default is not None:
                return default
            value = float(value)
            if not allow_negative and value < 0:
                print("Value cannot be negative.")
            else:
                return value
        except ValueError:
            print("Invalid input, please enter a valid number.")

# Create new fuel record
def create_record():
    id = get_valid_int("Enter new fuel ID: ")
    if id in data_warehouse:      # Handling apabila ID sudah terdaftar
        print(f"ID {id} already exists. Use Update instead.")
        return
    
    # handling fuel type tidak case sensitive
    fuel_type = input("Enter fuel type: ").lower()
    
    # Check apakah fuel type sudah terdapat di table utama
    for record in data_warehouse.values():
        if record['fuel_type'] == fuel_type:
            print(f"Fuel type '{fuel_type}' already exists with a different ID. Use Update instead.")
            return

    stock = get_valid_int("Enter fuel Stock quantity (in liters): ")
    location = input("Enter warehouse location: ")
    demand = get_valid_int("Enter fuel demand (in liters): ")
    delivery = get_valid_int("Enter fuel delivery (in liters): ")
    
    # Pengiriman tidak boleh lebih besar dari permintaan
    if delivery > demand:
        print("Delivery cannot exceed demand.")
        return
    
    purchase_price = get_valid_float("Enter purchase price per liter: ")
    selling_price = get_valid_float("Enter selling price per liter: ")

    # Membuat record baru jika semua inputan valid
    data_warehouse[id] = {
        'fuel_type': fuel_type,
        'stock': stock,
        'location': location,
        'demand': demand,
        'delivery': delivery,
        'purchase_price': purchase_price,
        'selling_price': selling_price
    }
    
    print(f"Fuel record with ID {id} created successfully.")


# Digunakan untuk menu read record, akan menampilkan table saat ini.
def view_all_stock():
    if not data_warehouse:
        print("No records available.")
        return
    headers = ["ID", "Fuel Type", "stock", "location", "demand", "delivery", "Purchase Price", "Selling Price"]
    data = [[id, v['fuel_type'], v['stock'], v['location'], v['demand'], v['delivery'], v['purchase_price'], v['selling_price']] for id, v in data_warehouse.items()]
    print(tabulate(data, headers, tablefmt="grid"))

# Untuk update record yang sudah ada
def update_record():
    id = get_valid_int("Enter ID to update: ")
    if id not in data_warehouse:            # Handling apabila ID tidak terdaftar di table
        print(f"ID {id} does not exist. Please create the record first.")
        return

    print(f"Fuel Type: {data_warehouse[id]['fuel_type']}")
    print("Enter changes for the following fields (leave blank to skip):")

    # Validasi dan update stock, yang diinput adalah nilai total akhir setelah pembaharuan, bukan besarnya penambahan nilai
    # Validasi input update stock dengan menggunakan fungsi get_valid yang sudah didefinisikan di atas dengan mengatur,
    # nilai parameter 'default' dari fungsi get_valid menjadi nilai dari stock saat ini.
    # Sehingga ketika user skip atau mengosongkan inputan, maka nilai stock akan sama dengan nilai sebelumnya,
    # alias tidak ada perubahan/update. Berlaku juga untuk parameter lain seperti demand, delivery, dll.
    stock_change = get_valid_int(f"New Stock quantity (current: {data_warehouse[id]['stock']}): ", default=data_warehouse[id]['stock'])

    # Update lokasi
    location = input(f"New warehouse location (current: {data_warehouse[id]['location']}): ") or data_warehouse[id]['location']

    # Validasi dan update demand
    demand_change = get_valid_int(f"New demand (current: {data_warehouse[id]['demand']}): ", default=data_warehouse[id]['demand'])

    # Validasi dan update delivery
    while True:
        delivery_change = get_valid_int(f"New delivery (current: {data_warehouse[id]['delivery']}): ", default=data_warehouse[id]['delivery'])
        if delivery_change > demand_change:
            print("Error: Delivery cannot exceed demand. Try again.")
        else:
            break

    # Validasi dan update purchase price
    purchase_price_change = get_valid_float(f"New purchase price (current: {data_warehouse[id]['purchase_price']}): ", default=data_warehouse[id]['purchase_price'])

    # Validasi dan update selling price
    selling_price_change = get_valid_float(f"New selling price (current: {data_warehouse[id]['selling_price']}): ", default=data_warehouse[id]['selling_price'])

    # Terapkan pembaruan
    data_warehouse[id]['stock'] = stock_change
    data_warehouse[id]['location'] = location
    data_warehouse[id]['demand'] = demand_change
    data_warehouse[id]['delivery'] = delivery_change
    data_warehouse[id]['purchase_price'] = purchase_price_change
    data_warehouse[id]['selling_price'] = selling_price_change

    print(f"Record with ID {id} updated successfully.")


# Delete record dari table
def delete_record():
    id = get_valid_int("Enter ID to delete: ")
    if id in data_warehouse:
        del data_warehouse[id]
        print(f"Record with ID {id} deleted successfully.")
    else:
        print(f"ID {id} not found.")

# Mendapatkan top 5 bahan bakar dengan revenue tertinggi
def top_5_revenue():
    revenue_data = [(id, data['fuel_type'], (data['selling_price'] - data['purchase_price']) * data['delivery']) for id, data in data_warehouse.items()]
    top_5 = sorted(revenue_data, key=lambda x: x[2], reverse=True)[:5]
    headers = ["ID", "Fuel Type", "Revenue"]
    print(tabulate(top_5, headers, tablefmt="grid"))

# Menampilkan bahan bakar apa saja yang harus direstock dengan threshold sebesar 200
def display_restock():
    threshold = 200
    print(f"Note: Threshold yang digunakan adalah {threshold}")
    
    # Menyaring semua data yang perlu di-restock
    restock_data = [
        (id, data['fuel_type'], data['stock'], data['demand']) 
        for id, data in data_warehouse.items() 
        if data['demand'] > data['stock'] - threshold
    ]
    
    # Menampilkan tabel dengan kolom ID, Fuel Type, Stock saat ini, dan Demand saat ini
    if restock_data:
        print(tabulate(restock_data, ["ID", "Fuel Type", "Current Stock", "Current Demand"], tablefmt="grid"))
    else:
        print("No fuel needs to be restocked based on current thresholds.")


# Menampilkan menu help yang akan menjelaskan fungsi dari setiap menu
def show_help():
    help_text = """
    1. Create Record: Adds a new fuel record in the DWH. The ID must be unique.
    2. Read Record: Displays all fuel data in table format.
    3. Update Record: Updates fuel data in the DWH based on the ID. Enter new values or leave blank to skip.
    4. Delete Record: Deletes a fuel record from the DWH based on the ID.
    5. Top 5 Revenue: Shows the top 5 fuels with the highest revenue based on deliveries.
    6. Top 5 Restock: Shows the top 5 fuels that are close to running out and need to be restocked soon.
    7. Exit: Exit the program.
    """
    print(help_text)


# Fungsi menu utama
def menu():
    while True:
        print("\nWarehouse Management System")
        print("1. Create Record")
        print("2. Read Record")
        print("3. Update Record")
        print("4. Delete Record")
        print("5. Top 5 Revenue")
        print("6. Must Restock")
        print("7. Help")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            create_record()
        elif choice == '2':
            view_all_stock()
        elif choice == '3':
            update_record()
        elif choice == '4':
            delete_record()
        elif choice == '5':
            top_5_revenue()
        elif choice == '6':
            display_restock()
        elif choice == '7':
            show_help()
        elif choice == '8':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# menggunakan if __name__ == '__main__' untuk menjalankan kode karna best practice dan standar dari aplikasi/program Python.
# Salah satu tujuannya adalah ketika kita import script ini dari script lain, maka kode menu()/seluruh kode di bawah baris if,
# tidak akan dijalankan. Namun, ketika kita run script ini, maka menu() akan tetap dijalankan.
if __name__ == "__main__":
    menu()  