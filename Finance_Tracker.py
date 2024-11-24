import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg

class FinanceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker")
        self.root.geometry("800x600")

        # Variables
        self.entries = []
        self.current_month = datetime.now().month
        self.dark_mode = tk.BooleanVar(value=True)

        # Dark Mode
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", padding=(10, 5), font='Helvetica 10', foreground="white",
                             background="#333" if self.dark_mode.get() else "#DDD")
        self.style.configure("TLabel", font='Helvetica 10', foreground="white" if self.dark_mode.get() else "black",
                             background="#333" if self.dark_mode.get() else "#DDD")
        self.style.configure("TEntry", padding=(5, 5), font='Helvetica 10', foreground="black", background="white")

        # Widgets
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.income_expense_label = ttk.Label(self.frame, text="Income/Expense:")
        self.income_expense_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.description_label = ttk.Label(self.frame, text="Description:")
        self.description_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.amount_label = ttk.Label(self.frame, text="Amount:")
        self.amount_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.category_label = ttk.Label(self.frame, text="Category:")
        self.category_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

        self.income_expense_var = tk.StringVar(value="Income")
        self.income_expense_entry = ttk.Combobox(self.frame, textvariable=self.income_expense_var,
                                                 values=["Income", "Expense"])
        self.income_expense_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.description_var = tk.StringVar()
        self.description_entry = ttk.Entry(self.frame, textvariable=self.description_var)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.amount_var = tk.DoubleVar()
        self.amount_entry = ttk.Entry(self.frame, textvariable=self.amount_var)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        self.category_var = tk.StringVar()
        self.category_entry = ttk.Entry(self.frame, textvariable=self.category_var)
        self.category_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        self.add_button = ttk.Button(self.frame, text="Add Entry", command=self.add_entry)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.entries_tree = ttk.Treeview(self.frame, columns=("Description", "Amount", "Category"), show="headings")
        self.entries_tree.heading("Description", text="Description")
        self.entries_tree.heading("Amount", text="Amount")
        self.entries_tree.heading("Category", text="Category")
        self.entries_tree.grid(row=5, column=0, columnspan=2, pady=10)

        self.delete_button = ttk.Button(self.frame, text="Delete Entry", command=self.delete_entry)
        self.delete_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.update_button = ttk.Button(self.frame, text="Update Entry", command=self.update_entry)
        self.update_button.grid(row=6, column=1, pady=10)

        self.show_entries_button = ttk.Button(self.frame, text="Show Entries", command=self.show_entries)
        self.show_entries_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.monthly_summary_button = ttk.Button(self.frame, text="Monthly Summary", command=self.show_monthly_summary)
        self.monthly_summary_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.save_button = ttk.Button(self.frame, text="Save Data", command=self.save_data)
        self.save_button.grid(row=9, column=0, columnspan=2, pady=10)

        self.load_button = ttk.Button(self.frame, text="Load Data", command=self.load_data)
        self.load_button.grid(row=9, column=1, pady=10)

        self.toggle_dark_mode_button = ttk.Button(self.frame, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.toggle_dark_mode_button.grid(row=10, column=0, columnspan=2, pady=10)

    def add_entry(self):
        try:
            entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "description": self.description_var.get(),
                "amount": float(self.amount_var.get()),
                "is_income": self.income_expense_var.get() == "Income",
                "category": self.category_var.get()
            }
            self.entries.append(entry)
            self.clear_entry_fields()
            self.show_entries()
        except ValueError:
            messagebox.showerror("Invalid Entry", "Please enter a valid amount.")

    def show_entries(self):
        self.clear_treeview()
        for entry in self.entries:
            self.entries_tree.insert("", "end",
                                     values=(entry["description"], entry["amount"], entry.get("category", "")))

    def clear_treeview(self):
        for item in self.entries_tree.get_children():
            self.entries_tree.delete(item)

    def delete_entry(self):
        selected_item = self.entries_tree.selection()
        if selected_item:
            index = self.entries_tree.index(selected_item)
            del self.entries[index]
            self.show_entries()
        else:
            messagebox.showinfo("No Selection", "Please select an entry to delete.")

    def update_entry(self):
        selected_item = self.entries_tree.selection()
        if selected_item:
            index = self.entries_tree.index(selected_item)
            entry = self.entries[index]

            # Update entry fields
            self.income_expense_var.set("Income" if entry["is_income"] else "Expense")
            self.description_var.set(entry["description"])
            self.amount_var.set(entry["amount"])
            self.category_var.set(entry.get("category", ""))

            # Delete the selected entry
            del self.entries[index]

            # Show remaining entries
            self.show_entries()

        else:
            messagebox.showinfo("No Selection", "Please select an entry to update.")

    def show_monthly_summary(self):
        # Filter entries for the current month
        month_entries = [entry for entry in self.entries if
                         datetime.strptime(entry["date"], "%Y-%m-%d %H:%M:%S").month == self.current_month]

        # Separate income and expenses
        income = sum(entry["amount"] for entry in month_entries if entry["is_income"])
        expenses = sum(entry["amount"] for entry in month_entries if not entry["is_income"])

        # Plotting
        labels = ['Income', 'Expenses']
        values = [income, expenses]

        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#66b3ff', '#99ff99'])
        plt.title(f'Monthly Summary - {datetime.now().strftime("%B %Y")}')
        plt.show()

    def save_data(self):
        with open("finance_data.json", 'w') as file:
            json.dump(self.entries, file)
        messagebox.showinfo("Data Saved", "Financial data saved successfully.")

    def load_data(self):
        try:
            with open("finance_data.json", 'r') as file:
                self.entries = json.load(file)
            self.show_entries()
            messagebox.showinfo("Data Loaded", "Financial data loaded successfully.")
        except FileNotFoundError:
            messagebox.showinfo("No Data Found", "No saved data found.")

    def toggle_dark_mode(self):
        self.dark_mode.set(not self.dark_mode.get())
        self.style.configure("TButton", background="#333" if self.dark_mode.get() else "#DDD")
        self.style.configure("TLabel", background="#333" if self.dark_mode.get() else "#DDD",
                             foreground="white" if self.dark_mode.get() else "black")
        self.style.configure("TEntry", background="white" if self.dark_mode.get() else "#DDD")

        # Update existing treeview
        for child in self.entries_tree.get_children():
            self.entries_tree.item(child, tags=("dark" if self.dark_mode.get() else "light",))

        # Refresh treeview
        self.show_entries()

    def clear_entry_fields(self):
        self.income_expense_var.set("Income")
        self.description_var.set("")
        self.amount_var.set("")
        self.category_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTrackerApp(root)
    root.mainloop()

