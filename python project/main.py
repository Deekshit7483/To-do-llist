import tkinter as tk
import tkinter.messagebox as msgbox
from tkcalendar import DateEntry
import hashlib
from datetime import datetime

# Fonts
custom_font = ('Helvetica', 18)
label_font = ('Helvetica', 16)
button_font = ('Helvetica', 14)

# Color
bg_color = "#e0f7fa"         
input_bg_color = "#ffffff"  
button_bg_color = "#00796b"  
button_fg_color = "#ffffff"   
label_fg_color = "#004d40"   

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
    signup_window.configure(bg=bg_color, padx=20, pady=20)

    tk.Label(signup_window, text="Username", font=label_font, bg=bg_color, fg=label_fg_color).pack(anchor='w')
    signup_username_entry = tk.Entry(signup_window, font=custom_font, bg=input_bg_color, relief='solid', bd=1)
    signup_username_entry.pack(fill='x')

    tk.Label(signup_window, text="Password", font=label_font, bg=bg_color, fg=label_fg_color).pack(anchor='w')
    signup_password_entry = tk.Entry(signup_window, show="*", font=custom_font, bg=input_bg_color, relief='solid', bd=1)
    signup_password_entry.pack(fill='x')

    tk.Label(signup_window, text="Gmail", font=label_font, bg=bg_color, fg=label_fg_color).pack(anchor='w')
    signup_gmail_entry = tk.Entry(signup_window, font=custom_font, bg=input_bg_color, relief='solid', bd=1)
    signup_gmail_entry.pack(fill='x')

    tk.Label(signup_window, text="Phone Number", font=label_font, bg=bg_color, fg=label_fg_color).pack(anchor='w')
    signup_phone_entry = tk.Entry(signup_window, font=custom_font, bg=input_bg_color, relief='solid', bd=1)
    signup_phone_entry.pack(fill='x')

    def register_user():
        new_username = signup_username_entry.get()
        new_password = hash_password(signup_password_entry.get())
        new_gmail = signup_gmail_entry.get()
        new_phone = signup_phone_entry.get()

        with open("useraccounts.txt", "a") as file:
            file.write(f"{new_username},{new_password},{new_gmail},{new_phone}\n")

        msgbox.showinfo("Success", "Signup completed successfully.")
        signup_window.destroy()

    signup_button = tk.Button(signup_window, text="Sign Up", command=register_user, font=button_font,
                              bg=button_bg_color, fg=button_fg_color, padx=10, pady=5)
    signup_button.pack(pady=10)

# Function to open the to-do list window
def open_todo_list(username):
    root.destroy()
    todo_root = tk.Tk()
    todo_root.title(f"Welcome, {username}'s To-Do List")
    todo_root.configure(bg=bg_color, padx=20, pady=20)

    def add_task():
        task = task_entry.get()
        deadline = deadline_entry.get_date()

        # Validate task and deadline
        if not task:
            msgbox.showerror("Error", "Task is required.")
            return

        if not deadline:
            msgbox.showerror("Error", "Deadline is required.")
            return

        # Check if the selected date is in the past
        today = datetime.now().date()
        if deadline < today:
            msgbox.showerror("Error", "Deadline cannot be in the past.")
            return

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

    tk.Label(todo_root, text=f"Welcome, {username}!", font=custom_font, bg=bg_color, fg=label_fg_color).pack(pady=10)

    tk.Label(todo_root, text="Task", font=label_font, bg=bg_color, fg=label_fg_color).pack(anchor='w')
    task_entry = tk.Entry(todo_root, font=custom_font, bg=input_bg_color, relief='solid', bd=1)
    task_entry.pack(fill='x')

    tk.Label(todo_root, text="Deadline", font=label_font, bg=bg_color, fg=label_fg_color).pack(anchor='w')
    deadline_entry = DateEntry(todo_root, font=custom_font, bg=input_bg_color, relief='solid', bd=1,
                               date_pattern='yyyy-mm-dd', width=15)
    deadline_entry.pack(fill='x')

    add_task_button = tk.Button(todo_root, text="Add Task", command=add_task, font=button_font,
                                bg=button_bg_color, fg=button_fg_color, padx=10, pady=5)
    add_task_button.pack(pady=5)

    remove_task_button = tk.Button(todo_root, text="Remove Task", command=remove_task, font=button_font,
                                   bg="#d32f2f", fg=button_fg_color, padx=10, pady=5)
    remove_task_button.pack(pady=5)

    tk.Label(todo_root, text="To-Do List", font=label_font, bg=bg_color, fg=label_fg_color).pack(pady=10)
    task_listbox = tk.Listbox(todo_root, height=10, width=50, font=custom_font, bg=input_bg_color)
    task_listbox.pack(pady=10)

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
root.configure(bg=bg_color, padx=20, pady=20)

tk.Label(root, text="Username", font=label_font, bg=bg_color, fg=label_fg_color).pack(anchor='w')
username_entry = tk.Entry(root, font=custom_font, bg=input_bg_color, relief='solid', bd=1)
username_entry.pack(fill='x', pady=5)

tk.Label(root, text="Password", font=label_font, bg=bg_color, fg=label_fg_color).pack(anchor='w')
password_entry = tk.Entry(root, show="*", font=custom_font, bg=input_bg_color, relief='solid', bd=1)
password_entry.pack(fill='x', pady=5)

login_button = tk.Button(root, text="Login", command=login, font=button_font,
                         bg=button_bg_color, fg=button_fg_color, padx=10, pady=5)
login_button.pack(pady=10)

signup_button = tk.Button(root, text="Sign Up", command=signup, font=button_font,
                          bg="#2196f3", fg=button_fg_color, padx=10, pady=5)
signup_button.pack(pady=10)

root.mainloop()
