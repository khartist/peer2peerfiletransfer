from tkinter import *
from tkinter import font
from tkinter import Image
import tkinter.messagebox
import sqlite3
connection = sqlite3.connect('users.db')
cursor = connection.cursor()

command1 = """
    CREATE TABLE IF NOT EXISTS
    USERS(username text, password text)
"""
cursor.execute(command1)

cursor.execute()

class FirstPage(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#fff")
        self.title('File Transfer Admin')
        self.geometry("480x480")

    
        self.background = Label(self,text="Welcome back bro")
        self.background.pack()

        self.buttonframe = Frame(self)
        self.buttonframe.pack(side="bottom")

        self.button1=Button(self.buttonframe,border=0, width=20, pady=5, bg='#FECEFC', fg='#1B365C', text="Click here", command=lambda: self.change_frame("listPage"))
        self.button1.grid(row=0, column=0, padx=5, pady=5)

        self.mainloop()

    def change_frame(self, frame_name):
    # Destroy the button frame
        self.buttonframe.destroy()

    # Hide the FirstPage window
        self.withdraw()

    # Create and show the new frame
        if frame_name == "listPage":
            ListPage()

    # Close the FirstPage window
        self.destroy()


FILE_LIST = {'a.txt','b.pdf','c.docx','d.pdf','e.pptx', 'f.txt', 'm.txt', 'xxx.txt', 'lol.exe', 'ciscoPacketTrace.txt', 'yyy.txt'}
class ListPage(Tk):
    def __init__(self):
        super().__init__() 
        self.configure(bg="#fff")
        self.title('File Transfer Admin')
        self.geometry("700x250")
        
        listFrame = Frame(self, bg="black")
        label = Label(listFrame, text = "File list")
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
        button1=Button(buttonframe, border=0, width=20, pady=5, bg='#FECEFC', fg='#1B365C', text="Ping", command=lambda: self.change_frame("pingView"))
        button1.grid(row=0, column=0, padx=5, pady=5)
        button2=Button(buttonframe, border=0, width=20, pady=5, bg='#FECEFC', fg='#1B365C', text="Discover", command=lambda: self.change_frame("discoverView"))
        button2.grid(row=0, column=1, padx=5, pady=5)
        button3=Button(buttonframe, border=0, width=20, pady=5, bg='#FECEFC', fg='#1B365C', text="IP List", command=lambda: self.change_frame("listIPview"))
        button3.grid(row=0, column=2, padx=5, pady=5)

        listbox.pack()
        self.mainloop()

    def change_frame(self,frame_name):
        if frame_name == "pingView":
            pingView()
            self.close()
        elif frame_name == "discoverView":
            discoverView()
            self.close()
        elif frame_name == "listIPview":
            listIPview()
            self.close()

class pingView(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#fff")
        self.title('Ping')
        self.geometry("200x200")

        pingFrame = Frame(self, background="#fff")
        pingFrame.pack(side="top")
        text1 = Label(pingFrame, text = "Destination's IP").grid(row=0, column=0)

        des = StringVar()
        box = Entry(pingFrame, textvariable=des).grid(row=0, column =1)
        
        buttonframe = Frame(self)
        buttonframe.pack(side="bottom")
        button1=Button(buttonframe, border=0, width=20, pady=5, bg='#FECEFC', fg='#1B365C', text="Submit") #, command=lambda: self.change_frame("pingView"))
        button1.pack()

        self.mainloop()

class discoverView(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#fff")
        self.title('Discover')
        self.geometry("200x200")

        pingFrame = Frame(self, background="#fff")
        pingFrame.pack(side="top")
        text1 = Label(pingFrame, text = "Destination's IP").grid(row=0, column=0)

        des = StringVar()
        box = Entry(pingFrame, textvariable=des).grid(row=0, column =1)
        
        buttonframe = Frame(self)
        buttonframe.pack(side="bottom")
        button1=Button(buttonframe, border=0, width=20, pady=5, bg='#FECEFC', fg='#1B365C', text="Submit") #, command=lambda: self.change_frame("pingView"))
        button1.pack()

        self.mainloop()

IP_LIST = {'1.1.1.1','2.2.2.2','3.3.3.3','4.4.4.4','5.5.5.5', '6.6.6.6', '7.7.7.7', '8.8.8.8', '9.9.9.9'}
class listIPview(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#fff")
        self.title('IP list')
        self.geometry("200x200")


        listFrame = Frame(self, bg="black")
        label = Label(listFrame, text = "IP list")
        listbox = Listbox(listFrame, height = 10, 
                  width = 15, 
                  bg = "grey",
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg = "yellow")
        i = 1
        for item in IP_LIST: 
            listbox.insert(i, item)
            i = i + 1

        #scrollbar
        scrollbar =Scrollbar(listFrame, orient= 'vertical')
        scrollbar.pack(side= RIGHT, fill= BOTH)
        listbox.config(yscrollcommand= scrollbar.set)
        #Configure the scrollbar
        scrollbar.config(command= listbox.yview)
        
        listFrame.pack(side="top")
        label.pack()
        listbox.pack()

        self.mainloop()

if __name__ == "__main__":
    root = FirstPage()

    
