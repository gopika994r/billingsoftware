#==================imports===================
import sqlite3
import re
import random
import string
import inflect
import locale
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
from datetime import date
from tkinter import scrolledtext as tkst
#============================================



root = Tk()

root.geometry("1366x768")
root.title("Retail Manager")


user = StringVar()
passwd = StringVar()
fname = StringVar()
lname = StringVar()
new_user = StringVar()
new_passwd = StringVar()


cust_name = StringVar()
cust_num = StringVar()
cust_new_bill = StringVar()
cust_search_bill = StringVar()
bill_date = StringVar()



with sqlite3.connect("./Database/store.db") as db:
    cur = db.cursor()

def random_bill_number(stringLength):
    lettersAndDigits = string.ascii_letters.upper() + string.digits
    strr=''.join(random.choice(lettersAndDigits) for i in range(stringLength-2))
    return ('BB'+strr)


def valid_phone(phn):
    if re.match(r"[789]\d{9}$", phn):
        return True
    return False

def login(Event=None):
    global username
    username = user.get()
    password = passwd.get()

    with sqlite3.connect("./Database/store.db") as db:
        cur = db.cursor()
    find_user = "SELECT * FROM employee WHERE emp_id = ? and password = ?"
    cur.execute(find_user, [username, password])
    results = cur.fetchall()
    if results:
        messagebox.showinfo("Login Page", "The login is successful")
        page1.entry1.delete(0, END)
        page1.entry2.delete(0, END)
        root.withdraw()
        global biller
        global page2
        biller = Toplevel()
        page2 = bill_window(biller)
        page2.time()
        biller.protocol("WM_DELETE_WINDOW", exitt)
        biller.mainloop()

    else:
        messagebox.showerror("Error", "Incorrect username or password.")
        page1.entry2.delete(0, END)




def logout():
    sure = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=biller)
    if sure == True:
        biller.destroy()
        root.deiconify()
        page1.entry1.delete(0, END)
        page1.entry2.delete(0, END)

