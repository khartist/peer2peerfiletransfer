'''
|\---/|
| o_o |
 \_^_/
 /\_/\
( o.o )
 > ^ <
'''
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *
import re
import socket
import client ###neu doi client thi doi o day lai
import json
SERVER_IP = socket.gethostbyname(socket.gethostname()) # IP của máy chủ
SERVER_PORT = 5050  # Port của máy chủ
CLIENT_IP = socket.gethostbyname(socket.gethostname())  # Địa chỉ IP của client

class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("350x350")  
        self.root.configure(bg="#E8E8E8")
        self.config = {}
        self.load_config()
        self.sign_in_page()
        self.config_file_path = r"C:\Users\Admin\OneDrive\Documents\BKU\Junior\ComputerNetworking\peer2peerfiletransfer\Assignment1\config.json"

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
    def load_config(self):
        # Load the configuration from a file
        config_file_path = r"C:\Users\Admin\OneDrive\Documents\BKU\Junior\ComputerNetworking\peer2peerfiletransfer\Assignment1\config.json"  # Adjust the path to your configuration file
        try:
            with open(config_file_path, 'r') as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError:
            self.config = {}

    def update_file_path(self, new_file_path):
        self.config["file_path"] = new_file_path
        self.save_config()
        self.chooseDes()
        # self.chooseDes()  # After updating file_path, go to the chooseDes page

    def update_output_folder(self, new_output_folder):
        self.config["output_folder"] = new_output_folder
        self.save_config()
        # After updating output_folder, go back to the homeView page

    def save_config(self):
        # Save the updated configuration to the file
        with open(self.config_file_path, 'w') as config_file:
            json.dump(self.config, config_file, indent=4)

#=======================================================================================================
    def sign_in(self):
        response = client.login_user(self.username_entry.get(), self.password_entry.get())
        if response == False:
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
        client.register_user(username,password,confirm_password)
        self.sign_in_page()
        
        #response = self.send_registration_data_to_server(username, password, CLIENT_IP, SERVER_PORT)

      # if response == "200":
          #  messagebox.showinfo("Notification", "Registered successfully! Please login.")
#            self.sign_in_page()
   #     else:
      #      messagebox.showerror("Error", response)

#=========================Choose path===================#
    def choosePath(self):
        self.clear_window()
        self.root.title("Select Path")
        ttk.Label(self.root, text="Choose Path you want to make your Repository", font=("Arial", 15), background="#E8E8E8").pack(pady=15)
        sth = tk.StringVar()
        box = ttk.Entry(self.root, textvariable=sth)
        client.file_path = box.get()
        box.pack()
        ttk.Button(self.root, text="Confirm", command=lambda: self.update_file_path(box.get())).pack(pady=5)
    
    def chooseDes(self):
        self.clear_window()
        self.root.title("Select Destination")
        ttk.Label(self.root, text="Choose Path you want to publish file", font=("Arial", 15), background="#E8E8E8").pack(pady=15)
        sth = tk.StringVar()
        box = ttk.Entry(self.root, textvariable=sth)
        client.output_folder = box.get()
        box.pack()
        ttk.Button(self.root, text="Confirm", command=lambda: self.update_output_folder(box.get())).pack(pady=5)
        home_page()

    def change_frame(self, frame_name):
        if(frame_name == "homeView"):
            self.clear_window()
            self.root.destroy()
            home_page()
        elif(frame_name == "chooseDes"): 
            self.chooseDes()
        else: print("huhu")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
