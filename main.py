import json
from tkinter import *
from tkinter import messagebox
import random
import pw_attributes_data
import pyperclip

LOGO_FILE = "logo.png"
FREQUENTLY_USED_EMAIL = "geniusminds777@gmail.com"



# ---------------------------- CLOSE POPUP MESSAGEBOX -------------------------------- #
def close_window():
    is_ok = messagebox.askokcancel(title="", message="Are you sure to close the app?")
    if is_ok:
        window.destroy()

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pw_btn_clicked():
    password_entry.delete(first=0, last=END)
    generate_password()

def generate_password():
    char = pw_attributes_data.letters
    num = pw_attributes_data.numbers
    sym = pw_attributes_data.symbols

    password_length = random.randint(12, 16)

    random_pw_arr = [random.choice(char + num + sym) for _ in range(password_length)]
    password_generated = "".join(random_pw_arr)

    password_entry.insert(0, password_generated)
    pyperclip.copy(password_generated) # it's auto-copied to clipboard!


# ------------------------- SEARCH EMAIL/PASSWORD ---------------------------#

def find_password():
    website_input = website_entry.get()

    try:
        with open("data.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Data file does not exist.")
    else:
        if website_input in data:
            messagebox.showinfo(title=f"{data[website_input]}",
                                message=f"Account: {data[website_input]["email"]}\nPassword: {data[website_input]["password"]}")
            pyperclip.copy(data[website_input]["password"])
        else:
            messagebox.showinfo(title="Error", message="The website was not found.")


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website_input = website_entry.get()
    email_input = email_entry.get()
    password_input = password_entry.get()
    #josn data structure blueprint
    json_data = {
        website_input: {
            "email": email_input,
            "password": password_input,
        }
    }

    is_ok = messagebox.askokcancel(title=website_input, message=f"There are details entered: \nWebsite: {website_input}\nAccount: {email_input} \nPassword: {password_input}")

    if is_ok:
        if len(website_input) <= 0 or len(email_input) <= 0 or len(password_input) <= 0:
            messagebox.showerror(website_input, "Please fill out all the inputs.")
        else:
            try:
                ## UPDATING -- ADD NEW DATA into EXISTING DATA
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(json_data, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(json_data)
                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                # email_entry.delete(0, END)
                password_entry.delete(0, END)
                messagebox.showinfo(title=website_input, message="Successfully saved!")



# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
window.protocol("WM_DELETE_WINDOW", close_window)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file=LOGO_FILE)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels:
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)


# Entries:
website_entry = Entry(width=24)
website_entry.grid(row=1, column=1)
website_entry.focus()


email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, FREQUENTLY_USED_EMAIL)


password_entry = Entry(width=24)
password_entry.grid(row=3, column=1)


# Buttons:
search_btn = Button(text="Search", padx=4, pady=3, command=find_password)
search_btn.grid(row=1, column=2)

gen_pw_btn = Button(text="Gen PW", padx=4, pady=3, command=gen_pw_btn_clicked)
gen_pw_btn.grid(row=3, column=2)

add_btn = Button(text="Add", width=33, command=save)
add_btn.grid(row=4, column=1, columnspan=2)




window.mainloop()





