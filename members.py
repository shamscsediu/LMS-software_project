from tkinter import *
from tkinter import messagebox
import sqlite3
import base
con = sqlite3.connect('LMS.db')
cur = con.cursor()

class StoreMember(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("800x800")
        self.title("Enter Member")
        self.resizable(False,False)

        self.top_frame = Frame(self, height=150, bg='grey')
        self.top_frame.pack(fill=X)
        heading = Label(self.top_frame, text='Add new member',font='arial 18 bold' ,bg='grey')
        heading.place(x=300, y=60)

        self.bodyframe = Frame(self,height=650,bg='white')
        self.bodyframe.pack(fill=X)

        self.lbl_member_name = Label(self.bodyframe, text='Enter name:', font='arial 12 bold', bg='white')
        self.lbl_member_name.place(x=40, y=40)
        self.txt_member_name = Entry(self.bodyframe, width=30, bd=2)
        self.txt_member_name.place(x= 200,y=45)

        self.lbl_phone = Label(self.bodyframe, text='Enter phone', font='arial 12 bold', bg='white')
        self.lbl_phone.place(x=40, y=80)
        self.txt_phone = Entry(self.bodyframe, width=30, bd=2)
        self.txt_phone.place(x= 200,y=80)

        # Save Button
        savebutton = Button(self.bodyframe, text='Save now', command=self.savemember)
        savebutton.place(x=270, y=200)

    def savemember(self):
        """
            Adds member to the library and updates DB
        """
        membername = self.txt_member_name.get()
        phone = self.txt_phone.get()

        if(membername != '' and phone != ''):
            try:
                query = "INSERT INTO member(name, phone)VALUES(?,?)"
                cur.execute(query,(membername,phone))
                con.commit()
                messagebox.showinfo('Success','Member is created!',icon='info')
            except:
                messagebox.showerror('Error','Transaction failed!',icon='warning')
        
        else:
            messagebox.showerror('Error','All fields are required!',icon='warning')