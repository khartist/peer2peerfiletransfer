import tkinter as tk
from tkinter import messagebox, ttk
from client3 import login_user  
from client3 import register_user
import re
import socket


HEADER = 64 
FORMAT = "utf-8"
CENTRAL_SERVER_IP = socket.gethostbyname(socket.gethostname())
CENTRAL_SERVER_PORT = 5050  # Adjust the port as needed
SUCCESS_MESSAGE = "Kết nối thành công - 1"
class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("350x350")  
        self.root.configure(bg="#E8E8E8")
        self.sign_in_page()

    def sign_in_page(self):
        self.clear_window()
        self.root.title("Sign In/Sign Up")

        ttk.Label(self.root, text="Sign In", font=("Arial", 15), background="#E8E8E8").pack(pady=15)
        
        ttk.Label(self.root, text="Username", background="#E8E8E8").pack(pady=5)
        self.username_entry = ttk.Entry(self.root, width= 30)
        self.username_entry.pack(pady=5)

        ttk.Label(self.root, text="Password", background="#E8E8E8").pack(pady=5)
        self.password_entry = ttk.Entry(self.root, show="*", width = 30)
        self.password_entry.pack(pady=5)

        ttk.Button(self.root, text="Sign In", command=self.sign_in).pack(pady=20)
        ttk.Button(self.root, text="Go to Register", command=self.sign_up_page).pack(pady=5)
#=======================================================================================================
    def sign_in(self):
        login_user(self.username_entry.get(), self.password_entry.get())
        response = self.receive_from_server()
        if response == "Kết nối thành công - 1":
            messagebox.showinfo("Notification", "Sign In successfully!")
            self.home_page()
        else: 
            messagebox.showerror("Error", "Incorrect username or password!")

  

#=======================================================================================================
    
    def sign_up_page(self):
        self.clear_window()
        self.root.title("Sign In/Sgin Up")

        ttk.Label(self.root, text="Register", font=("Arial", 15), background="#E8E8E8").pack(pady=15)

        ttk.Label(self.root, text="Username", background="#E8E8E8", width=30).pack(pady=5)
        self.new_username_entry = ttk.Entry(self.root, width=30)
        self.new_username_entry.pack(pady=5)

        ttk.Label(self.root, text="Password", background="#E8E8E8", width=30).pack(pady=5)
        self.new_password_entry = ttk.Entry(self.root, show="*", width=30)
        self.new_password_entry.pack(pady=5)

        ttk.Label(self.root, text="Confirm Password", background="#E8E8E8", width=30).pack(pady=5)
        self.confirm_password_entry = ttk.Entry(self.root, show="*", width=30)
        self.confirm_password_entry.pack(pady=5)

        ttk.Button(self.root, text="Register", command=self.sign_up).pack(pady=20)
        ttk.Button(self.root, text="Go to Sign In", command=self.sign_in_page).pack(pady=5)

    def receive_from_server(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT))
            message_header = client.recv(HEADER)
            if len(message_header):
                message_length = int(message_header.decode(FORMAT).strip())
                message = client.recv(message_length).decode(FORMAT)
                return message
            else:
                return None
        except ConnectionError:
            messagebox.showerror("Connection Error", "Unable to connect to the server.")
            return None
        finally:
            client.close()
        
    def sign_up(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not re.match("^[a-zA-Z][a-zA-Z0-9]{3,11}$", username):
            messagebox.showerror("Error", "Invalid username!")
            return

        if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
            messagebox.showerror("Error", "Invalid password!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Password confirmation does not match!")
            return
        register_user(username, password, confirm_password)
        response = self.receive_from_server()
        if response == "Account created successfully - 1":
            messagebox.showinfo("Notification", "Registered successfully! Please login.")
            self.sign_in_page()
        elif response == "Error. Try again...":
            messagebox.showerror("Error", response)
        else:
            messagebox.showerror("Error", "Account already exists! Try again...")

#=======================================================================================================
    def home_page(self):
        self.clear_window()
        self.root.title("Home")
        ttk.Label(self.root, text="Welcome to the homepage!", font=("Arial", 16), background="#E8E8E8").pack(pady=20)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

root = tk.Tk()
app = App(root)
root.mainloop()