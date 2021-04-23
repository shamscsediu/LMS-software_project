import importlib
from tkinter import *
from tkinter import ttk
import sqlite3

bookwindow = importlib.import_module('books')
memberwindow = importlib.import_module('members')
issuebookwindow = importlib.import_module('issuebook')
con = sqlite3.connect('LMS.db')
cur = con.cursor()

class System:
    def __init__(self,master):
        self.master = master
    
        def showsummary(self):
            """
                get queryset from the DB and show the details of
                books not issued, members count and books issued
                on the summary panel

            """

            book_instock_counter = cur.execute("SELECT COUNT(book_id) FROM books WHERE book_status").fetchall()
            member_counter = cur.execute("SELECT COUNT(member_id) FROM member").fetchall()
            issued_counter = cur.execute("SELECT COUNT(book_id) FROM books WHERE book_status=1").fetchall()
            self.lbl_book_count.config(text="IN STOCK: "+str(book_instock_counter[0][0]))
            self.lbl_member_counter.config(text="MEMBERS: "+str(member_counter[0][0]))
            self.lbl_taken_count.config(text="ISSUED: "+str(issued_counter[0][0]))

        def showbooks(self):
            """
                For displaying all books of the library to the user
            """

            counter = 0
            books = cur.execute("SELECT * FROM books").fetchall()
            for book in books:
                self.management_box.insert(counter,str(book[0])+'-'+book[1])
                counter+= 1

            def bookinfo(evt):
                """
                    Displaying the book information to the user 
                    for the selected book
                """

                value = str(self.management_box.get(self.management_box.curselection()))
                id = value.split('-')[0]
                self.list_details.delete(0,'end')

                book = cur.execute("SELECT * FROM books WHERE book_id=?",(id))
                book_info = book.fetchall()
                self.list_details.insert(0, 'Book Name:'+book_info[0][1])
                self.list_details.insert(1, 'Author:'+book_info[0][2])
                self.list_details.insert(2, 'Pages:'+str(book_info[0][3]))

                if book_info[0][4] == 0:
                    self.list_details.insert(3,'Status: In Stock')
                else:
                    self.list_details.insert(3,'Status: Not in stock')

            self.management_box.bind('<<ListboxSelect>>',bookinfo)

        # Main Frame
        main_frame = Frame(self.master)
        main_frame.pack()

        # Top Frame
        top_frame = Frame(main_frame, width= 900, height= 70, borderwidth = 2,relief= SUNKEN, padx= 20)
        top_frame.pack(side= TOP, fill= X)

        self.btn_add_member = Button(top_frame, text="Add New Member", font="arial 12 bold",padx=10,command=self.new_member)
        self.btn_add_member.pack(side=LEFT)

        self.btn_add_book = Button(top_frame, text="Add New Book", font="arial 12 bold",padx=10,command=self.new_book)
        self.btn_add_book.pack(side=LEFT)

        self.btn_issue_book = Button(top_frame, text="Issue Book", font="arial 12 bold",padx=10, command = self.issue_book)
        self.btn_issue_book.pack(side=LEFT)


        # Centre Frame
        centre_frame = Frame(main_frame, width = 900, height= 800, relief = RIDGE)
        centre_frame.pack(side= TOP)

        # Left Frame
        left_frame = Frame(centre_frame, width=600, height=700, relief=SUNKEN, borderwidth=2)
        left_frame.pack(side = LEFT)

        self.leftab = ttk.Notebook(left_frame, width=600, height=600)
        self.leftab.pack()

        self.tab1 = ttk.Frame(self.leftab)
        self.tab2 = ttk.Frame(self.leftab)
        self.leftab.add(self.tab1, text = 'Management')
        self.leftab.add(self.tab2, text = 'Summary')

        # List Box (in left frame)
        # Management
        self.management_box = Listbox(self.tab1, width=40, height=30, font='times 12 bold')
        self.scroll = Scrollbar(self.tab1, orient=VERTICAL)
        self.management_box.grid(row=0,column=0,padx=(10,0), pady=10, sticky=N)
        self.scroll.config(command=self.management_box.yview)
        self.management_box.config(yscrollcommand = self.scroll.set)
        self.scroll.grid(row = 0,column=0, sticky= N+S+E)

        self.list_details = Listbox(self.tab1, width=80,height = 30, font= 'times 12 bold')
        self.list_details.grid(row=0, column=1, padx=(10,0), pady=10, sticky=N)

        #summary
        self.lbl_book_count = Label(self.tab2, text='', pady=20, font='verdana 14 bold')
        self.lbl_book_count.grid(row=0)
        self.lbl_member_counter = Label(self.tab2, text='', pady=20, font='verdana 14 bold')
        self.lbl_member_counter.grid(row=1,sticky=W)
        self.lbl_taken_count = Label(self.tab2, text='', pady=20, font='verdana 14 bold')
        self.lbl_taken_count.grid(row=2,sticky=W)

        # Right Frame
        right_frame = Frame(centre_frame, width=300, height=700, relief=SUNKEN, borderwidth=2)
        right_frame.pack()
       
        searchbar = LabelFrame(right_frame, width=250, height=75, text="Search")
        searchbar.pack()
        #'''
        # Search Bar (In Right Frame)
        self.label_search = Label(searchbar, text='Search Book', font='arial 12 bold')
        self.label_search.grid(row=0,column=0,padx=20,pady=10)

        self.ent_search = Entry(searchbar, width=30,bd=10)
        self.ent_search.grid(row=0, column=1 ,columnspan=3, padx=10, pady=10)
        self.btn_search = Button(searchbar,text='Search Now', font='arial 12', command=self.search)
        self.btn_search.grid(row=0,column=4,padx=20,pady=10)

        # List Box (In Right Frame)
        list_bar = LabelFrame(right_frame, width=280, height=200, text='Books List', bg="#fff")
        list_bar.pack(fill = BOTH)
        list_label = Label(list_bar, text="Sort by:",font="times 16")
        list_label.grid(row=0, column=2)

        self.list_choice = IntVar()

        # Radio Buttons
        
        rbtn_all_books = Radiobutton(list_bar, text='Sort all books', var=self.list_choice,value=1)
        rbtn_all_books.grid(row=1,column=0)
        rbtn_instock = Radiobutton(list_bar, text='Books available', var=self.list_choice,value=2)
        rbtn_instock.grid(row=1,column=1)
        rbtn_issued_books = Radiobutton(list_bar, text='Books issued', var=self.list_choice,value=3)
        rbtn_issued_books.grid(row=1,column=2)

        btn_show_books = Button(list_bar, text='Show books', font='arial 12 bold',command = self.searchsort)
        btn_show_books.grid(row=1,column=3,padx=40,pady=10)

        welcome_image = Frame(right_frame, width=300, height=400)
        welcome_image.pack(fill=BOTH)
        self.welcome_main_image = PhotoImage(file='images/intro.png')
        self.image_label = Label(welcome_image, image=self.welcome_main_image)
        self.image_label.grid(row=1)

        showbooks(self)
        showsummary(self)

    def searchsort(self):
        """
            Sorting all the books on the basis of radio button
            selected by the user
        """
        value = self.list_choice.get()
        query = ''
        if value == 1:
            query = "SELECT * FROM books ORDER BY book_name"
        
        elif value == 2:
            query = "SELECT * FROM books WHERE book_status = 0"

        else:
            query = "SELECT * FROM books WHERE book_status = 1"

        self.management_box.delete(0,END)
        counter = 0
        searchquery = cur.execute(query).fetchall()
        for book in searchquery:
            self.management_box.insert(counter, str(book[0])+'-'+str(book[1]))
            counter += 1

    def issue_book(self):
        """
            Issues book to the member
        """
        add = issuebookwindow.IssueBook()

    def new_book(self):
        """
            For adding new book in the library
        """
        add = bookwindow.StoreBook()

    def new_member(self):
        """
            For adding new member in the library
        """
        add = memberwindow.StoreMember()

    def search(self):
        """
            For searching book in the Library
        """
        value = self.ent_search.get()
        searchquery = cur.execute("SELECT * FROM books WHERE book_name LIKE ?",('%'+value+'%',)).fetchall()
        self.management_box.delete(0,END)
        counter = 0
        for book in searchquery:
            self.management_box.insert(counter, str(book[0])+'-'+str(book[1]))
            counter += 1

def base():
    """
        It starts the main application and sets up all of its frames,
        buttons and all other attributes
    """

    base_window = Tk()
    app         = System(base_window)
    base_window.title("Library Management System")
    base_window.geometry("1300x900")     # "_fullscreen",True
    base_window.mainloop()

if __name__ == '__main__':
    base()