import tkinter as tk
from tkinter import messagebox, ttk
import re

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

    def sign_in(self):
                # query với server để có thể đăng nhập tk khác, dưới là tk mặc định
        username = "BrianDuong"
        password = "Quan@2802"
        # Nav tới trang chủ
        if self.username_entry.get() == username and self.password_entry.get() == password:
            messagebox.showinfo("Notification", "Sign In successfully!")
            self.home_page()
        else:
            messagebox.showerror("Error", "Incorrect username or password!")

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

        # lưu account info ( implement cái này với server)
        #...
        messagebox.showinfo("Notification", "Registered successfully! Please login.")
        self.sign_in_page()

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
