'''
  _      _      _
>(.)__ <(.)__ =(.)__
 (___/  (___/  (___/  hjw
'''
from tkinter import *
from tkinter import font
from tkinter import Image
import tkinter.messagebox
import server

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

        self.button1=Button(self.buttonframe,border=0, width=20, pady=5, bg='#FFF9E3', fg='#1B365C', text="Click here", command=lambda: self.change_frame("listPage"))
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


#FILE_LIST = {('0.0.0.0', 'a.txt')}
class ListPage(Tk):
    def __init__(self):
        super().__init__() 
        self.configure(bg="#fff")
        self.title('File Transfer Admin')
        self.geometry("700x400")
        
        listFrame = Frame(self, bg="#fff")
        label = Label(listFrame, text="File list")
        listbox = Listbox(listFrame, height=10, width=15, bg="#E3FFFC", activestyle='dotbox', font="Helvetica", fg="#050505")

        # Function to update the listbox contents
        def update_listbox():
            listbox.delete(0, "end")  # Clear the listbox
            FILE_LIST = server.getFileList()
            for item in FILE_LIST: 
                ip = item[0]
                file = item[1]
                display_text = f"{ip}: {file}"
                listbox.insert("end", display_text)

                
            print("Update view")  # Schedule the next update after 5 seconds

        def schedule_update():
            update_listbox()
            self.after(10000, schedule_update)

        schedule_update()  # Initial call to populate the listbox

        # Scrollbar
        scrollbar = Scrollbar(listFrame, orient='vertical')
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        listFrame.pack(side="top")
        label.pack()
        listbox.pack()

        buttonframe = Frame(self)
        buttonframe.pack(side="bottom")
        button1 = Button(buttonframe, border=0, width=20, pady=5, bg='#FFF9E3', fg='#1B365C', text="Ping", command=lambda: self.change_frame("pingView"))
        button1.grid(row=0, column=0, padx=5, pady=5)
        button2 = Button(buttonframe, border=0, width=20, pady=5, bg='#FFF9E3', fg='#1B365C', text="Discover", command=lambda: self.change_frame("discoverView"))
        button2.grid(row=0, column=1, padx=5, pady=5)
        button3 = Button(buttonframe, border=0, width=20, pady=5, bg='#FFF9E3', fg='#1B365C', text="Online IP List", command=lambda: self.change_frame("onlineView"))
        button3.grid(row=1, column=0, padx=5, pady=5)
        button4 = Button(buttonframe, border=0, width=20, pady=5, bg='#FFF9E3', fg='#1B365C', text="Quit", command=lambda: self.change_frame("quit"))
        button4.grid(row=1, column=1, padx=5, pady=5)

        self.mainloop()

    def change_frame(self,frame_name):
        if frame_name == "pingView":
            pingView()
            self.close()
        elif frame_name == "discoverView":
            discoverView()
            self.close()
        elif frame_name == "onlineView":
            onlineView()
            self.close()
        elif frame_name == "quit":
            self.withdraw()
            self.destroy()
            exit()

