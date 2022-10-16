from tkinter import *
from tkinter import messagebox
from random import shuffle, randint, choice
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    letters_char = [choice(letters) for nr in range(randint(8, 10))]
    symbols_char = [choice(symbols) for nr in range(randint(2, 4))]
    numbers_char = [choice(numbers) for nr in range(randint(2, 4))]

    password_list = letters_char + symbols_char + numbers_char
    shuffle(password_list)
    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if website == "" or email == "" or password == "":
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \n"
                                                  f"Email: {email}\nPassword: {password}\n"
                                                  f"Is it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as f:
                    data = json.load(f)
                    data.update(new_data)
            except FileNotFoundError:
                with open("data.json", "w") as f:
                    json.dump(new_data, f, indent=4)
            else:
                with open("data.json", "w") as f:
                    json.dump(data, f, indent=4)
            website_entry.delete(0, "end")
            email_entry.delete(0, "end")
            password_entry.delete(0, "end")
            website_entry.focus()


# ---------------------------SEARCH PASSWORD--------------------------- #
def search_password():
    ask = website_entry.get()
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
        ask_email = data[ask]["email"]
        ask_password = data[ask]["password"]
    except KeyError:
        messagebox.showwarning(title="Oops", message="No Information")
    except FileNotFoundError:
        messagebox.showwarning(title="Oops", message="No File")
    else:
        messagebox.showinfo(title=website_entry.get(), message=f"Email: {ask_email}\n"
                                                       f"Password: {ask_password}")




# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)
canvas = Canvas(width=200, height=200)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=1)

#title
website_title = Label(text="Website:")
website_title.grid(row=1, column=0)
email_title = Label(text="Email/Username:")
email_title.grid(row=2, column=0)
password_title = Label(text="Password:")
password_title.grid(row=3, column=0)

#entry
website_entry = Entry(width=28)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=45)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "12345@gmail.com")
password_entry = Entry(width=28)
password_entry.grid(row=3, column=1)

#button
password_btn = Button(window, text="Generate Password", command=generate_password)
password_btn.grid(row=3, column=2)
add_btn = Button(window, text="Add", width=45, command=save_password)
add_btn.grid(row=4, column=1, columnspan=2)
search_btn = Button(window, text="Search",  width=16, command=search_password)
search_btn.grid(row=1, column=2)





window.mainloop()
