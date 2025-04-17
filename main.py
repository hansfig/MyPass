import customtkinter as ctk
from PIL import Image
from password_characters import letters, symbols, numbers
from random import choice, shuffle, randint
import pyperclip
import json
from tkinter import messagebox

# ---------------------------- SETUP ------------------------------- #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("themes/magenta.json")


window = ctk.CTk()
window.title("Password Manager")
window.geometry("600x500")
window.minsize(600, 500)
window.maxsize(600, 500)  # prevent resizing


# ---------------------------- FUNCTIONS ------------------------------- #
def find_password():
    website_search_entry = website_entry.get().strip().capitalize()

    try:
        with open("password.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("File Error", "No data file found.")
        if website_search_entry in file:
            found_password = data[website_search_entry]["password"]
            found_email = data[website_search_entry]["email"]
            messagebox.showinfo(
                "Login Info",
                f"Login info for {website_search_entry}:\n\nEmail: {found_email}\nPassword: {found_password}\n\nPassword copied to clipboard!",
            )
            pyperclip.copy(found_password)
        else:
            messagebox.showerror("Search Error", "Website not found.")


def generate_password():
    password_list = (
        [choice(letters) for _ in range(randint(8, 10))]
        + [choice(symbols) for _ in range(randint(2, 4))]
        + [choice(numbers) for _ in range(randint(2, 4))]
    )

    shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, "end")
    password_entry.insert(0, password)
    pyperclip.copy(password)


def save_to_file():
    website = website_entry.get().capitalize()
    email_username = email_username_entry.get()
    password = password_entry.get()
    new_data = {website: {"email": email_username, "password": password}}

    if not website or not password or not email_username:
        messagebox.showerror("ERROR", "Don't leave any fields empty!")
        return

    is_ok = messagebox.askokcancel(
        title=website,
        message=f"These are the details:\nEmail: {email_username}\nPassword: {password}\n\nSave it?",
    )

    if is_ok:
        try:
            with open("password.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        data.update(new_data)

        with open("password.json", "w") as file:
            json.dump(data, file, indent=4)

        website_entry.delete(0, "end")
        email_username_entry.delete(0, "end")
        password_entry.delete(0, "end")


# ---------------------------- UI LAYOUT ------------------------------- #

main_frame = ctk.CTkFrame(window, corner_radius=10)
main_frame.pack(pady=0, padx=0, fill="both", expand=True)

# Logo Image
try:
    logo_image = ctk.CTkImage(Image.open("logo.png"), size=(285, 285))
    logo_label = ctk.CTkLabel(main_frame, image=logo_image, text="")
    logo_label.image = logo_image  # Keep reference
    logo_label.pack(pady=(0, 2))
except Exception as e:
    ctk.CTkLabel(main_frame, text=f"Image failed to load: {e}").pack()

# Input Fields
input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
input_frame.pack(pady=0, padx=0)

ctk.CTkLabel(input_frame, text="Website:").grid(
    row=0, column=0, padx=5, pady=10, sticky="e"
)
website_entry = ctk.CTkEntry(input_frame, width=240)
website_entry.grid(row=0, column=1, padx=5, pady=10)
website_entry.focus()
ctk.CTkButton(input_frame, text="Search", command=find_password).grid(
    row=0, column=2, padx=5, pady=10
)

ctk.CTkLabel(input_frame, text="Email/Username:").grid(
    row=1, column=0, padx=5, pady=10, sticky="e"
)
email_username_entry = ctk.CTkEntry(input_frame, width=240)
email_username_entry.grid(row=1, column=1, padx=5, pady=10)

ctk.CTkLabel(input_frame, text="Password:").grid(
    row=2, column=0, padx=5, pady=10, sticky="e"
)
password_entry = ctk.CTkEntry(input_frame, width=240)
password_entry.grid(row=2, column=1, padx=5, pady=10)
ctk.CTkButton(input_frame, text="Generate", command=generate_password).grid(
    row=2, column=2, padx=5, pady=10
)

ctk.CTkButton(main_frame, text="Add", command=save_to_file, width=200).pack(pady=20)

window.mainloop()