class login_page:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Retail Manager")
        

        self.label1 = Label(root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/employee_login.png")
        self.label1.configure(image=self.img)

        self.entry1 = Entry(root)
        self.entry1.place(relx=0.373, rely=0.273, width=374, height=24)
        self.entry1.configure(font="-family {Poppins} -size 10")
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=user)

        self.entry2 = Entry(root)
        self.entry2.place(relx=0.373, rely=0.384, width=374, height=24)
        self.entry2.configure(font="-family {Poppins} -size 10")
        self.entry2.configure(relief="flat")
        self.entry2.configure(show="*")
        self.entry2.configure(textvariable=passwd)

        self.button1 = Button(root)
        self.button1.place(relx=0.366, rely=0.685, width=356, height=43)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#D2463E")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#D2463E")
        self.button1.configure(font="-family {Poppins SemiBold} -size 20")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""LOGIN""")
        self.button1.configure(command=login)




class Item:
    def __init__(self, name, price, qty):
        self.product_name = name
        self.price = price
        self.qty = qty

class Cart:
    def __init__(self):
        self.items = []
        self.dictionary = {}

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self):
        self.items.pop()

    def remove_items(self):
        self.items.clear()

    def total(self):
        total = 0.0
        for i in self.items:
            total += i.price * i.qty
        return total

    def isEmpty(self):
        if len(self.items)==0:
            return True
        
    def allCart(self):
        for i in self.items:
            if (i.product_name in self.dictionary):
                self.dictionary[i.product_name] += i.qty
            else:
                self.dictionary.update({i.product_name:i.qty})
    

def exitt():
    sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=biller)
    if sure == True:
        biller.destroy()
        root.destroy()

class bill_window:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Billing System")


        self.headinglabel=Label(biller,text='Billing System',font=('-family {poppins} -size 20'),bg='white',fg='black')
        self.headinglabel.pack(fill=X,pady=10)

        self.button1 = Button(self.headinglabel)
        self.button1.place(relx=0.031, rely=0.104, width=76, height=23)
        self.button1.configure(foreground="black")
        self.button1.configure(background="alice blue")
        self.button1.configure(font="-family {Poppins} -size 10")
        self.button1.configure(text="Logout")
        self.button1.configure(command=logout)

        self.clock = Label(self.headinglabel)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.customer_details_frame=LabelFrame(biller,text='Customer Details',font=('-family {poppins} -size 10'),fg='black',bg='white')
        self.customer_details_frame.pack(fill=X,padx=10)

        self.billlabel=Label(self.customer_details_frame,text='Bill Number',font=('-family {poppins} -size 10'),bg='white',fg='black')
        self.billlabel.grid(row=0,column=0,padx=20,pady=2)

        self.billEntry=Entry(self.customer_details_frame,font=('-family {poppins} -size 10'),width=28,textvariable=cust_search_bill)
        self.billEntry.grid(row=0,column=1,padx=8)

        self.searchButton=Button(self.customer_details_frame,text='Search',font=('-family {poppins} -size 10'),bg='alice blue',fg='black',command=self.search_bill)
        self.searchButton.grid(row=0,column=2,padx=30,pady=8)


        self.customernamelabel=Label(self.customer_details_frame,text='Customer Name',font=('-family {poppins} -size 10'),bg='white',fg='black')
        self.customernamelabel.grid(row=0,column=3,padx=20,pady=2)

        self.customernameEntry=Entry(self.customer_details_frame,font=('-family {poppins} -size 10'),width=28,textvariable=cust_name)
        self.customernameEntry.grid(row=0,column=4,padx=8)

        self.contactnumberlabel=Label(self.customer_details_frame,text='Contact Number',font=('-family {poppins} -size 10'),bg='white',fg='black')
        self.contactnumberlabel.grid(row=0,column=5,padx=20,pady=2)


        self.contactnumberEntry=Entry(self.customer_details_frame,font=('-family {poppins} -size 10'),width=28,textvariable=cust_num)
        self.contactnumberEntry.grid(row=0,column=6,padx=8)

        self.productsFrame=Frame(biller)
        self.productsFrame.pack()

        self.productlabel=LabelFrame(self.productsFrame,text='Products',font=('-family {poppins} -size 10'),bg='white',fg='black')
        self.productlabel.grid(row=0,column=0,pady=10,sticky='w',ipadx=25)

        self.categorylabel=Label(self.productlabel,text='Select Category',font=('-family {poppins} -size 10'),bg='white',fg='black')
        self.categorylabel.grid(row=0,column=0,padx=10,pady=15,sticky='w')

        

        self.subcategorylabel=Label(self.productlabel,text='Sub Category',font=('-family {poppins} -size 10'),bg='white',fg='black')
        self.subcategorylabel.grid(row=2,column=0,padx=10,pady=15,sticky='w')

        

        self.productslabel=Label(self.productlabel,text='Product',font=('-family {poppins} -size 10'),bg='white',fg='black')
        self.productslabel.grid(row=4,column=0,padx=10,pady=15,sticky='w')

        

        self.Quantitylabel=Label(self.productlabel,text='Quantity',font=('-family {poppins} -size 10'),bg='white',fg='black')
        self.Quantitylabel.grid(row=6,column=0,padx=10,pady=15,sticky='w')

        self.QuantityEntry=Entry(self.productlabel,font=('-family {poppins} -size 10'),width=8)
        self.QuantityEntry.grid(row=7,column=0,padx=10,pady=15)


        self.addcartButton=Button(self.productlabel,text='Add to Cart',font=('-family {poppins} -size 10'),bg='alice blue',fg='black',command=self.add_to_cart)
        self.addcartButton.grid(row=9,column=0,padx=10,pady=40)

        self.removeButton=Button(self.productlabel,text='Remove',font=('-family {poppins} -size 10'),bg='alice blue',fg='black',command=self.remove_product)
        self.removeButton.grid(row=9,column=1,padx=30,pady=40)

        self.clearButton=Button(self.productlabel,text='Clear',font=('-family {poppins} -size 10'),bg='alice blue',fg='black',command=self.clear_selection)
        self.clearButton.grid(row=9,column=2,padx=30,pady=40)

        self.billoptionlabel=LabelFrame(self.productsFrame,text='Bill options',font=('-family {poppins} -size 10'),bg='white',fg='black')
        self.billoptionlabel.grid(row=1,column=0,pady=10,padx=2,ipadx=100)

        self.TotalButton=Button(self.billoptionlabel,text='Total',font=('-family {poppins} -size 10'),bg='alice blue',fg='black',command=self.total_bill)
        self.TotalButton.grid(row=0,column=1,padx=30,pady=40)

        self.GenerateButton=Button(self.billoptionlabel,text='Generate',font=('-family {poppins} -size 10'),bg='alice blue',fg='black',command=self.gen_bill)
        self.GenerateButton.grid(row=0,column=2,padx=20,pady=40)

        self.ClearButton=Button(self.billoptionlabel,text='Clear',font=('-family {poppins} -size 10'),bg='alice blue',fg='black',command=self.clear_bill)
        self.ClearButton.grid(row=0,column=3,padx=30,pady=40)


        self.ExitButton=Button(self.billoptionlabel,text='Exit',font=('-family {poppins} -size 10'),bg='alice blue',fg='black',command=exitt)
        self.ExitButton.grid(row=0,column=4,padx=20,pady=40)

        

        self.billframe=Frame(self.productsFrame,relief=GROOVE,bd=3)
        self.billframe.grid(row=0,column=1,rowspan=3,padx=10)

        self.billwindowlabel=Label(self.billframe,text='Bill Window',font=('-family {poppins} -size 10'),bg='white',fg='black')
        self.billwindowlabel.pack(fill=X)

        self.scrollbar=Scrollbar(self.billframe,orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        
        self.textarea=Text(self.billframe,height=30,width=80)
        self.textarea.pack()

        self.textarea.delete(1.0, END)
        self.textarea.insert(END, "\t\t\t IPCS")
        self.textarea.insert(END, "\n\t\t\t NEW BUS STAND ")
        self.textarea.insert(END, "\n\t\t\t SALEM-636004")
        self.textarea.insert(END, "\n\t\t\t HELPLINE: 1800-200-255")
        self.textarea.insert(END, "\n\t\t\t GSTIN: 35AABCS1429B1ZX (w.e.f 01.07.2017)")
        self.textarea.insert(END, '\n\n Customer Name :\t\t\t\t\t\t Ph Number:')
        self.textarea.insert(END, '\n Bill Number:\t\t\t\t\t\t Date:')
        self.textarea.insert(END, "\n\n--------------------------------------------------------------------------------")
        self.textarea.insert(END, '\n Product\t\t\t\t Quantity(QTY)\t\t\t\t Price')
        self.textarea.insert(END, "\n--------------------------------------------------------------------------------")

        
        self.combo1 = ttk.Combobox(self.productlabel)
        self.combo1.grid(row=1,column=0,padx=10)

        find_category = "SELECT product_cat FROM raw_inventory"
        cur.execute(find_category)
        result1 = cur.fetchall()
        cat = []
        for i in range(len(result1)):
            if(result1[i][0] not in cat):
                cat.append(result1[i][0])

        self.combo1.configure(values=cat)
        self.combo1.configure(width=50)
        self.combo1.configure(state="readonly")
        self.combo1.configure(font="-family {Poppins} -size 8")
        self.combo1.option_add("*TCombobox*Listbox.font", "text_font")
        self.combo1.option_add("*TCombobox*Listbox.selectBackground", "#D2463E")
        
        self.combo1.bind("<<ComboboxSelected>>", self.get_category)

        self.combo2 = ttk.Combobox(self.productlabel)
        self.combo2.grid(row=3,column=0,ipadx=10)
        self.combo2.configure(font="-family {Poppins} -size 8")
        
        self.combo2.option_add("*TCombobox*Listbox.font", "text_font") 
        self.combo2.configure(state="disabled")

        self.combo3 = ttk.Combobox(self.productlabel)
        self.combo3.grid(row=5,column=0,padx=10)
        self.combo3.configure(state="disabled")
        self.combo3.configure(font="-family {Poppins} -size 8")
        self.combo3.option_add("*TCombobox*Listbox.font", "text_font")
    
   

    def get_category(self, Event):
        self.combo2.configure(state="readonly")
        self.combo2.set('')
        self.combo3.set('')
        find_subcat = "SELECT product_subcat FROM raw_inventory WHERE product_cat = ?"
        cur.execute(find_subcat, [self.combo1.get()])
        result2 = cur.fetchall()
        subcat = []
        for j in range(len(result2)):
            if(result2[j][0] not in subcat):
                subcat.append(result2[j][0])
        
        self.combo2.configure(values=subcat)
        self.combo2.bind("<<ComboboxSelected>>", self.get_subcat)
        self.combo3.configure(state="disabled")

    def get_subcat(self, Event):
        self.combo3.configure(state="readonly")
        self.combo3.set('')
        find_product = "SELECT product_name FROM raw_inventory WHERE product_cat = ? and product_subcat = ?"
        cur.execute(find_product, [self.combo1.get(), self.combo2.get()])
        result3 = cur.fetchall()
        pro = []
        for k in range(len(result3)):
            pro.append(result3[k][0])

        self.combo3.configure(values=pro)
        self.combo3.bind("<<ComboboxSelected>>", self.show_qty)
        self.QuantityEntry.configure(state="disabled")

    def show_qty(self, Event):
        self.QuantityEntry.configure(state="normal")
        self.qty_label = Label(self.productlabel)
        self.qty_label.grid(row=8,column=0)
        self.qty_label.configure(font="-family {Poppins} -size 8")
        self.qty_label.configure(anchor="w")

        product_name = self.combo3.get()
        find_qty = "SELECT stock FROM raw_inventory WHERE product_name = ?"
        cur.execute(find_qty, [product_name])
        results = cur.fetchone()
        self.qty_label.configure(text="In Stock: {}".format(results[0]))
        self.qty_label.configure(background="#ffffff")
        self.qty_label.configure(foreground="#333333")

      
    

    

    cart = Cart()
    def add_to_cart(self):
        self.textarea.configure(state="normal")
        strr = self.textarea.get('1.0', END)
        if strr.find('Total')==-1:
            product_name = self.combo3.get()
            if(product_name!=""):
                product_qty = self.QuantityEntry.get()
                find_mrp = "SELECT mrp, stock FROM raw_inventory WHERE product_name = ?"
                cur.execute(find_mrp, [product_name])
                results = cur.fetchall()
                stock = results[0][1]
                mrp = results[0][0]
                if product_qty.isdigit()==True:
                    if (stock-int(product_qty))>=0:
                        sp = mrp*int(product_qty)
                        item = Item(product_name, mrp, int(product_qty))
                        self.cart.add_item(item)
                        self.textarea.configure(state="normal")
                        bill_text = "\n{}\t\t\t\t {}\t\t\t\t   {}\n".format(product_name, product_qty, sp)
                        self.textarea.insert('insert', bill_text)
                        self.textarea.configure(state="disabled")
                    else:
                        messagebox.showerror("Oops!", "Out of stock. Check quantity.", parent=biller)
                else:
                    messagebox.showerror("Oops!", "Invalid quantity.", parent=biller)
            else:
                messagebox.showerror("Oops!", "Choose a product.", parent=biller)
        else:
            self.textarea.delete('1.0', END)
            new_li = []
            li = strr.split("\n")
            for i in range(len(li)):
                if len(li[i])!=0:
                    if li[i].find('Total')==-1:
                        new_li.append(li[i])
                    else:
                        break
            for j in range(len(new_li)-1):
                self.textarea.insert('insert', new_li[j])
                self.textarea.insert('insert','\n')
            product_name = self.combo3.get()
            if(product_name!=""):
                product_qty = self.QuantityEntry.get()
                find_mrp = "SELECT mrp, stock, product_id FROM raw_inventory WHERE product_name = ?"
                cur.execute(find_mrp, [product_name])
                results = cur.fetchall()
                stock = results[0][1]
                mrp = results[0][0]
                if product_qty.isdigit()==True:
                    if (stock-int(product_qty))>=0:
                        sp = results[0][0]*int(product_qty)
                        item = Item(product_name, mrp, int(product_qty))
                        self.cart.add_item(item)
                        self.textarea.configure(state="normal")
                        bill_text = "{}\t\t\t\t\t\t{}\t\t\t\t\t   {}\n".format(product_name, product_qty, sp)
                        self.textarea.insert('insert', bill_text)
                        self.textarea.configure(state="disabled")
                    else:
                        messagebox.showerror("Oops!", "Out of stock. Check quantity.", parent=biller)
                else:
                    messagebox.showerror("Oops!", "Invalid quantity.", parent=biller)
            else:
                messagebox.showerror("Oops!", "Choose a product.", parent=biller)

    def remove_product(self):
        if(self.cart.isEmpty()!=True):
            self.textarea.configure(state="normal")
            strr = self.textarea.get('1.0', END)
            if strr.find('Total')==-1:
                try:
                    self.cart.remove_item()
                except IndexError:
                    messagebox.showerror("Oops!", "Cart is empty", parent=biller)
                else:
                    self.textarea.configure(state="normal")
                    get_all_bill = (self.textarea.get('1.0', END).split("\n"))
                    new_string = get_all_bill[:len(get_all_bill)-3]
                    self.textarea.delete('1.0', END)
                    for i in range(len(new_string)):
                        self.textarea.insert('insert', new_string[i])
                        self.textarea.insert('insert','\n')
                    
                    self.textarea.configure(state="disabled")
            else:
                try:
                    self.cart.remove_item()
                except IndexError:
                    messagebox.showerror("Oops!", "Cart is empty", parent=biller)
                else:
                    self.textarea.delete('1.0', END)
                    new_li = []
                    li = strr.split("\n")
                    for i in range(len(li)):
                        if len(li[i])!=0:
                            if li[i].find('Total')==-1:
                                new_li.append(li[i])
                            else:
                                break
                    new_li.pop()
                    for j in range(len(new_li)-1):
                        self.textarea.insert('insert', new_li[j])
                        self.textarea.insert('insert','\n')
                    self.textarea.configure(state="disabled")

        else:
            messagebox.showerror("Oops!", "Add a product.", parent=biller)

    def wel_bill(self):
        self.name_message = Text(biller)
        self.name_message.place(relx=0.585, rely=0.394, width=176, height=30)
        self.name_message.configure(font="-family {poppins} -size 10")
        self.name_message.configure(borderwidth=0)
        self.name_message.configure(background="#ffffff")

        self.num_message = Text(biller)
        self.num_message.place(relx=0.842, rely=0.394, width=90, height=30)
        self.num_message.configure(font="-family {poppins} -size 10")
        self.num_message.configure(borderwidth=0)
        self.num_message.configure(background="#ffffff")

        self.bill_message = Text(biller)
        self.bill_message.place(relx=0.568, rely=0.417, width=176, height=26)
        self.bill_message.configure(font="-family {poppins} -size 10")
        self.bill_message.configure(borderwidth=0)
        self.bill_message.configure(background="#ffffff")

        self.bill_date_message = Text(biller)
        self.bill_date_message.place(relx=0.812, rely=0.417, width=90, height=26)
        self.bill_date_message.configure(font="-family {poppins} -size 10")
        self.bill_date_message.configure(borderwidth=0)
        self.bill_date_message.configure(background="#ffffff")
    
    def total_bill(self):
        if self.cart.isEmpty():
            messagebox.showerror("Oops!", "Add a product.", parent=biller)
        else:
            self.textarea.configure(state="normal")
            strr = self.textarea.get('1.0', END)
            if strr.find('Total')==-1:
                self.textarea.configure(state="normal")
                divider = "\n\n\n"+("-"*80)
                self.textarea.insert('insert', divider)
                subtotal = self.cart.total()
                cgst_rate = 9/100
                cgst_amount = subtotal * cgst_rate
                sgst_amount = cgst_amount
                a= subtotal + cgst_amount + sgst_amount
                total =round(a)
                p = inflect.engine()
                total_text = p.number_to_words(total).replace('-', ' ')
                subtotal = "\n\t\t\t\t\t\tSub Total     : Rs. {: .2f}".format(subtotal)
                self.textarea.insert('insert', subtotal)
                cgst = "\n\t\t\t\t\t        CGST (9%)     : Rs. {: .2f}".format(cgst_amount)
                self.textarea.insert('insert',cgst)
                sgst = "\n\t\t\t\t\t        SGST (9%)     : Rs. {: .2f}".format(sgst_amount)
                self.textarea.insert('insert',sgst)
                divider2 = "\n"+("-"*80)
                self.textarea.insert('insert', divider2)
                Total = "\n\t\t\t\t\t   Total Amount    : Rs. {: .2f}".format(total)
                self.textarea.insert('insert',Total)
                total_text = "\n\nTotal Amount (in words) : {} rupees only.".format(total_text.title())
                
                self.textarea.insert('insert', total_text)
                self.textarea.configure(state="disabled")
            else:
                return
            
    
         
            

    state = 1
    def gen_bill(self):

        if self.state == 1:
            strr = self.textarea.get('1.0', END)
            self.wel_bill()
            if(cust_name.get()==""):
                messagebox.showerror("Oops!", "Please enter a name.", parent=biller)
            elif(cust_num.get()==""):
                messagebox.showerror("Oops!", "Please enter a number.", parent=biller)
            elif valid_phone(cust_num.get())==False:
                messagebox.showerror("Oops!", "Please enter a valid number.", parent=biller)
            elif(self.cart.isEmpty()):
                messagebox.showerror("Oops!", "Cart is empty.", parent=biller)
            else: 
                if strr.find('Total')==-1:
                    self.total_bill()
                    self.gen_bill()
                else:
                    self.name_message.insert(END, cust_name.get())
                    self.name_message.configure(state="disabled")
            
                    self.num_message.insert(END, cust_num.get())
                    self.num_message.configure(state="disabled")
            
                    cust_new_bill.set(random_bill_number(8))

                    self.bill_message.insert(END, cust_new_bill.get())
                    self.bill_message.configure(state="disabled")
                
                    bill_date.set(str(date.today()))

                    self.bill_date_message.insert(END, bill_date.get())
                    self.bill_date_message.configure(state="disabled")

                    

                    with sqlite3.connect("./Database/store.db") as db:
                        cur = db.cursor()
                    insert = (
                        "INSERT INTO bill(bill_no, date, customer_name, customer_no, bill_details) VALUES(?,?,?,?,?)"
                    )
                    cur.execute(insert, [cust_new_bill.get(), bill_date.get(), cust_name.get(), cust_num.get(), self.textarea.get('1.0', END)])
                    db.commit()
                    #print(self.cart.items)
                    print(self.cart.allCart())
                    for name, qty in self.cart.dictionary.items():
                        update_qty = "UPDATE raw_inventory SET stock = stock - ? WHERE product_name = ?"
                        cur.execute(update_qty, [qty, name])
                        db.commit()
                    messagebox.showinfo("Success!!", "Bill Generated", parent=biller)
                    self.billEntry.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.customernameEntry.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.state = 0
        else:
            return
        
                    
    def clear_bill(self):
        self.wel_bill()
        self.billEntry.configure(state="normal")
        self.customernameEntry.configure(state="normal")
        self.billEntry.delete(0, END)
        self.customernameEntry.delete(0, END)
        self.contactnumberEntry.delete(0, END)
        self.name_message.configure(state="normal")
        self.num_message.configure(state="normal")
        self.bill_message.configure(state="normal")
        self.bill_date_message.configure(state="normal")
        self.textarea.configure(state="normal")
        self.name_message.delete(1.0, END)
        self.num_message.delete(1.0, END)
        self.bill_message.delete(1.0, END)
        self.bill_date_message.delete(1.0, END)
        self.textarea.delete(1.0, END)
        self.name_message.configure(state="disabled")
        self.num_message.configure(state="disabled")
        self.bill_message.configure(state="disabled")
        self.bill_date_message.configure(state="disabled")
        self.textarea.configure(state="disabled")
        self.cart.remove_items()
        self.state = 1

    def clear_selection(self):
        self.QuantityEntry.delete(0, END)
        self.combo1.configure(state="normal")
        self.combo2.configure(state="normal")
        self.combo3.configure(state="normal")
        self.combo1.delete(0, END)
        self.combo2.delete(0, END)
        self.combo3.delete(0, END)
        self.combo2.configure(state="disabled")
        self.combo3.configure(state="disabled")
        self.QuantityEntry.configure(state="disabled")
        try:
            self.qty_label.configure(foreground="#ffffff")
        except AttributeError:
            pass
             
    def search_bill(self):
        find_bill = "SELECT * FROM bill WHERE bill_no = ?"
        cur.execute(find_bill, [cust_search_bill.get().rstrip()])
        results = cur.fetchall()
        if results:
            self.clear_bill()
            self.wel_bill()
            self.name_message.insert(END, results[0][2])
            self.name_message.configure(state="disabled")
    
            self.num_message.insert(END, results[0][3])
            self.num_message.configure(state="disabled")
    
            self.bill_message.insert(END, results[0][0])
            self.bill_message.configure(state="disabled")

            self.bill_date_message.insert(END, results[0][1])
            self.bill_date_message.configure(state="disabled")

            self.textarea.configure(state="normal")
            self.textarea.insert(END, results[0][4])
            self.textarea.configure(state="disabled")

            self.billEntry.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
            self.customernameEntry.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")

            self.state = 0

        else:
            messagebox.showerror("Error!!", "Bill not found.", parent=biller)
            self.contactnumberEntry.delete(0, END)
            
    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

   




page1 = login_page(root)
root.bind("<Return>", login)
root.mainloop()








