import tkinter as tk
from tkinter import ttk

class Account:
    def __init__(self, name, percent, amount):
        self.name = name
        self.percent = percent
        self.amount = amount

def print_details():
    for i, account in enumerate(account_list):
        name_label = ttk.Label(details_frame, text=account.name)
        name_label.grid(row=i+1, column=0, padx=5, pady=5)

        percent_label = ttk.Label(details_frame, text=f"{account.percent}%")
        percent_label.grid(row=i+1, column=1, padx=5, pady=5)

        amount_label = ttk.Label(details_frame, text=f"${account.amount:.2f}")
        amount_label.grid(row=i+1, column=2, padx=5, pady=5)

        # Set color based on account balance
        if account.amount == 0:
            amount_label.configure(foreground="red")
        elif account.amount < 10:
            amount_label.configure(foreground="#DE9900")
        else:
            amount_label.configure(foreground="green")  # Light green

def deposit():
    try:
        deposit_amount = float(deposit_entry.get())
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter a valid number for deposit amount.")
        return
    
    for account in account_list:
        new_amount = account.amount + (deposit_amount * (account.percent / 100.0))
        account.amount = new_amount

    print_details()
    deposit_entry.delete(0, tk.END)

def withdraw():
    try:
        account_choice = int(account_combobox.get().split(':')[0]) - 1
        withdraw_amount = float(withdraw_entry.get())
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter valid numbers for account choice and withdraw amount.")
        return
    
    account_list[account_choice].amount -= withdraw_amount

    print_details()
    withdraw_entry.delete(0, tk.END)

def edit():
    try:
        account_choice = int(edit_combobox.get().split(':')[0]) - 1
        edit_choice = edit_var.get()
        if edit_choice == 1:
            new_name = edit_entry.get()
            account_list[account_choice].name = new_name
        else:
            new_percent = int(edit_entry.get())
            account_list[account_choice].percent = new_percent
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter a valid number for account choice and percent.")
        return
    
    print_details()
    edit_entry.delete(0, tk.END)

def add():
    name = name_entry.get()
    percent = percent_entry.get()
    
    if not name or not percent:
        tk.messagebox.showerror("Error", "Please enter both name and percent.")
        return
    
    try:
        percent = int(percent)
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter a valid number for percent.")
        return
    
    account = Account(name, percent, 0.0)
    account_list.append(account)

    print_details()
    name_entry.delete(0, tk.END)
    percent_entry.delete(0, tk.END)

def save_and_exit():
    with open("savings.txt", "w") as file:
        for i, account in enumerate(account_list):
            if i == len(account_list) - 1:
                file.write(f"{account.name},{account.percent},{account.amount},")
            else:
                file.write(f"{account.name},{account.percent},{account.amount},\n")

    root.destroy()

root = tk.Tk()
root.title("Savings Account Management")

# Create account list
account_list = []
with open("savings.txt") as file:
    for line in file:
        name, percent, amount, temp = line.strip().split(",")
        account_list.append(Account(name, int(percent), float(amount)))

# Deposit frame
deposit_frame = ttk.Frame(root)
deposit_frame.pack(padx=10, pady=10, fill="x")

deposit_label = ttk.Label(deposit_frame, text="Deposit Amount:")
deposit_label.grid(row=0, column=0, padx=5, pady=5)

deposit_entry = ttk.Entry(deposit_frame)
deposit_entry.grid(row=0, column=1, padx=5, pady=5)

deposit_button = ttk.Button(deposit_frame, text="Deposit", command=deposit)
deposit_button.grid(row=0, column=2, padx=5, pady=5)

# Withdraw frame
withdraw_frame = ttk.Frame(root)
withdraw_frame.pack(padx=10, pady=10, fill="x")

withdraw_label = ttk.Label(withdraw_frame, text="Withdraw Amount:")
withdraw_label.grid(row=0, column=0, padx=5, pady=5)

withdraw_entry = ttk.Entry(withdraw_frame)
withdraw_entry.grid(row=0, column=1, padx=5, pady=5)

account_combobox = ttk.Combobox(withdraw_frame, values=[f"{i+1}: {account.name}" for i, account in enumerate(account_list)])
account_combobox.grid(row=0, column=2, padx=5, pady=5)

withdraw_button = ttk.Button(withdraw_frame, text="Withdraw", command=withdraw)
withdraw_button.grid(row=0, column=3, padx=5, pady=5)

# Edit frame
edit_frame = ttk.Frame(root)
edit_frame.pack(padx=10, pady=10, fill="x")

edit_var = tk.IntVar()
edit_var.set(1)

edit_combobox = ttk.Combobox(edit_frame, values=[f"{i+1}: {account.name}" for i, account in enumerate(account_list)])
edit_combobox.grid(row=0, column=0, padx=5, pady=5)

edit_radio1 = ttk.Radiobutton(edit_frame, text="Name", variable=edit_var, value=1)
edit_radio1.grid(row=0, column=1, padx=5, pady=5)

edit_radio2 = ttk.Radiobutton(edit_frame, text="Percent", variable=edit_var, value=2)
edit_radio2.grid(row=0, column=2, padx=5, pady=5)

edit_entry = ttk.Entry(edit_frame)
edit_entry.grid(row=0, column=3, padx=5, pady=5)

edit_button = ttk.Button(edit_frame, text="Edit", command=edit)
edit_button.grid(row=0, column=4, padx=5, pady=5)

# Add frame
add_frame = ttk.Frame(root)
add_frame.pack(padx=10, pady=10, fill="x")

name_label = ttk.Label(add_frame, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5)

name_entry = ttk.Entry(add_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

percent_label = ttk.Label(add_frame, text="Percent:")
percent_label.grid(row=0, column=2, padx=5, pady=5)

percent_entry = ttk.Entry(add_frame)
percent_entry.grid(row=0, column=3, padx=5, pady=5)

add_button = ttk.Button(add_frame, text="Add", command=add)
add_button.grid(row=0, column=4, padx=5, pady=5)

# Details frame
details_frame = ttk.Frame(root)
details_frame.pack(padx=10, pady=10)

name_header = ttk.Label(details_frame, text="Name")
name_header.grid(row=0, column=0, padx=5, pady=5)

percent_header = ttk.Label(details_frame, text="Percent")
percent_header.grid(row=0, column=1, padx=5, pady=5)

amount_header = ttk.Label(details_frame, text="Amount")
amount_header.grid(row=0, column=2, padx=5, pady=5)

# Print initial account details
print_details()

# Save and Exit button
save_exit_button = ttk.Button(root, text="Save and Exit", command=save_and_exit)
save_exit_button.pack(padx=10, pady=10)

root.mainloop()
