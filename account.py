import copy
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Account:
    def __init__(self, name, percent, amount):
        self.name = name
        self.percent = percent
        self.amount = amount

actionsForUndo = []
def undo():
    global actionsForUndo
    global account_list

    if not actionsForUndo:
        tk.messagebox.showerror("Error", "No actions left to undo!")
        return
    else:
        # Retrieve the last deleted account
        actionToUndo = actionsForUndo.pop()

        # Add the account back to the original list
        account_list = actionToUndo

        sort_details()

        # Update the details display
        print_details()

def sort_details():
    global account_list
    global delete_combobox
    global account_combobox
    global edit_combobox

    sorted_accounts = sorted(account_list, key=lambda account: account.percent, reverse=True)

    account_list = sorted_accounts

    delete_combobox.grid_forget()
    account_combobox.grid_forget()
    edit_combobox.grid_forget()

    delete_combobox = ttk.Combobox(delete_frame, state="readonly", values=[f"{i+1}: {account.name}" for i, account in enumerate(account_list)])
    delete_combobox.grid(row=0, column=1, padx=5, pady=5)

    account_combobox = ttk.Combobox(withdraw_frame, state="readonly", values=[f"{i+1}: {account.name}" for i, account in enumerate(account_list)])
    account_combobox.grid(row=1, column=1, padx=15, pady=5)

    edit_combobox = ttk.Combobox(edit_frame, state="readonly", values=[f"{i+1}: {account.name}" for i, account in enumerate(account_list)])
    edit_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w") 

    return

def print_details():
    global account_list
    for widget in details_frame.grid_slaves():
        widget.grid_forget()

    sort_details()

    for i, account in enumerate(account_list):
        name_label = ttk.Label(details_frame, text=account.name + "    ", foreground="#333333", font=("Helvetica", 12))
        name_label.grid(row=i+1, column=0, padx=5, pady=5)

        percent_label = ttk.Label(details_frame, text=f"{account.percent}%" + "    ", foreground="#333333", font=("Helvetica", 12))
        percent_label.grid(row=i+1, column=1, padx=5, pady=5)

        amount_label = ttk.Label(details_frame, text=f"${account.amount:.2f}", font=("Helvetica", 12))
        amount_label.grid(row=i+1, column=2, padx=5, pady=5)

        

        # Set color based on account balance
        if account.amount <= 0:
            amount_label.configure(foreground="red")
        elif account.amount < 10:
            amount_label.configure(foreground="#DE9900") # dark yellow
        else:
            amount_label.configure(foreground="green")

def deposit():  
    global actionsForUndo
    try:
        deposit_amount = float(deposit_entry.get().replace(",", "", -1))
        
        if deposit_amount <= 0:
            tk.messagebox.showerror("Error", "Please enter a positive number for deposit amount.")
            return
            
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter a valid number for deposit amount.")
        return

    actionsForUndo.append(copy.deepcopy(account_list))

    for account in account_list:
        new_amount = account.amount + (deposit_amount * (account.percent / 100.0))
        account.amount = new_amount

    print_details()
    deposit_entry.delete(0, tk.END)

def withdraw():
    global actionsForUndo
    try:
        account_choice = int(account_combobox.get().split(':')[0]) - 1
        withdraw_amount = float(withdraw_entry.get().replace(",", "", -1))
        if withdraw_amount <= 0:
            tk.messagebox.showerror("Error", "Please enter a positive number for withdraw amount.")
            return
        elif withdraw_amount > account_list[account_choice].amount:
            tk.messagebox.showerror("Error", "Please enter a number smaller than or equal to the account amount.")
            return
        else:
            actionsForUndo.append(copy.deepcopy(account_list))

            account_list[account_choice].amount -= withdraw_amount
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter valid numbers for withdraw amount and account choice.")
        return
    except IndexError:
        tk.messagebox.showerror("Error", "Please enter a valid number for the account choice.")
        return

    print_details()
    withdraw_entry.delete(0, tk.END)