# Function to record a new income or expense entry
def record_entry(entries, entry_type, amount):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = {'timestamp': timestamp, 'type': entry_type, 'amount': amount}
    entries.append(entry)
    print(f"Entry recorded: {entry_type.capitalize()} of ${amount} on {timestamp}")

# Function to view all recorded entries
def view_all_entries(entries):
    if not entries:
        print("No entries recorded yet.")
    else:
        for entry in entries:
            print(f"{entry['timestamp']} - {entry['type'].capitalize()}: ${entry['amount']}")

# Function to calculate total income and total expenses
def calculate_totals(entries):
    total_income = sum(entry['amount'] for entry in entries if entry['type'] == 'income')
    total_expenses = sum(entry['amount'] for entry in entries if entry['type'] == 'expense')
    return total_income, total_expenses

# Function to view a summary of transactions for a specific month
def view_summary_for_month(entries, month):
    month_entries = [entry for entry in entries if entry['timestamp'].startswith(month)]
    if not month_entries:
        print(f"No entries recorded for {month}.")
    else:
        print(f"Summary for {month}:")
        for entry in month_entries:
            print(f"{entry['timestamp']} - {entry['type'].capitalize()}: ${entry['amount']}")

# Function to save financial data to a text file
def save_data(entries):
    with open('finance_data.txt', 'w') as file:
        json.dump(entries, file)

# Function to load financial data from a text file
def load_data():
    if os.path.exists('finance_data.txt'):
        with open('finance_data.txt', 'r') as file:
            return json.load(file)
    else:
        return []

# Main function
def main():
    entries = load_data()

    while True:
        print("\nFinance Tracker Menu:")
        print("1. Record new income")
        print("2. Record new expense")
        print("3. View all entries")
        print("4. Calculate totals")
        print("5. View summary for a specific month")
        print("6. Save and exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            description = input("Enter description: ")
            amount = float(input("Enter the income amount: "))
            record_entry(entries, 'income', amount)
        elif choice == '2':
            description = input("Enter description: ")
            amount = float(input("Enter the expense amount: "))
            record_entry(entries, 'expense', amount)
        elif choice == '3':
            view_all_entries(entries)
        elif choice == '4':
            total_income, total_expenses = calculate_totals(entries)
            print(f"Total Income: ${total_income}")
            print(f"Total Expenses: ${total_expenses}")
        elif choice == '5':
            month = input("Enter the month (YYYY-MM) for the summary: ")
            view_summary_for_month(entries, month)
        elif choice == '6':
            save_data(entries)
            print("Financial data saved. Exiting program.Good Bye !!!👋😊✔")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
