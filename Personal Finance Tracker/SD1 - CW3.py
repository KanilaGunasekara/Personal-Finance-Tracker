import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class FinanceTrackerGUI:
    def add_transaction_gui(self):
        category = input("Enter the category: ")
        amount = float(input("Enter the amount: "))
        date = input("Enter the date (YYYY-MM-DD): ")
        transaction_type = input("Enter the transaction type (income/expense): ")  

        if category not in self.transactions:
            self.transactions[category] = []
        self.transactions[category].append({"amount": amount, "date": date, "type": transaction_type or "expense"})
        self.save_transactions()
        print("Transaction added successfully.")

    def update_transaction_gui(self):
        category = input("Enter the category: ")
        index = int(input("Enter the index of the transaction to update: ")) - 1
        if category in self.transactions and 0 <= index < len(self.transactions[category]):
            amount = float(input("Enter the new amount: "))
            date = input("Enter the new date (YYYY-MM-DD): ")
            self.transactions[category][index] = {"amount": amount, "date": date}
            self.save_transactions()
            print("Transaction updated successfully.")
        else:
            print("Invalid category or transaction index.")

    def delete_transaction_gui(self):
         category = input("Enter the category: ")
         index = int(input("Enter the index of the transaction to delete: ")) - 1
         if category in self.transactions and 0 <= index < len(self.transactions[category]):
             del self.transactions[category][index]
             self.save_transactions()
             print("Transaction deleted successfully.")
         else:
             print("Invalid category or transaction index.")

    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.sort_states = {"Date": None, "Amount": None, "Type": None}
        self.transactions = self.load_transactions("transactions.json")  # Load transactions
        self.filtered_transactions = {}  # Define filtered_transactions attribute
        self.create_widgets()  # Create widgets after loading transactions

    def create_widgets(self):
        # Frame for table and scrollbar
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack(fill="both", expand=True)

        # Treeview for displaying transactions
        self.tree = ttk.Treeview(self.table_frame, columns=("Date", "Amount", "Type"))
        self.tree.heading("#0", text="Transaction")
        self.tree.heading("Date", text="Date", command=lambda: self.sort_by_column("Date"))
        self.tree.heading("Amount", text="Amount", command=lambda: self.sort_by_column("Amount"))
        self.tree.heading("Type", text="Type", command=lambda: self.sort_by_column("Type"))
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Search bar for category
        category_frame = ttk.Frame(self.root)
        category_frame.pack(fill=tk.X)
        self.category_var = tk.StringVar()
        category_entry = ttk.Entry(category_frame, textvariable=self.category_var)
        category_entry.pack(side=tk.LEFT, padx=5, pady=5)
        category_button = ttk.Button(category_frame, text="Search by Category", command=self.search_by_category)
        category_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Search bar for date
        date_frame = ttk.Frame(self.root)
        date_frame.pack(fill=tk.X)
        self.date_var = tk.StringVar()
        date_entry = ttk.Entry(date_frame, textvariable=self.date_var)
        date_entry.pack(side=tk.LEFT, padx=5, pady=5)
        date_button = ttk.Button(date_frame, text="Search by Date", command=self.search_by_date)
        date_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Search bar for amount
        amount_frame = ttk.Frame(self.root)
        amount_frame.pack(fill=tk.X)
        self.amount_var = tk.StringVar()
        amount_entry = ttk.Entry(amount_frame, textvariable=self.amount_var)
        amount_entry.pack(side=tk.LEFT, padx=5, pady=5)
        amount_button = ttk.Button(amount_frame, text="Search by Amount", command=self.search_by_amount)
        amount_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Search bar for type
        type_frame = ttk.Frame(self.root)
        type_frame.pack(fill=tk.X)
        self.type_var = tk.StringVar()
        type_entry = ttk.Entry(type_frame, textvariable=self.type_var)
        type_entry.pack(side=tk.LEFT, padx=5, pady=5)
        type_button = ttk.Button(type_frame, text="Search by Type", command=self.search_by_type)
        type_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Display transactions initially
        self.display_transactions()

    def load_transactions(self, filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("File not found")
            return {}

    def display_transactions(self):
        # Remove existing entries
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Determine whether to display all transactions or filtered transactions
        transactions_to_display = self.filtered_transactions if self.filtered_transactions else self.transactions

        # Add transactions to the treeview
        for category, transactions in transactions_to_display.items():
            for transaction in transactions:
                self.tree.insert("", "end", text=category, values=(transaction["date"], transaction["amount"], transaction["type"]))

    def search_by_category(self):
        # Search transactions by category
        query = self.category_var.get()
        self.filtered_transactions = {category: data for category, data in self.transactions.items() if query.lower() in category.lower()}
        self.display_transactions()

    def search_by_date(self):
        # Search transactions by date
        query = self.date_var.get()
        try:
            date_obj = datetime.strptime(query, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        self.filtered_transactions = {}
        for category, data in self.transactions.items():
            filtered_data = [t for t in data if datetime.strptime(t["date"], "%Y-%m-%d") == date_obj]
            if filtered_data:
                self.filtered_transactions[category] = filtered_data
        self.display_transactions()

    def search_by_amount(self):
        # Search transactions by amount
        query = self.amount_var.get()
        try:
            amount = float(query)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")
            return

        tolerance = 0.01
        self.filtered_transactions = {}
        for category, data in self.transactions.items():
            filtered_data = [t for t in data if abs(float(t.get("amount", 0)) - amount) < tolerance]
            if filtered_data:
                self.filtered_transactions[category] = filtered_data
        self.display_transactions()

    def search_by_type(self):
        # Search transactions by type (income/expense)
        query = self.type_var.get().lower()
        if query not in ["income", "expense"]:
            messagebox.showerror("Error", "Invalid transaction type. Please enter 'income' or 'expense'.")
            return

        self.filtered_transactions = {}
        for category, data in self.transactions.items():
            filtered_data = [t for t in data if t.get("type", "").lower() == query]
            if filtered_data:
                self.filtered_transactions[category] = filtered_data
        self.display_transactions()

    def sort_by_column(self, col):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort()
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        self.tree.heading(col, command=lambda: self.sort_by_column_reverse(col))

    def sort_by_column_reverse(self, col):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=True)
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        self.tree.heading(col, command=lambda: self.sort_by_column(col))

    def save_transactions(self):
        with open("transactions.json", "w") as file:
            json.dump(self.transactions, file)

    def gui(self):
        self.display_transactions()

def main():
    root = tk.Tk()
    finance_tracker = FinanceTrackerGUI(root)
    
    while True:
        print(" 1: Add Transactions\n 2: Update Transactions\n 3: Delete Transactions\n 4: GUI\n 5: Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            finance_tracker.add_transaction_gui()
        elif choice == 2:
            finance_tracker.update_transaction_gui()
        elif choice == 3:
            finance_tracker.delete_transaction_gui()
        elif choice == 4:
            finance_tracker.gui()
            root.mainloop()  # Start the Tkinter event loop only when GUI is chosen
        elif choice == 5:
            print("Exiting..")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()