def edit():
    global actionsForUndo
    try:
        account_choice = int(edit_combobox.get().split(':')[0]) - 1
        edit_choice = edit_var.get()
        if edit_choice == 1:
            new_name = edit_entry.get()

            if new_name.strip(" ") == "":
                tk.messagebox.showerror("Error", "Please enter a valid name for the account choice.")
                return
            else:
                actionsForUndo.append(copy.deepcopy(account_list))

                account_list[account_choice].name = new_name
        else:
            new_percent = int(edit_entry.get())

            total_percent = 0

            for account in account_list:

                total_percent += account.percent

            if total_percent - account_list[account_choice].percent + new_percent > 100:
                
                tk.messagebox.showerror("Error", "Please enter a smaller number for the percent. (Total sum of percentages should be at or lower than 100%) You may need to edit a current account percent.")
                return
            elif new_percent < 0:
                
                tk.messagebox.showerror("Error", "Please enter a number greater than or equal to 0 for the percent.")
                return          
            else:
                actionsForUndo.append(copy.deepcopy(account_list))

                account_list[account_choice].percent = new_percent

            sort_details()
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter a valid number for account choice and percent.")
        return
    
    print_details()
    edit_entry.delete(0, tk.END)

def add():
    global actionsForUndo

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
    
    total_percent = 0

    for account in account_list:

        total_percent += account.percent

    if total_percent + percent > 100:
        
        tk.messagebox.showerror("Error", "Please enter a smaller number for the percent. (Total sum of percentages should be at or lower than 100%) You may need to edit a current account percent.")
        return 
    
    elif percent < 0:
        
        tk.messagebox.showerror("Error", "Please enter a number greater than or equal to 0 for the percent.")
        return 
    
    elif name.strip(" ") == "":
        tk.messagebox.showerror("Error", "Please enter a valid name for the account choice.")
        return
    
    else:
        actionsForUndo.append(copy.deepcopy(account_list))

        account = Account(name, percent, 0.0)
        account_list.append(account)

    sort_details()

    print_details()
    name_entry.delete(0, tk.END)
    percent_entry.delete(0, tk.END)

def delete():
    global actionsForUndo


    try:
        account_choice = int(delete_combobox.get().split(':')[0]) - 1

        if account_choice < 0 or account_choice >= len(account_list):
            raise IndexError
        
        
        actionsForUndo.append(copy.deepcopy(account_list))

        # Remove the selected account from the account list
        del account_list[account_choice]

        # Update the details display
        print_details()

        sort_details()


    except ValueError:
        tk.messagebox.showerror("Error", "Please choose a valid number for account choice")
    except IndexError:
        tk.messagebox.showerror("Error", "Please choose a valid account to delete.")

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
deposit_frame.pack(padx=10, pady=15, fill="x")

deposit_label = ttk.Label(deposit_frame, text="Deposit an amount to split between accounts:", foreground="#333333", font=("Helvetica", 12))
deposit_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

dollar_label = ttk.Label(deposit_frame, text="$", foreground="#333333", font=("Helvetica", 11))
dollar_label.grid(row=0, column=1, padx=(5, 0), pady=5, sticky="w")

deposit_entry = ttk.Entry(deposit_frame)
deposit_entry.grid(row=0, column=1, padx=(15, 5), pady=5, sticky="e")

deposit_button = ttk.Button(deposit_frame, text="Deposit", command=deposit)
deposit_button.grid(row=0, column=2, padx=5, pady=5)

# Withdraw frame
withdraw_frame = ttk.Frame(root)
withdraw_frame.pack(padx=10, pady=15, fill="x")

withdraw_label = ttk.Label(withdraw_frame, text="Withdraw an amount from a specific account:", foreground="#333333", font=("Helvetica", 12))
withdraw_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

withdraw_entry = ttk.Entry(withdraw_frame)
withdraw_entry.grid(row=0, column=1, padx=5, pady=5)

select_account_label = ttk.Label(withdraw_frame, text="Select an account:", foreground="#333333", font=("Helvetica", 11))
select_account_label.grid(row=1, column=0, padx=5, pady=5, sticky="e") 

account_combobox = ttk.Combobox(withdraw_frame, state="readonly", values=[f"{i+1}: {account.name}" for i, account in enumerate(account_list)])
account_combobox.grid(row=1, column=1, padx=15, pady=5)

withdraw_button = ttk.Button(withdraw_frame, text="Withdraw", command=withdraw)
withdraw_button.grid(row=1, column=2, columnspan=1, padx=5, pady=5, sticky="ew")

