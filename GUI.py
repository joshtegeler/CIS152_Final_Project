import tkinter as tk
from tkinter import ttk, messagebox
from main import Car, Inventory


class CarInventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Tracker")

        # Set the GUI to fit the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Instance of Inventory class
        self.inventory = Inventory(file_path='car_inventory.csv')
        self.inventory.load_data()

        # Creating GUI Elements
        self.listbox = tk.Listbox(root, width=50, height=15, font=("Arial", 12))
        self.label_year = tk.Label(root, text="Year:", font=("Arial", 12))
        self.label_make = tk.Label(root, text="Make:", font=("Arial", 12))
        self.label_model = tk.Label(root, text="Model:", font=("Arial", 12))
        self.label_price = tk.Label(root, text="Price:", font=("Arial", 12))
        self.label_description = tk.Label(root, text="Description:", font=("Arial", 12))

        self.entry_year = tk.Entry(root, width=20, font=("Arial", 12))
        self.entry_make = tk.Entry(root, width=20, font=("Arial", 12))
        self.entry_model = tk.Entry(root, width=20, font=("Arial", 12))
        self.entry_price = tk.Entry(root, width=20, font=("Arial", 12))
        self.entry_description = tk.Entry(root, width=20, font=("Arial", 12))

        self.button_add_car = tk.Button(root, text="Add Car", command=self.add_car_to_inventory, font=("Arial", 12))
        self.button_view_inventory = tk.Button(root, text="View Inventory", command=self.show_inventory, font=("Arial",
                                                                                                               12))
        self.button_remove_car = tk.Button(root, text="Remove Car", command=self.remove_selected_car, font=("Arial",
                                                                                                            12))
        self.button_show_description = tk.Button(root, text="Show Description", command=self.show_description,
                                                 font=("Arial", 12))
        self.label_search = tk.Label(root, text="Search:", font=("Arial", 12))
        self.entry_search = tk.Entry(root, width=20, font=("Arial", 12))
        self.button_search = tk.Button(root, text="Search", command=self.search_inventory, font=("Arial", 12))
        self.button_edit_car = tk.Button(root, text="Edit Car", command=self.edit_selected_car, font=("Arial", 12))

        self.sorting_option = tk.StringVar(root)
        self.sorting_option.set("Year (High to Low)")

        # Sorting options for the drop-down
        sorting_options = ["Year (Low to High)", "Year (High to Low)", "Price (Low to High)", "Price (High to Low)",
                           "Make", "Model"]
        self.sort_dropdown = ttk.Combobox(root, textvariable=self.sorting_option, values=sorting_options, font=("Arial",
                                                                                                                12))
        # Placing GUI elements onto a grid
        self.listbox.grid(row=0, column=0, rowspan=5, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.label_year.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.label_make.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.label_model.grid(row=2, column=2, padx=10, pady=10, sticky="w")
        self.label_price.grid(row=3, column=2, padx=10, pady=10, sticky="w")
        self.label_description.grid(row=4, column=2, padx=10, pady=10, sticky="w")

        self.entry_year.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        self.entry_make.grid(row=1, column=3, padx=10, pady=10, sticky="ew")
        self.entry_model.grid(row=2, column=3, padx=10, pady=10, sticky="ew")
        self.entry_price.grid(row=3, column=3, padx=10, pady=10, sticky="ew")
        self.entry_description.grid(row=4, column=3, padx=10, pady=10, sticky="ew")

        self.button_add_car.grid(row=5, column=3, padx=10, pady=10, sticky="ew")

        self.button_view_inventory.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")
        self.button_remove_car.grid(row=6, column=3, padx=10, pady=10, sticky="ew")
        self.button_edit_car.grid(row=6, column=2, padx=10, pady=10, sticky="ew")
        self.sort_dropdown.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")
        self.button_show_description.grid(row=7, column=3, padx=10, pady=10, sticky="ew")
        self.label_search.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.entry_search.grid(row=7, column=1, padx=10, pady=10, sticky="ew")
        self.button_search.grid(row=7, column=2, padx=10, pady=10, sticky="ew")

        # Configure grid weight(resizing)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_rowconfigure(6, weight=1)

        # Add some style to GUI
        self.style = ttk.Style()
        self.style.configure("TButton", padding=5, relief="flat", font=("Arial", 12))
        self.style.configure("TCombobox", padding=5, font=("Arial", 12))

        self.listbox.configure(fg="white", bg="#808080")

        # Default for drop down
        self.sort_dropdown.set("Year (High to Low)")

        self.show_inventory()

    def show_inventory(self):
        # Clear listbox
        self.listbox.delete(0, tk.END)
        # Get sorted inventory
        sorted_inventory = self.get_sorted_inventory()
        # Insert car details into listbox
        for car in sorted_inventory:
            self.listbox.insert(tk.END, f"{car.year} {car.make} {car.model} - ${car.price}")

    def get_sorted_inventory(self):
        sorting_option = self.sorting_option.get()

        # Sorting key based on the option selected from drop-down
        if sorting_option == "Year (Low to High)":
            sorting_key = lambda car: (-car.year, car.price)
        elif sorting_option == "Year (High to Low)":
            sorting_key = lambda car: (car.year, car.price)  # Keep year ascending
        elif sorting_option == "Price (Low to High)":
            sorting_key = lambda car: (-car.price, car.year, car.make, car.model)
        elif sorting_option == "Price (High to Low)":
            sorting_key = lambda car: (car.price, car.year, car.make, car.model)  # Keep price ascending
        elif sorting_option == "Make":
            sorting_key = lambda car: (car.make, car.model, car.price, car.year)
        elif sorting_option == "Model":
            sorting_key = lambda car: (car.model, car.make, car.price, car.year)
        else:
            sorting_key = lambda car: (car.year, car.make, car.model, -car.price)

        sorted_inventory = sorted(self.inventory.get_inventory(), key=sorting_key, reverse=True)
        return sorted_inventory

    def add_car_to_inventory(self):
        try:
            # Get the values from the entry fields
            year = int(self.entry_year.get())
            make = self.entry_make.get()
            model = self.entry_model.get()
            price = int(self.entry_price.get())
            description = self.entry_description.get()

            # Validation for input values
            if not (1900 <= year <= 2100) or price < 0 or make == '' or model == '':
                messagebox.showerror("Error", "Invalid input. Please enter valid values.")
                return

            # Create new car object, then add to inventory
            new_car = Car(year, make, model, price, description)
            self.inventory.add_car(new_car)
            self.show_inventory()

            # Clear all fields
            self.entry_year.delete(0, tk.END)
            self.entry_make.delete(0, tk.END)
            self.entry_model.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            self.entry_description.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid values.")

    def remove_selected_car(self):
        # Get selected index from listbox
        selected_index = self.listbox.curselection()

        if selected_index:
            # Remove selected car
            removed_car = self.inventory.remove_car(selected_index[0])

            if removed_car:
                # Update list box and display message
                self.show_inventory()
                messagebox.showinfo("Car Removed", f"The car has been removed:\n{repr(removed_car)}")
        else:
            # Waring message if no car has been selected
            messagebox.showwarning("No Car Selected", "Please select a car to remove.")

    def show_description(self):
        # Get selected index from listbox
        selected_index = self.listbox.curselection()

        if selected_index:
            # Get the selected car
            selected_car = self.get_sorted_inventory()[selected_index[0]]

            # Create new window to display description
            description_window = tk.Toplevel(self.root)
            description_window.title("Car Description")

            # Labels
            tk.Label(description_window, text=f"Year: {selected_car.year}", font=("Arial", 12)).pack()
            tk.Label(description_window, text=f"Make: {selected_car.make}", font=("Arial", 12)).pack()
            tk.Label(description_window, text=f"Model: {selected_car.model}", font=("Arial", 12)).pack()
            tk.Label(description_window, text=f"Price: {selected_car.price}", font=("Arial", 12)).pack()

            tk.Label(description_window, text="Description:", font=("Arial", 12)).pack()
            description_text = tk.Text(description_window, wrap=tk.WORD, width=40, height=10, font=("Arial", 12))
            description_text.insert(tk.END, selected_car.description)
            # Read-only
            description_text.config(state=tk.DISABLED)
            description_text.pack()

            # Button to close the window
            tk.Button(description_window, text="Close", command=description_window.destroy,
                      font=("Arial", 12)).pack()

        else:
            # Warning message if no car is selected
            messagebox.showwarning("No Car Selected", "Please select a car to view its description.")

    def search_inventory(self):
        # Get search term from entry field
        search_term = self.entry_search.get().lower()
        matching_cars = []

        # Find cars that match search
        current = self.inventory.inventory.head
        while current is not None:
            if (
                    search_term in current.car.make.lower()
                    or search_term in current.car.model.lower()
                    or search_term in str(current.car.year)
            ):
                matching_cars.append(current.car)
            current = current.next_node

        # Clear listbox and display matching cars
        self.listbox.delete(0, tk.END)
        for car in matching_cars:
            self.listbox.insert(tk.END, repr(car))

    def edit_selected_car(self):
        # Get selected index from list box
        selected_index = self.listbox.curselection()

        if selected_index:
            # Get the selected car from inventory
            selected_car = self.get_sorted_inventory()[selected_index[0]]

            # New window for editing car
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Car Details")

            # Labels
            labels = ["Year:", "Make:", "Model:", "Price:", "Description:"]
            entries = [tk.Entry(edit_window, font=("Arial", 12)) for _ in range(5)]

            for label, entry, value in zip(labels, entries, [selected_car.year, selected_car.make, selected_car.model,
                                                             selected_car.price, selected_car.description]):
                tk.Label(edit_window, text=label, font=("Arial", 12)).pack()
                entry.insert(tk.END, value)
                entry.pack()

            def update_car_details():
                try:
                    edited_car = Car(int(entries[0].get()), entries[1].get(), entries[2].get(),
                                     int(entries[3].get()), entries[4].get())

                    # Update car and save data
                    self.inventory.inventory.update_car(selected_index[0], edited_car)
                    self.inventory.save_data()
                    self.show_inventory()

                    # Close window when save changes made
                    edit_window.destroy()

                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please enter valid values.")

            # Save changes button
            tk.Button(edit_window, text="Save Changes", command=update_car_details, font=("Arial", 12)).pack()

        else:
            messagebox.showwarning("No Car Selected", "Please select a car to edit.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CarInventoryApp(root)
    root.mainloop()
