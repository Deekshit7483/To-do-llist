import tkinter as tk
import tkinter.messagebox as msgbox
import hashlib

# Create a custom font with doubled font size
custom_font = ('Helvetica', 20)

# Background color
bg_color = "#f0f0f0"

# Function to hash the password
def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode())
    return sha256.hexdigest()

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()

    try:
        with open("useraccounts.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        msgbox.showerror("Error", "User database not found.")
        return

    for line in lines:
        stored_username, stored_password, _, _ = line.strip().split(',')
        if username == stored_username and hash_password(password) == stored_password:
            open_todo_list(username)
            return

    msgbox.showerror("Error", "Invalid username or password")

# Function to handle signup
def signup():
    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")

    signup_window.configure(bg="darkgrey")  # Background color

    tk.Label(signup_window, text="Username", font=custom_font, bg="darkgrey").pack()
    signup_username_entry = tk.Entry(signup_window, font=custom_font)
    signup_username_entry.pack()

    tk.Label(signup_window, text="Password", font=custom_font, bg="darkgrey").pack()
    signup_password_entry = tk.Entry(signup_window, show="*", font=custom_font)
    signup_password_entry.pack()

    tk.Label(signup_window, text="Gmail", font=custom_font, bg="darkgrey").pack()
    signup_gmail_entry = tk.Entry(signup_window, font=custom_font)
    signup_gmail_entry.pack()

    tk.Label(signup_window, text="Phone Number", font=custom_font, bg="darkgrey").pack()
    signup_phone_entry = tk.Entry(signup_window, font=custom_font)
    signup_phone_entry.pack()

    def register_user():
        new_username = signup_username_entry.get()
        new_password = hash_password(signup_password_entry.get())
        new_gmail = signup_gmail_entry.get()
        new_phone = signup_phone_entry.get()

        with open("useraccounts.txt", "a") as file:
            file.write(f"{new_username},{new_password},{new_gmail},{new_phone}\n")

        msgbox.showinfo("Success", "Signup completed successfully.")
        signup_window.destroy()

    signup_button = tk.Button(signup_window, text="Sign Up", command=register_user, font=custom_font, bg="#4CAF50", fg="white")
    signup_button.pack()

# Function to open the to-do list window
def open_todo_list(username):
    root.destroy()
    todo_root = tk.Tk()
    todo_root.title(f"Welcome, {username}'s To-Do List")

    todo_root.configure(bg="darkgrey")  # Background color

    def add_task():
        task = task_entry.get()
        deadline = deadline_entry.get()
        task_listbox.insert(tk.END, f"Task: {task}, Deadline: {deadline}")
        save_tasks(username)

    def remove_task():
        selected_task_index = task_listbox.curselection()
        if selected_task_index:
            task_listbox.delete(selected_task_index)
            save_tasks(username)

    def save_tasks(username):
        try:
            with open(f"{username}_tasks.txt", "w") as file:
                for task in task_listbox.get(0, tk.END):
                    file.write(task + '\n')
        except FileNotFoundError:
            msgbox.showerror("Error", "Tasks file not found.")

    tk.Label(todo_root, text=f"Welcome, {username}!", font=custom_font, bg="darkgrey").pack()

    tk.Label(todo_root, text="Task", font=custom_font, bg="darkgrey").pack()
    task_entry = tk.Entry(todo_root, font=custom_font)
    task_entry.pack()

    tk.Label(todo_root, text="Deadline", font=custom_font, bg="darkgrey").pack()
    deadline_entry = tk.Entry(todo_root, font=custom_font)
    deadline_entry.pack()

    add_task_button = tk.Button(todo_root, text="Add Task", command=add_task, font=custom_font, bg="#2196F3", fg="white")
    add_task_button.pack()

    remove_task_button = tk.Button(todo_root, text="Remove Task", command=remove_task, font=custom_font, bg="#F44336", fg="white")
    remove_task_button.pack()

    tk.Label(todo_root, text="To-Do List", font=custom_font, bg="darkgrey").pack()
    task_listbox = tk.Listbox(todo_root, height=10, width=50, font=custom_font, bg=bg_color)
    task_listbox.pack()

    try:
        with open(f"{username}_tasks.txt", "r") as file:
            saved_tasks = file.read().splitlines()
            for task in saved_tasks:
                task_listbox.insert(tk.END, task)
    except FileNotFoundError:
        pass

    todo_root.mainloop()

# Create the main login window
root = tk.Tk()
root.title("Login")

root.configure(bg="darkgrey")  # Background color

tk.Label(root, text="Username", font=custom_font, bg="darkgrey").pack()
username_entry = tk.Entry(root, font=custom_font)
username_entry.pack()

tk.Label(root, text="Password", font=custom_font, bg="darkgrey").pack()
password_entry = tk.Entry(root, show="*", font=custom_font)
password_entry.pack()

login_button = tk.Button(root, text="Login", command=login, font=custom_font, bg="#4CAF50", fg="white")
login_button.pack()

signup_button = tk.Button(root, text="Sign Up", command=signup, font=custom_font, bg="#2196F3", fg="white")
signup_button.pack()

root.mainloop()