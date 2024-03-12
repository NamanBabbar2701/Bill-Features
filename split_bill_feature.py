import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image,ImageTk


# =====================Create the menu and order============================
menu = [
    {"name": "Tea", "category": "Beverages", "price": 15.0, "gst": 0.75},
    {"name": "Tea Adrak", "category": "Beverages", "price": 20.0, "gst": 0.4},
    {"name": "Masala Tea", "category": "Beverages", "price": 25.0, "gst": 1.25},
    {"name": "Coffee", "category": "Beverages", "price": 25.0, "gst": 1.25},
    {"name": "Cold Coffee", "category": "Beverages", "price": 40.0, "gst": 2},
    {"name": "Farm Fresh", "category": "Pizza", "price": 150.0, "gst": 7.5},
    {"name": "Mushroom Pizza", "category": "Pizza", "price": 120.0, "gst": 6},
    {"name": "Kulhad Pizza", "category": "Pizza", "price": 130.0, "gst": 6.5},
    {"name": "Veg Momos", "category": "Momo", "price": 80.0, "gst": 4},
    {"name": "Paneer Momos", "category": "Momo", "price": 100.0, "gst": 5},
    {"name": "Red Sauce Pasta", "category": "Pasta", "price": 180.0, "gst": 9},
    {"name": "Pink Sauce Pasta", "category": "Pasta", "price": 190.0, "gst": 9.5},
    {"name": "White Sauce Pasta", "category": "Pasta", "price": .0, "gst": 0.1},
    {"name": "Grill Sandwich", "category": "Sandwich", "price": 70.0, "gst": 3.5},
    {"name": "Cheese Sandwich", "category": "Sandwich", "price": 90.0, "gst": 4.5},
    {"name": "Veg Burger", "category": "Burger", "price": 50.0, "gst": 2.5},
    {"name": "Cheese Burger", "category": "Burger", "price": 70.0, "gst": 3.5},
    {"name": "Fried Rice", "category": "Rice", "price": 80.0, "gst": 4},
    {"name": "Schezwan Rice", "category": "Rice", "price": 100.0, "gst": 5},
    {"name": "Hakka Noodles", "category": "Noodles", "price": 90.0, "gst": 4.5},
    {"name": "Schezwan Noodles", "category": "Noodles", "price": 110.0, "gst": 5.5},
]

order = []

# Functions for GUI actions
def add_item():
    item = menu_listbox.get(menu_listbox.curselection())
    quantity = int(quantity_entry.get())
    for menu_item in menu:
        if menu_item["name"] == item:
            order.append({"menu_item": menu_item, "quantity": quantity})
            order_listbox.insert(tk.END, f"{menu_item['name']} x{quantity}")
            quantity_entry.delete(0, tk.END)
            break

def calculate_total():
    total = 0
    gst_total = 0
    for item in order:
        total_item_price = item["menu_item"]["price"] * item["quantity"]
        total += total_item_price
        gst_total += item["menu_item"]["gst"] * item["quantity"]
    return total, gst_total

def print_bill():
    total, gst_total = calculate_total()
    if not order:
        messagebox.showwarning("Empty Order", "Please enter items in your order first.")
        return
    bill_text.config(state=tk.NORMAL)
    bill_text.delete(1.0, tk.END)
    bill_text.insert(tk.END, "\n============================ Bill =============================\n")
    bill_text.insert(tk.END, "Item\t\tCategory\t\tPrice\tQuantity\tTotal\n")
    for item in order:
        total_item_price = item["menu_item"]["price"] * item["quantity"]
        bill_text.insert(tk.END, f"{item['menu_item']['name']}\t\t{item['menu_item']['category']}\t\t{item['menu_item']['price']}\t{item['quantity']}\t{total_item_price}\n")
    bill_text.insert(tk.END, "\nSubtotal: " + str(total) + "\n")
    bill_text.insert(tk.END, "GST: " + str(gst_total) + "\n")
    bill_text.insert(tk.END, "Grand Total: " + str(total + gst_total) + "\n")
    bill_text.config(state=tk.DISABLED)

def clear_order():
    order.clear()
    order_listbox.delete(0, tk.END)

