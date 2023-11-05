import tkinter as tk
from tkinter import messagebox, ttk
import re
import socket
import client2 ###neu doi client thi doi o day lai
import json
SERVER_IP = '127.0.0.1'  # IP của máy chủ
SERVER_PORT = 5050  # Port của máy chủ
CLIENT_IP = socket.gethostbyname(socket.gethostname())  # Địa chỉ IP của client

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
#=========================Choose path===================#
    def choosePath(self):
        self.clear_window()
        self.root.title("Select Path")
        ttk.Label(self.root, text="Choose Path you want to send file", font=("Arial", 15), background="#E8E8E8").pack(pady=15)
        sth = tk.StringVar()
        box = tk.Entry(self.root, textvariable=sth)
        client2.file_path = box.get()
        ttk.Button(self.root, text="Confirm", command=self.chooseDes()).pack(pady=5)
    
    def chooseDes(self):
        self.clear_window()
        self.root.title("Select Destination")
        ttk.Label(self.root, text="Choose Path you want to store file", font=("Arial", 15), background="#E8E8E8").pack(pady=15)
        sth = ttk.StringVar()
        box = ttk.Entry(self.root, textvariable=sth)
        client2.output_folder = box.get()
        ttk.Button(self.root, text="Confirm", command=self.home_page()).pack(pady=5)

#=======================================================================================================
    def sign_in(self):
        response = self.send_login_data_to_server(self.username_entry.get(), self.password_entry.get())
        if response == "200":
            messagebox.showinfo("Notification", "Sign In successfully!")
            self.choosePath() #chon path truoc roi moi vao home page
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
        
        #response = self.send_registration_data_to_server(username, password, CLIENT_IP, SERVER_PORT)

      # if response == "200":
          #  messagebox.showinfo("Notification", "Registered successfully! Please login.")
#            self.sign_in_page()
   #     else:
      #      messagebox.showerror("Error", response)

#=======================================================================================================
    def home_page(self):
        self.clear_window()
        self.root.title("Home")
        self.root.geometry("350x350")  
        ttk.Label(self.root, text="Welcome to the homepage!", font=("Arial", 16), background="#E8E8E8").pack(pady=20)

        ttk.buttonframe = ttk.Frame(self)
        ttk.buttonframe.pack(side="bottom")
        ttk.button1 = ttk.Button(ttk.buttonframe, border=0, width=20, pady=5, bg='#E8E8E8', text="Fetch", command=lambda: self.change_frame("fetchView"))
        ttk.button1.grid(row=0, column=0, padx=5, pady=5)
        ttk.button2 = ttk.Button(ttk.buttonframe, border=0, width=20, pady=5, bg='#E8E8E8', text="Publish", command=lambda: self.change_frame("publishView"))
        ttk.button2.grid(row=0, column=1, padx=5, pady=5)

    def change_frame(self, frame_name):
        if(frame_name == "fetchView"):
            fetchView()
        elif(frame_name == "publishView"):
            publishView()
        else: print("huhu")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class publishView(ttk):
    def __init__(self):
        super.__init__()
        self.root.geometry("700x350")  
        self.root.configure(bg="#E8E8E8")
        self.geometry("350x350")

        pingFrame = ttk.Frame(self, background="#E8E8E8")
        pingFrame.pack(side="top")
        introText = ttk.Label(pingFrame, text = "Use this function to publish a file", font=("Arial", 16)).grid(row=0)
        text1 = ttk.Label(pingFrame, text = "local name", font=("Arial", 16)).grid(row=1, column=0)
        self.des = ttk.StringVar()
        box1 = ttk.Entry(pingFrame, textvariable=self.des)
        box1.grid(row=1, column =1)
        text2 = ttk.Label(pingFrame, text = "file name", font=("Arial", 16)).grid(row=2, column=0)
        self.des = ttk.StringVar()
        box2 = ttk.Entry(pingFrame, textvariable=self.des)
        box2.grid(row=2, column =1)


        buttonframe = ttk.Frame(self)
        buttonframe.pack(side="bottom")
        button1=ttk.Button(buttonframe, border=0, width=20, pady=5, bg='#E8E8E8', text="Execute", command=lambda: doPublish(box1.get(), box2.get()))
        button1.grid(row=0, column=0, padx=5, pady=5)
        button2=ttk.Button(buttonframe, border=0, width=20, pady=5, bg='#FFF9E3', fg='#1B365C', text="Quit", command=lambda: quit())
        button2.grid(row=0, column=1, padx=5, pady=5)

        def quit():
            self.destroy()

        def doPublish(lname, fname):
            msg = "publish "+ lname + " " + fname
            client2.publish(msg)

class fetchView(ttk):
    def __init__(self):
        super.__init__()
        self.root.geometry("350x350")  
        self.root.configure(bg="#E8E8E8")
        self.geometry("700x350")

        pingFrame = ttk.Frame(self, background="#E8E8E8")
        pingFrame.pack(side="top")
        text1 = ttk.Label(pingFrame, text = "Fetch File", font=("Arial", 16)).grid(row=1, column=0)
        introText = ttk.Label(pingFrame, text = "Use this function to fetch file", font=("Arial", 16)).grid(row=0)

        self.des = ttk.StringVar()
        box = ttk.Entry(pingFrame, textvariable=self.des)
        box.grid(row=1, column =1)

        buttonframe = ttk.Frame(self)
        buttonframe.pack(side="bottom")
        button1=ttk.Button(buttonframe, border=0, width=20, pady=5, bg='#E8E8E8', text="Execute", command=lambda: doFetch(box.get()))
        button1.grid(row=0, column=0, padx=5, pady=5)
        button2=ttk.Button(buttonframe, border=0, width=20, pady=5, bg='#FFF9E3', fg='#1B365C', text="Quit", command=lambda: quit())
        button2.grid(row=0, column=1, padx=5, pady=5)
        #button1.grid(row=0, column=0, padx=5, pady=5)
        #button1.pack()

        def quit():
            self.destroy()

        def doFetch(file):
            msg = "fetch "+ client2.file_path+file
            client2.fetch(msg)




root = tk.Tk()
app = App(root)
root.mainloop()