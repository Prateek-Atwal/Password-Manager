from tkinter import*
import tkinter.messagebox as mb
import random
import json


# password generation logic
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    password_list = []

    password_list += [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_list += [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_list += [random.choice(numbers) for _ in range(random.randint(2, 4))]

    random.shuffle(password_list)
    password = "".join(password_list)

    window.clipboard_clear()
    window.clipboard_append(password)
    password_entry.delete(0, END)
    password_entry.insert(0, password)


# logic to save data entered into the fields
def add_info():
    cur_email = email_entry.get()
    cur_website = website_entry.get()
    cur_password = password_entry.get()
    pass_dict = {cur_website: {
        "email": cur_email,
        "password": cur_password
    }}
    if len(cur_email) == 0 or len(cur_website) == 0 or len(cur_password) == 0:
        mb.showwarning(title="Warning", message="Please enter all the fields to save")
        return
    user_input = mb.askokcancel(title="Save your changes?",
                                message=f"website: {cur_website}\nemail address: {cur_email}\npassword: {cur_password}")
    if user_input:
        try:
            data_file = open("passwords.json", "r")
        except FileNotFoundError:
            data = {}
        else:
            data = json.load(data_file)
        finally:
            data.update(pass_dict)
            data_file.close()

        with open("passwords.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
        website_entry.delete(0, END)
        password_entry.delete(0, END)


# Search functionality Logic
def search_website():
    key = website_entry.get()
    res = {}
    try:
        with open("passwords.json", "r") as data_file:
            data = json.load(data_file)
            res = data[key]
    except FileNotFoundError:
        with open("passwords.json", "w") as data_file:
            json.dump({}, data_file)
    except KeyError:
        mb.showinfo("Data Not Found", f"No details found for the website: {key}")
    finally:
        if len(res) > 0:
            mb.showinfo(key, f"Email:   {res['email']}\nPassword:   {res['password']}")
            window.clipboard_append(res["password"])
        website_entry.delete(0, END)
    return


# Logic to create UI
window = Tk()
icon = Canvas(width=200, height=200, bg="white", highlightbackground="white")
window.config(padx=50, pady=50, bg="white")

logo = PhotoImage(file="logo.png")
icon.create_image(100, 100, image=logo)
icon.grid(row=0, column=1)

website_label = Label(text="Website:", font=("Serif", 12, "normal"), bg="white", pady=4)
website_label.grid(row=1, column=0)

username_label = Label(text="Email/Username:", font=("Serif", 12, "normal"), bg="white", pady=4)
username_label.grid(row=2, column=0)

password_label = Label(text="Password:", font=("Serif", 12, "normal"), bg="white", pady=4)
password_label.grid(row=3, column=0)

website_entry = Entry(width=34, bg="white", highlightthickness=0.5)
website_entry.grid(row=1, column=1)
website_entry.focus_set()

email_entry = Entry(width=53, bg="white", highlightthickness=0.5)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "atwalprateek8@gmail.com")

password_entry = Entry(width=33, bg="white", highlightthickness=0.5)
password_entry.grid(row=3, column=1)

search_button = Button(width=14, text="Search", bg="white", highlightcolor="white", command=search_website)
search_button.grid(row=1, column=2)

generate_button = Button(text="Generate Password ", bg="white", highlightcolor="white", command=generate_password)
generate_button.grid(row=3, column=2)

add_button = Button(text="Add", bg="white", width=44, command=add_info)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
