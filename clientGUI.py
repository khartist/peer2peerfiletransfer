from tkinter import *
from tkinter import font
from tkinter import Image
import tkinter.messagebox

class FirstPage(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#fff")
        self.title('Peer2peer File Transfer Service')
        self.geometry("1000x480")

    
        self.background = Label(self,text="Welcome back to our peer2peer file transfer service, the best service you'll ever see in the market. Use our service and never got spied by big corp again")
        self.background.pack()

        self.login = RegistryFrame(self, bground="white",fname="login")
        self.register = RegistryFrame(self, bground="white",fname="register")
        
        # buttons
        self.buttonframe = Frame(self)
        self.buttonframe.pack(side="bottom")

        button1=Button(self.buttonframe,border=0, width=50, pady=5, bg='#FECEFC', fg='#1B365C', text="Register", command=lambda: self.change_frame("register"))
        button1.grid(row=0, column=0, padx=5, pady=5)
        button1.grid_rowconfigure(0, weight=1)
        button2=Button(self.buttonframe,border=0, width=50, pady=5, bg='#FECEFC', fg='#1B365C', text="Login", command=lambda: self.change_frame("login"))
        button2.grid(row=0, column=1, padx=5, pady=5)
        self.mainloop()

    def auto_close(self):
        if self.login.close:
            self.login.close = -1 #stop sign
            self.destroy()

        elif self.login.close != -1: 
            self.after(1000, self.auto_close)
    def change_frame(self,frame_name):
        # delete background
        self.background.pack_forget()
        self.buttonframe.pack_forget()
        # controller
        if frame_name == "login":
            self.login.pack(fill='both', expand=1)
            self.register.pack_forget()
           # self.destroy()
        elif frame_name == "register":
            self.register.pack(fill='both', expand=1)
            self.login.pack_forget()
          #  self.destroy()
        else:
            print("Ahuhu :((")

# Subframe for First Page - Toggle between Login and Register Service
class RegistryFrame(Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(bg=kwargs["bground"])
        self.fname = kwargs["fname"]
        self.close = False 
        self.render()
    def delete(self):
        for widget in self.winfo_children():
            widget.destroy()
    def render(self):
        if self.fname == "login":
            label_0 = Label(self, fg="#57a1f8", bg="#fff", text="Login form", font=("Microsoft YaHei UI Light",25,"bold"))
            label_0.place(x=400,y=20)
            
            user = Entry(self, width=30, border=0)
            user.place(x=400,y=100)
            user.insert(0,'Username')
           # user.bind('<FocusIn>', lambda event: on_enter(event, "user"))
           # user.bind('<FocusOut>', lambda event: on_leave(event, "user"))
            #Frame(self, width=295, height=2,bg='black').place(x=95,y=120)

            passwd = Entry(self, width=30, border=0, show="*")
            passwd.place(x=400,y=150)
            passwd.insert(0,'Password')
            #passwd.bind('<FocusIn>', lambda event: on_enter(event, "passwd"))
          #  passwd.bind('<FocusOut>', lambda event: on_leave(event, "passwd"))
            #Frame(self, width=295, height=2,bg='black').place(x=95,y=170)

            submit = Button(self, text="Login", border=0, width=40, pady=5, bg='#FECEFC', fg='#1B365C', command=lambda: login_redirect())
            submit.place(x=400,y=220)

            def on_enter(_,name):
                if name == "user":
                    user.delete(0,END)
                elif name == "passwd":
                    passwd.delete(0,END)
                else:
                    pass
            def on_leave(_, name):
                if name == "user":
                    if user.get() == "":
                        user.insert(0,'Username')
                elif name == "passwd":
                    if passwd.get() == "":
                        passwd.insert(0,'Password')
                else:
                    pass
            
            def login_redirect():
                # Validate results
                if user.get() == "" or user.get() == "Username":
                    tkinter.messagebox.showerror(title="Lỗi đăng nhập",message="Nhập tên tài khoản !!")
                elif passwd.get() == "" or passwd.get() == "Password":
                    tkinter.messagebox.showerror(title="Lỗi đăng nhập",message="Nhập mật khẩu !!")
                else:
                    result = []
                    result = client.loginService(user.get(),passwd.get())
                    ## move to OnlineUserPage
                    if result==True:
                        self.close = True
                        funcPage()
                    #else:
                    #    tkinter.messagebox.showerror(title="Lỗi đăng nhập",message="Tài khoản hoặc mật khẩu không đúng!")
        
        
        elif self.fname == "register":
            label_0 = Label(self, fg="#57a1f8", bg="#fff", text="Welcome to our service", font=("Microsoft YaHei UI Light",25,"bold"))
            label_0.place(x=400,y=20)
            
            user = Entry(self, width=30, border=0)
            user.place(x=400,y=100)
            user.insert(0,'Username')

            passwd = Entry(self, width=30, border=0, show="*")
            passwd.place(x=400,y=150)
            passwd.insert(0,'Password')

            submit = Button(self, text="Register", border=0, width=40, pady=5, bg='#FECEFC', fg='#1B365C', command=lambda: register_redirect())
            submit.place(x=350,y=220)

FILE_LIST = {'a.txt','b.pdf','c.docx','d.pdf','e.pptx', 'f.txt', 'm.txt', 'xxx.txt', 'lol.exe', 'ciscoPacketTrace.txt', 'yyy.txt'}
class funcPage(Tk):
    def __init__(self):
        super().__init__() 
        self.configure(bg="#fff")
        self.title('peer2peer file transfer')
        self.geometry("700x250")

        listFrame = Frame(self, bg="black")
        label = Label(listFrame, text = "Local File list")
        listbox = Listbox(listFrame, height = 10, 
                  width = 15, 
                  bg = "grey",
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg = "yellow")
        i = 1
        for item in FILE_LIST: 
            listbox.insert(i, item)
            i = i + 1

        #scrollbar
        scrollbar =Scrollbar(listFrame, orient= 'vertical')
        scrollbar.pack(side= RIGHT, fill= BOTH)
        listbox.config(yscrollcommand= scrollbar.set)
        #Configure the scrollbar
        scrollbar.config(command= listbox.yview)
        
        listFrame.pack(side= "top")
        label.pack()

        buttonframe = Frame(self)
        buttonframe.pack(side="bottom")
        button1=Button(buttonframe, border=0, width=20, pady=5, bg='#FECEFC', fg='#1B365C', text="Fetch", command=lambda: self.change_frame("fetchView"))
        button1.grid(row=0, column=0, padx=5, pady=5)
        button2=Button(buttonframe, border=0, width=20, pady=5, bg='#FECEFC', fg='#1B365C', text="Publish", command=lambda: self.change_frame("publishView"))
        button2.grid(row=0, column=1, padx=5, pady=5)

        listbox.pack()
        self.mainloop()

    def change_frame(self,frame_name):
        if frame_name == "fetchView":
            fetchView()
            self.close()
        elif frame_name == "publishView":
            publishView()
            self.close()

class fetchView(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#fff")
        self.title('Fetch')
        self.geometry("200x200")

        pingFrame = Frame(self, background="#fff")
        pingFrame.pack(side="top")
        text1 = Label(pingFrame, text = "file name").grid(row=0, column=0)

        des = StringVar()
        box = Entry(pingFrame, textvariable=des).grid(row=0, column =1)
        
        buttonframe = Frame(self)
        buttonframe.pack(side="bottom")
        button1=Button(buttonframe, border=0, width=20, pady=5, bg='#FECEFC', fg='#1B365C', text="Execute") #, command=lambda: self.change_frame("pingView"))
        button1.pack()

        self.mainloop()

class publishView(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#fff")
        self.title('Ping')
        self.geometry("200x200")

        pingFrame = Frame(self, background="#fff")
        pingFrame.pack(side="top")
        text1 = Label(pingFrame, text = "Local file name").grid(row=0, column=0)

        lname = StringVar()
        box = Entry(pingFrame, textvariable=lname).grid(row=0, column =1)

        text2 = Label(pingFrame, text = "Publish file name").grid(row=1, column=0)

        fname = StringVar()
        box = Entry(pingFrame, textvariable=fname).grid(row=1, column =1)
        
        buttonframe = Frame(self)
        buttonframe.pack(side="bottom")
        button1=Button(buttonframe, border=0, width=20, pady=5, bg='#FECEFC', fg='#1B365C', text="Submit") #, command=lambda: self.change_frame("pingView"))
        button1.pack()

        self.mainloop()

if __name__ == "__main__":
    root = FirstPage()