def split_equal():
    num_guests_str = simpledialog.askinteger("Number of Guests for Equal Split", "Enter the number of guests:")
    if num_guests_str is None:
        return

    num_guests = int(num_guests_str)
    if num_guests <= 0:
        messagebox.showerror("Invalid Input", "Please enter a valid number of guests.")
        return

    total, gst_total = calculate_total()
    split_total = total / num_guests
    split_gst = gst_total / num_guests

    individual_split = []
    for i in range(num_guests):
        individual_split.append({
            "Guest": i + 1,
            "Subtotal": split_total,
            "GST": split_gst,
            "Total": split_total + split_gst
        })

    if not order:
        messagebox.showwarning("Empty Order", "Please enter items in your order first.")
        return

    bill_text.config(state=tk.NORMAL)
    bill_text.delete(1.0, tk.END)
    bill_text.insert(tk.END, "=== Equal Split Bill ===\n")
    bill_text.insert(tk.END, "Number of Guests: " + str(num_guests) + "\n\n")
    for item in individual_split:
        bill_text.insert(tk.END, f"Guest {item['Guest']}\n")
        bill_text.insert(tk.END, "Subtotal: " + str(item["Subtotal"]) + "\n")
        bill_text.insert(tk.END, "GST: " + str(item["GST"]) + "\n")
        bill_text.insert(tk.END, "Grand Total: " + str(item["Total"]) + "\n\n")
    bill_text.config(state=tk.DISABLED)

def create_itemwise_window():
    if not order:
        messagebox.showwarning("Empty Order", "Please enter items in your order first.")
        return

    itemwise_window = tk.Toplevel(root)
    itemwise_window.title("Itemwise Split")

    def itemwise_split():
        num_guests_str = num_guests_itemwise_entry.get()
        if not num_guests_str:
            messagebox.showerror("Invalid Input", "Please enter a valid number of guests.")
            return

        num_guests = int(num_guests_str)
        if num_guests <= 0:
            messagebox.showerror("Invalid Input", "Please enter a valid number of guests.")
            return

        guests_orders = []
        for i in range(num_guests):
            guest_order = []
            for item in order:
                max_quantity = item["quantity"]
                quantity = simpledialog.askinteger(f"Guest {i + 1}'s Order", f"How many {item['menu_item']['name']}s does Guest {i + 1} want?", minvalue=0, maxvalue=max_quantity)
                if quantity is not None and 0 < quantity <= max_quantity:
                    guest_order.append({"menu_item": item["menu_item"], "quantity": quantity})
                    item["quantity"] -= quantity
                elif quantity is not None and quantity > max_quantity:
                    messagebox.showwarning("Quantity Limit", f"Sorry, there are only {max_quantity} {item['menu_item']['name']}(s) available.")

            guests_orders.append(guest_order)

        order_frame.pack_forget()
        individual_bills_frame.pack()

        for i, guest_order in enumerate(guests_orders):
            bill_text.config(state=tk.NORMAL)
            bill_text.insert(tk.END, f"\n=== Individual Split Bill ===\n")
            bill_text.insert(tk.END, f"\n=== Guest {i + 1}'s Bill ===\n")
            bill_text.insert(tk.END, "Item\t\tCategory\t\tPrice\tQuantity\tTotal\n")
            for item in guest_order:
                total_item_price = item["menu_item"]["price"] * item["quantity"]
                bill_text.insert(tk.END, f"{item['menu_item']['name']}\t\t{item['menu_item']['category']}\t\t{item['menu_item']['price']}\t{item['quantity']}\t{total_item_price}\n")
            guest_total, guest_gst_total = calculate_individual_total(guest_order)
            bill_text.insert(tk.END, "\nSubtotal: " + str(guest_total) + "\n")
            bill_text.insert(tk.END, "GST: " + str(guest_gst_total) + "\n")
            bill_text.insert(tk.END, "Grand Total: " + str(guest_total + guest_gst_total) + "\n")
            bill_text.config(state=tk.DISABLED)

    num_guests_itemwise_label = tk.Label(itemwise_window, text="Number of Guests:")
    num_guests_itemwise_label.pack()
    num_guests_itemwise_entry = tk.Entry(itemwise_window)
    num_guests_itemwise_entry.pack()
    itemwise_split_button = tk.Button(itemwise_window, text="Split Itemwise", command=itemwise_split)
    itemwise_split_button.pack()

# Calculate individual total for itemwise split
def calculate_individual_total(guest_order):
    total = 0
    gst_total = 0
    for item in guest_order:
        total_item_price = item["menu_item"]["price"] * item["quantity"]
        total += total_item_price
        gst_total += item["menu_item"]["gst"] * item["quantity"]
    return total, gst_total