class pingView(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#fff")
        self.title('Ping')
        self.geometry("600x200")

        pingFrame = Frame(self, background="#fff")
        pingFrame.pack(side="top")
        text1 = Label(pingFrame, text = "Destination's hostname").grid(row=1, column=0)
        introText = Label(pingFrame, text = "Use this function to check if an hostname is online").grid(row=0)

        self.des = StringVar()
        box = Entry(pingFrame, textvariable=self.des)
        box.grid(row=1, column =1)
        buttonframe = Frame(self)
        buttonframe.pack(side="bottom")
        button1=Button(buttonframe, border=0, width=20, pady=5, bg='#FFF9E3', fg='#1B365C', text="Execute", command=lambda: respond(box.get()))
        button1.pack()

        def respond(var):
            print(var)
            state = server.pingSearchInDB(var)
            if(state == True):
                respondFrame = Frame(self)
                respondFrame.pack(side="top")
                label = Label(respondFrame, text = "this hostname is online")
                label.pack()
                buttonframe = Frame(self)
                buttonframe.pack(side="bottom")
                button1=Button(buttonframe, border=0, width=20, pady=5, bg='#FFF9E3', fg='#1B365C', text="Quit", command=lambda: quit())
                button1.pack()
                buttonframe.pack()

                print("YES")
                
            elif(state == False):
                respondFrame = Frame(self)
                respondFrame.pack(side="top")
                label = Label(respondFrame, text = "this hostname is offline")
                label.pack()
                buttonframe = Frame(self)
                buttonframe.pack(side="bottom")
                button1=Button(buttonframe, border=0, width=20, pady=5, bg='#FFF9E3', fg='#1B365C', text="Quit", command=lambda: quit())
                button1.pack()
                buttonframe.pack()
                print("NO")
            else: 
                print("Ahuhu can not do anything lmao lmao lmao lmao")

        def quit():
            self.destroy()

        self.mainloop()


class discoverView(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#fff")
        self.title('Discover')
        self.geometry("550x300")

        pingFrame = Frame(self, background="#fff")
        pingFrame.pack(side="top")
        text1 = Label(pingFrame, text = "Destination's hostname").grid(row=1, column=0)
        introText = Label(pingFrame, text = "Use this function to get file list from an hostname").grid(row=0)

        self.des = StringVar()
        box = Entry(pingFrame, textvariable=self.des)
        box.grid(row=1, column =1)
        
        buttonframe = Frame(self)
        buttonframe.pack(side="bottom")
        button1=Button(buttonframe, border=0, width=20, pady=5, bg='#FFF9E3', fg='#1B365C', text="Submit", command=lambda: fileListView(box.get()))
        #button1.grid(row=0, column=0, padx=5, pady=5)
        button1.pack()
        

        def fileListView(var):
            #discoverList = server.discover(des)
            #discoverList = DISCOVER_TEST_LIST
            listFrame = Frame(self, bg="#fff")
            label = Label(listFrame, text="File list")
            listbox = Listbox(listFrame, height=10, width=15, bg="#E3FFFC", activestyle='dotbox', font="Helvetica", fg="#050505")
            listbox.delete(0, "end")  # Clear the listbox
            FILE_LIST = server.discoverGUI(var)
            #FILE_LIST = {'a.txt','b.pdf','c.docx','d.pdf','e.pptx', 'f.txt', 'm.txt', 'xxx.txt', 'lol.exe', 'ciscoPacketTrace.txt', 'yyy.txt'}
            for item in FILE_LIST: 
                listbox.insert("end", item)
            #self.after(15000, update_listbox)


            scrollbar = Scrollbar(listFrame, orient='vertical')
            scrollbar.pack(side="right", fill="y")
            listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=listbox.yview)
            print("Update view")

            
            buttonframe = Frame(self)
            buttonframe.pack(side="bottom")
            button1=Button(buttonframe, border=0, width=20, pady=5, bg='#FFF9E3', fg='#1B365C', text="Quit", command=lambda: quit())
            button1.pack()
            listFrame.pack()
            listbox.pack()
            label.pack()

        def quit():
            self.destroy()

        self.mainloop()



#IP_LIST = {'1.1.1.1','2.2.2.2','3.3.3.3','4.4.4.4','5.5.5.5', '6.6.6.6', '7.7.7.7', '8.8.8.8', '9.9.9.9'}
class onlineView(Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg="#fff")
        self.title('IP list')
        self.geometry("400x400")

        listFrame = Frame(self, bg="#E3FFFC")
        label = Label(listFrame, text="IP list")
        listbox = Listbox(listFrame, height=10, width=15,bg="#E3FFFC", activestyle='dotbox', font="Helvetica", fg="#050505")

        # Function to update the listbox contents
        def update_listbox():
            listbox.delete(0, "end")  # Clear the listbox
            i = 1
            IP_LIST = server.getIPList()
            for item in IP_LIST:
                listbox.insert(i, item)
                i = i + 1
            self.after(1000, update_listbox) # Schedule the next update after 1 second
            print("1 second has pass") 

        update_listbox()  # Initial call to populate the listbox

        # Scrollbar
        scrollbar = Scrollbar(listFrame, orient='vertical')
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        listFrame.pack(side="top")
        label.pack()
        listbox.pack()

        buttonframe = Frame(self)
        buttonframe.pack(side="bottom")
        button1=Button(buttonframe, border=0, width=20, pady=5, bg='#FFF9E3', fg='#1B365C', text="Quit", command=lambda: quit())
        #button1.grid(row=0, column=0, padx=5, pady=5)
        button1.pack()

        def quit():
            self.destroy()

        self.mainloop()
    

if __name__ == "__main__":
    root = FirstPage()

    