#=======================================================================================================
class home_page(Tk):    
    def __init__(self):
        super().__init__()
        self.title('Home')
        self.configure(bg="#E8E8E8")
        self.geometry("500x500")  
        ttk.Label(self, text="Welcome to the homepage!", font=("Arial", 16), background="#E8E8E8").pack(pady=20)

        buttonframe = Frame(self)
        buttonframe.pack(side="bottom")
        button1 = Button(buttonframe, border=0, width=20, pady=5, bg='#E8E8E8', text="Fetch", command=lambda: self.change_frame("fetchView"))
        button1.grid(row=0, column=0, padx=5, pady=5)
        button2 = Button(buttonframe, border=0, width=20, pady=5, bg='#E8E8E8', text="Publish", command=lambda: self.change_frame("publishView"))
        button2.grid(row=0, column=1, padx=5, pady=5)
        button2 = Button(buttonframe, border=0, width=20, pady=5, bg='#E8E8E8', text="Log Out", command=lambda: self.change_frame("logOut"))
        button2.grid(row=0, column=2, padx=5, pady=5)

        self.mainloop()
        
    def change_frame(self, frame_name):
        if(frame_name == "fetchView"):
            fetchView()
        elif(frame_name == "publishView"):
            publishView()
        elif(frame_name =="logOut"):
            client.logout_user()
        else: print("huhu")

#=========Publish view===============#

class publishView(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("700x350")  
        self.configure(bg="#E8E8E8")
        self.title('Publish')

        pingFrame = Frame(self)
        pingFrame.pack(side="top")
        introText = ttk.Label(pingFrame, text = "Use this function to publish a file", font=("Arial", 16)).grid(row=0)
        text1 = ttk.Label(pingFrame, text = "local name", font=("Arial", 16)).grid(row=1, column=0)
        self.des = tk.StringVar()
        box1 = Entry(pingFrame, textvariable=self.des)
        box1.grid(row=1, column =1)
        text2 = ttk.Label(pingFrame, text = "file name", font=("Arial", 16)).grid(row=2, column=0)
        self.l = tk.StringVar()
        box2 = ttk.Entry(pingFrame, textvariable=self.l)
        box2.grid(row=2, column =1)


        buttonframe = ttk.Frame(self)
        buttonframe.pack(side="bottom")
        button1=Button(buttonframe, border=0, width=20, pady=5, bg='#E8E8E8', text="Execute", command=lambda: self.doPublish((box1.get(), box2.get())))
        button1.grid(row=0, column=0, padx=5, pady=5)
        button2=Button(buttonframe, border=0, width=20, pady=5, bg='#E8E8E8', text="Quit", command=lambda: self.quit())
        button2.grid(row=0, column=1, padx=5, pady=5)

        self.mainloop()

    def quit(self):
        self.destroy()

    def doPublish(self, args):
        lname, fname = args
        msg = "publish "+ lname + " " + fname
        client.publish(msg)

#============Fetch view=======================#

class fetchView(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("350x350")  
        self.configure(bg="#E8E8E8")
        self.title("fetch")

        pingFrame = ttk.Frame(self)
        pingFrame.pack(side="top")
        text1 = ttk.Label(pingFrame, text = "Fetch File", font=("Arial", 16)).grid(row=1, column=0)
        introText = ttk.Label(pingFrame, text = "Use this function to fetch file", font=("Arial", 16)).grid(row=0)

        self.des = tk.StringVar()
        box = Entry(pingFrame, textvariable=self.des)
        box.grid(row=1, column =1)

        buttonframe = ttk.Frame(self)
        buttonframe.pack(side="bottom")
        button1=Button(buttonframe, border=0, width=20, pady=5, bg='#E8E8E8', text="Execute", command=lambda: self.doFetch(box.get()))
        button1.grid(row=0, column=0, padx=5, pady=5)
        button2=Button(buttonframe, border=0, width=20, pady=5, bg='#E8E8E8', text="Quit", command=lambda:self.quit())
        button2.grid(row=0, column=1, padx=5, pady=5)
        #button1.grid(row=0, column=0, padx=5, pady=5)
        #button1.pack()
        self.mainloop()

    def quit(self):
        self.destroy()

    def doFetch(self, args):
        file = args
        msg = "fetch " + file
        client.fetch(msg)
        


root = tk.Tk()
app = App(root)
root.mainloop()
