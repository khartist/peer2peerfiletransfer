from tkinter import *
from tkinter import font
from tkinter import Image
import tkinter.messagebox

class FirstPage(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#fff")
        self.title('File Transfer Admin')
        self.geometry("480x480")

    
        self.background = Label(self,text="Welcome back bro")
        self.background.pack()

        buttonframe = Frame(self)
        buttonframe.pack(side="bottom")

        button1=Button(buttonframe,border=0, width=20, pady=5, bg='#FECEFC', fg='#1B365C', text="Click here", command=lambda: self.change_frame("listPage"))
        button1.grid(row=0, column=0, padx=5, pady=5)

        self.mainloop()

    def change_frame(self,frame_name):
        # delete background
        self.background.pack_forget()
        # controller
        if frame_name == "listPage":
            ListPage()
            self.close()

FILE_LIST = {'a.txt','b.pdf','c.docx','d.pdf','e.pptx', 'f.txt', 'm.txt', 'xxx.txt', 'lol.exe', 'ciscoPacketTrace.txt', 'yyy.txt'}
class ListPage(Tk):
    def __init__(self):
        super().__init__() 
        self.configure(bg="#fff")
        self.title('File Transfer Admin')
        self.geometry("480x480")
        
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
        
        listFrame.pack(side = "top")
        label.pack()

        buttonframe = Frame(self)
        buttonframe.pack(side="bottom")
        button1=Button(buttonframe, border=0, width=20, pady=5, bg='#FECEFC', fg='#1B365C', text="Ping", command=lambda: self.change_frame("pingView"))
        button1.grid(row=1, column=1, padx=5, pady=5)
        button2=Button(buttonframe, border=0, width=20, pady=5, bg='#FECEFC', fg='#1B365C', text="Discover", command=lambda: self.change_frame("discoverView"))
        button2.grid(row=1, column=2, padx=5, pady=5)

        listbox.pack()
        self.mainloop()

    def change_frame(self,frame_name):
        if frame_name == "pingView":
            pingView()
            self.close()
        elif frame_name == "discoverView":
            discoverView()
            self.close()

class pingView(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#fff")
        self.title('Ping command')
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
        self.title('Discover command')
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

if __name__ == "__main__":
    root = FirstPage()