#==================================== Create the main application window============================================
#==================================================================================================================

# ========================================Setup====================================================================
root = tk.Tk()
root.title("Restaurant Bill Splitter")
root.wm_iconbitmap("11-removebg-preview.ico")
root.geometry("1550x800+0+0")
root.configure(background="#ffde59")

# ========================================================
# ===============image logo taken====================

img1 = Image.open("11-removebg-preview.png")
img1 = img1.resize((150, 80))
photo = ImageTk.PhotoImage(img1)
libling = tk.Label(root, image=photo, bd=4)
libling.place(x=0, y=0, width=120, height=80 )

# =============title=============================
lbl_title=tk.Label(root,text="CHAISAA",font="georgia 40 bold",bg="#ffde59",fg="black", bd=4)
lbl_title.place(x=120,y=0,width=1420,height=80)

#===============Main Frame=====================
frame1=tk.Frame(root,bd=6)
frame1.place(x=0,y=80,width=1550,height=720)

# ==========================menu label name=========================
menu_label=tk.Label(frame1,text="MENU",font="georgia 20 bold",bg="#ffde59",fg="black", bd=4)
menu_label.place(x=0,y=0,width=516, height=30 )

#=================================== Menu Listbox========================================
menu_listbox = tk.Listbox(frame1, bd=4, bg="lightgrey", font="georgia 16 bold")
for item in menu:
    menu_listbox.insert(tk.END, item["name"])
menu_listbox.place(x=0,y=30, width=516, height=480)

#
# ================================Quantity Label and Entry=================================
quantity_label = tk.Label(frame1, text="Quantity:", fg="blue", font="georgia 10 bold" )
quantity_label.place(x=0, y= 540, width=100, height=40)
quantity_entry = tk.Entry(frame1, bg="lightgrey", bd=5)
quantity_entry.place(x=100, y=540, height=40)

# ============================Added Item Button===================================
add_item_button = tk.Button(frame1, text="+", padx=8, font="georgia 20 bold", command=add_item, bd=5, bg="#ffde59",fg="black")
add_item_button.place(x=250, y= 540, width=50,height=35)


# ==========================order label name=========================
order_label=tk.Label(frame1,text="ORDER",font="georgia 20 bold",bg="#ffde59",fg="black", bd=4)
order_label.place(x=516,y=0,width=516, height=30 )

# ==========================Order Listbox selected from menu and added in them================
order_listbox = tk.Listbox(frame1, bg="lightgrey", bd=4, font="georgia 16 bold")
order_listbox.place(x=516,y=30, width=516, height=480)

#=========================================Calculate Total Button==========================================
calculate_total_button = tk.Button(frame1, text="Calculate Total", font="georgia 10 bold", bd=5, bg="#ffde59", fg="black", command=print_bill)
calculate_total_button.place(x=545, y= 540, height=40)

# ====================================Clear Order Button================================
clear_order_button = tk.Button(frame1, text="Clear Order", font="georgia 10 bold", bd=5, bg="#ffde59", fg="black", command=clear_order)
clear_order_button.place(x=890, y= 540, height=40)

# ==========================================Split Equal Button=============================
split_equal_button = tk.Button(frame1, text="Split Equal", font="georgia 10 bold", bd=5, bg="#ffde59", fg="black", command=split_equal)
split_equal_button.place(x=1100, y= 540, height=40)

# =====================================Split Itemwise Button===============================
split_itemwise_button = tk.Button(frame1, text="Split Itemwise", font="georgia 10 bold", bd=5, bg="#ffde59", fg="black", command=create_itemwise_window)
split_itemwise_button.place(x=1390, y= 540, height=40)

# ==========================bill label name=========================
bill_label=tk.Label(frame1,text="BILL",font="georgia 20 bold",bg="#ffde59",fg="black", bd=4)
bill_label.place(x=1032,y=0,width=518, height=30 )

#======================================= Bill Text ==========================
bill_text = tk.Text(frame1, height=20, width=50, bg="lightgrey", bd=4)
bill_text.place(x=1032,y=30, width=518, height=480)
bill_text.config(state=tk.DISABLED)

# # ============================Number of Guests for Equal Split Label and Entry==============================
# num_guests_label = tk.Label(root, text="Number of Guests for Equal Split:")
# num_guests_label.pack()
# num_guests_entry = tk.Entry(root)
# num_guests_entry.pack()

order_frame = tk.Frame(root)
individual_bills_frame = tk.Frame(root)

root.mainloop()