# Edit frame
edit_frame = ttk.Frame(root)
edit_frame.pack(padx=10, pady=15, fill="x")

edit_var = tk.IntVar()
edit_var.set(1)

edit_label = ttk.Label(edit_frame, text="Select an account to edit:", foreground="#333333", font=("Helvetica", 12))
edit_label.grid(row=0, column=0, padx=5, pady=5)

edit_combobox = ttk.Combobox(edit_frame, state="readonly", values=[f"{i+1}: {account.name}" for i, account in enumerate(account_list)])
edit_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w") 

edit_radio1 = ttk.Radiobutton(edit_frame, text="Name", variable=edit_var, value=1)
edit_radio1.grid(row=0, column=2, padx=(15,0), pady=5, sticky="w") 

edit_radio2 = ttk.Radiobutton(edit_frame, text="Percent", variable=edit_var, value=2)
edit_radio2.grid(row=0, column=3, padx=(0,2), pady=0, sticky="w") 

edit_entryLabel = ttk.Label(edit_frame, text="Enter new edit:", foreground="#333333", font=("Helvetica", 11))
edit_entryLabel.grid(row=1, column=0, padx=5, pady=5, sticky="e")

edit_entry = ttk.Entry(edit_frame)
edit_entry.grid(row=1, column=1, padx=5, pady=5)  

edit_button = ttk.Button(edit_frame, text="Confirm Edit", command=edit)
edit_button.grid(row=1, column=2, padx=10, pady=5, sticky="ew")  

# Add frame
add_frame = ttk.Frame(root)
add_frame.pack(padx=10, pady=15, fill="x")

name_title = ttk.Label(add_frame, text="Add a new account:", foreground="#333333", font=("Helvetica", 12))
name_title.grid(row=0, column=0, padx=5, pady=5, sticky="w")

name_label = ttk.Label(add_frame, text="Name:", foreground="#333333", font=("Helvetica", 11))
name_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

name_entry = ttk.Entry(add_frame)
name_entry.grid(row=1, column=1, padx=5, pady=5)

percent_label = ttk.Label(add_frame, text="Percent:", foreground="#333333", font=("Helvetica", 11))
percent_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

percent_entry = ttk.Entry(add_frame)
percent_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = ttk.Button(add_frame, text="Add", command=add)
add_button.grid(row=2, column=2, padx=5, pady=5)

# Delete account frame
delete_frame = ttk.Frame(root)
delete_frame.pack(padx=10, pady=15, fill="x")

delete_label = ttk.Label(delete_frame, text="Choose an account to delete:", foreground="#333333", font=("Helvetica", 12))
delete_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

delete_combobox = ttk.Combobox(delete_frame, state="readonly", values=[f"{i+1}: {account.name}" for i, account in enumerate(account_list)])
delete_combobox.grid(row=0, column=1, padx=5, pady=5)

delete_button = ttk.Button(delete_frame, text="Confirm Delete", command=delete)
delete_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

# Undo button
undo_frame = ttk.Frame(root)
undo_frame.pack(padx=10, pady=15, fill="x")

undo_label = ttk.Label(undo_frame, text="Undo last action:", foreground="#333333", font=("Helvetica", 12))
undo_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

undo_button = ttk.Button(undo_frame, text="Undo", command=undo)
undo_button.grid(row=0, column=1, padx=10, pady=5, sticky="e")

# Details frame
details_frame = ttk.Frame(root)
details_frame.pack(padx=10, pady=10)

name_header = ttk.Label(details_frame, text="Name", foreground="#333333", font=("Helvetica", 11, "bold"))
name_header.grid(row=0, column=0, padx=5, pady=5)

percent_header = ttk.Label(details_frame, text="Percent", foreground="#333333", font=("Helvetica", 11, "bold"))
percent_header.grid(row=0, column=1, padx=5, pady=5)

amount_header = ttk.Label(details_frame, text="Amount", foreground="#333333", font=("Helvetica", 11, "bold"))
amount_header.grid(row=0, column=2, padx=5, pady=5)

sort_details()
# Print initial account details
print_details()

# Save and Exit button
save_exit_button = ttk.Button(root, text="Save and Exit", command=save_and_exit)
save_exit_button.pack(padx=10, pady=(10,30))

root.mainloop()