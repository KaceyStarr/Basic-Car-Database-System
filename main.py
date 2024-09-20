import sqlite3
import tkinter as tk
from tkinter import messagebox

#creating a database and connect to SQL
conn = sqlite3.connect('car_database.db')
cursor = conn.cursor()


#assuming the cars table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL
    )
''')
conn.commit()



#This functions allows the user to add a new car to the database
# Function to add a new car to the database
def add_car():
    make = make_entry.get()
    model = model_entry.get()
    year = year_entry.get()

    if make and model and year:
        cursor.execute("INSERT INTO cars (make, model, year) VALUES (?, ?, ?)", (make, model, year))
        conn.commit()
        messagebox.showinfo("Success", "Car added successfully!")
        clear_entries()
        display_cars()
    else:
        messagebox.showerror("Error", "Please fill out all fields")


#This function deletes a car from the databse by its ID
def delete_car():
    car_id = id_entry.get()
    if car_id:
        cursor.execute("DELETE FROM cars WHERE id=?", (car_id,))
        conn.commit()
        messagebox.showinfo("Success", "Car deleted sucessfully!")
        display_cars()
    else:
        messagebox.showerror("Error", "Please enter a valid car ID")


#This function displays car in the listbox
def display_cars():
    cursor.execute("SELECT * FROM cars")  # Corrected 'excute' to 'execute'
    cars = cursor.fetchall()
    car_listbox.delete(0, tk.END)  # Clear the listbox

    for car in cars:
        car_listbox.insert(tk.END, f"ID: {car[0]}, Make: {car[1]}, Model: {car[2]}, Year: {car[3]}")



#This functions CLears entry fields
# Function to clear entry fields
def clear_entries():
    make_entry.delete(0, tk.END)
    model_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    id_entry.delete(0, tk.END)

#GUI Setup
root = tk.Tk()
root.title("Car Database Management")

# Labels
make_label = tk.Label(root, text="Make:")
make_label.grid(row=0, column=0)
model_label = tk.Label(root, text="Model:")
model_label.grid(row=1, column=0)
year_label = tk.Label(root, text="Year:")
year_label.grid(row=2, column=0)

# Entries
make_entry = tk.Entry(root)
make_entry.grid(row=0, column=1)
model_entry = tk.Entry(root)
model_entry.grid(row=1, column=1)
year_entry = tk.Entry(root)
year_entry.grid(row=2, column=1)

# Buttons
add_button = tk.Button(root, text="Add Car", command=add_car)
add_button.grid(row=3, column=1)
delete_button = tk.Button(root, text="Delete Car", command=delete_car)
delete_button.grid(row=4, column=1)

# Car List
car_listbox = tk.Listbox(root, width=50, height=10)
car_listbox.grid(row=5, column=0, columnspan=3)

# ID Entry for Deletion
id_label = tk.Label(root, text="ID to Delete:")
id_label.grid(row=6, column=0)
id_entry = tk.Entry(root)
id_entry.grid(row=6, column=1)

# Show cars when starting
display_cars()

# Run the GUI
root.mainloop()

# Close database connection when done
conn.close()