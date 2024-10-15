import tkinter as Tk
from tkinter import messagebox
import db_interface  

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Inventory Management System")
        self.master.geometry("600x500")  
        self.center_window()
        self.master.configure(bg="#d3d3d3")  

        # Title
        self.lb_title = Tk.Label(master, text="Inventory Management System", font=('Helvetica', 18, 'bold'), bg="#6c757d", fg="white", padx=10, pady=10)
        self.lb_title.pack(fill='x')

        # Create a frame for input fields with padding
        self.input_frame = Tk.Frame(master, bg="#d3d3d3")
        self.input_frame.pack(pady=20)

        # Item name
        self.create_label_and_entry("Item Name", 0)
        # Buy price
        self.create_label_and_entry("Buy Price", 1)
        # Sell price
        self.create_label_and_entry("Sell Price", 2)
        # Quantity
        self.create_label_and_entry("Quantity", 3)

        # Frame for buttons
        self.button_frame = Tk.Frame(master, bg="#d3d3d3")
        self.button_frame.pack(pady=10)

        # Submit button
        self.btn_submit = Tk.Button(self.button_frame, text="Add Item", font=('Helvetica', 12), bg="#6c757d", fg="white", command=self.submit_to_db)
        self.btn_submit.grid(row=0, column=0, padx=5)

        # Remove Item Section
        self.lb_remove = Tk.Label(master, text="Remove Item", font=('Helvetica', 16), bg="#d3d3d3")
        self.lb_remove.pack(pady=10)

        self.txt_item_to_remove = Tk.Entry(master, font=('Helvetica', 12))
        self.txt_item_to_remove.pack(pady=5)

        # Remove button (now under the remove input)
        self.btn_remove = Tk.Button(master, text="Remove Item", font=('Helvetica', 12), bg="#6c757d", fg="white", command=self.remove_item)
        self.btn_remove.pack(pady=5)

        # View Items Section
        self.btn_view = Tk.Button(self.button_frame, text="View Items", font=('Helvetica', 12), bg="#6c757d", fg="white", command=self.view_items)
        self.btn_view.grid(row=0, column=1, padx=5)

        # Footer
        self.footer = Tk.Label(master, text="© 2024 Inventory Management", bg="#d3d3d3", fg="#6c757d")
        self.footer.pack(side='bottom', pady=10)

    def create_label_and_entry(self, text, row):
        label = Tk.Label(self.input_frame, text=text, font=('Helvetica', 12), bg="#d3d3d3")
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry = Tk.Entry(self.input_frame, font=('Helvetica', 12), bd=2, relief='solid')
        entry.grid(row=row, column=1, padx=10, pady=5)
        setattr(self, f'txt_{text.replace(" ", "_").lower()}', entry) 

    def center_window(self):
        """Centers the window on the screen."""
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        position_right = int(self.master.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.master.winfo_screenheight() / 2 - window_height / 2)
        self.master.geometry(f"+{position_right}+{position_down}")

    def submit_to_db(self):
        item_name = self.txt_item_name.get()
        try:
            buy_price = float(self.txt_buy_price.get())
            sell_price = float(self.txt_sell_price.get())
            quantity = int(self.txt_quantity.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for prices and quantity.")
            return

        # Write to the database
        db_interface.write_to_database(item_name, buy_price, sell_price, quantity)

        # Clear input fields after submission
        self.clear_inputs()
        messagebox.showinfo("Success", f"Item '{item_name}' added successfully!")

    def remove_item(self):
        item_name = self.txt_item_to_remove.get().strip()
        if not item_name:
            messagebox.showerror("Invalid Input", "Please enter an item name to remove.")
            return
        
        # Remove from the database
        success = db_interface.remove_from_database(item_name)

        if success:
            messagebox.showinfo("Success", f"Item '{item_name}' removed successfully!")
            self.txt_item_to_remove.delete(0, Tk.END)  
        else:
            messagebox.showerror("Error", f"Item '{item_name}' not found.")

    def view_items(self):
        items = db_interface.read_from_database()
        if not items:
            messagebox.showinfo("Items", "No items in inventory.")
            return

        # Create a new window to display items
        view_window = Tk.Toplevel(self.master)
        view_window.title("Current Inventory")
        view_window.geometry("500x300")

        lb_items = Tk.Listbox(view_window, font=('Helvetica', 12), bd=2, relief='solid')
        lb_items.pack(fill='both', expand=True, padx=10, pady=10)

        for row in items[1:]:  # Skip the header
            lb_items.insert(Tk.END, f"ID: {row[0]}, Name: {row[1]}, Buy Price: {row[2]}, Sell Price: {row[3]}, Quantity: {row[4]}")

    def clear_inputs(self):
        """Clears all input fields."""
        for attr in ['item_name', 'buy_price', 'sell_price', 'quantity']:
            getattr(self, f'txt_{attr}').delete(0, Tk.END)

# Run the application
root = Tk.Tk()
my_gui = MainWindow(root)
root.mainloop()
