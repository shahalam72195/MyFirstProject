from tkinter import Tk,Label,Frame,Entry,Button,messagebox,simpledialog,filedialog
from tkinter.ttk import Combobox
import time
import datetime
from PIL import Image,ImageTk
import autotable_creation
import random
import sqlite3
import gmail
from tkintertable import TableCanvas, TableModel
import re
import shutil
import os

win=Tk()
win.title('Welcome To ABC Bank')
win.state('zoomed')
# win.resizable(width=False,height=False)
win.configure(bg='light gray')

header_title=Label(win,text="ABC Bank Of India",font=('Times New Roman',50),bg='light gray',fg='blue')
header_title.pack()

current_date=time.strftime('%d-%b-%Y')

def update_time():
    curr_date = datetime.datetime.now().strftime('%d-%b-%Y  %I:%M:%S %p')
    header_date.config(text=f'Today-{curr_date}')
    win.after(1000, update_time)

header_date=Label(win,font=('Times New Roman',20),bg='light gray',fg='blue')
header_date.pack(pady=10)

update_time()

img=Image.open('logo1.jpg').resize((150,120))
bitmap_img=ImageTk.PhotoImage(img,master=win)

logo_label=Label(win,image=bitmap_img)
logo_label.place(relx=0,rely=0)

def main_screen():
    frm=Frame(win)
    frm.configure(bg='white')
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.67)

    global cap
    cap=''
    def genrate_captcha():
        global cap
        d=str(random.randint(0,9))
        cap=cap+d
        ch=chr(random.randint(65,90))
        cap=cap+ch

        d=str(random.randint(0,9))
        cap=cap+d
        ch=chr(random.randint(97,122))
        cap=cap+ch

        d=str(random.randint(0,9))
        cap=cap+d
        ch=chr(random.randint(97,122))
        cap=cap+ch

        return cap
    
    def reset():
        acn_entry.delete(0,"end")
        pass_entry.delete(0,"end")
        captcha_entry.delete(0,"end")
        acn_entry.focus()

    def login_click():
        global uacn
        uacn=acn_entry.get()
        upass=pass_entry.get()
        urole=role_cb.get()


        if len(uacn)==0 or len(upass)==0:
            messagebox.showerror("login","Account or Password can't be empty")
            return
        if captcha_entry.get()!=cap:
            messagebox.showerror("login","Invalid captcha")
            return

        uacn=int(uacn)
        if uacn==0 and upass=='admin' and urole=='Admin':
            frm.destroy()
            welcome_admin_screen()
        elif urole=='User':
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select * from users where users_acno=? and users_pass=?',(uacn,upass))
            tup=cur_obj.fetchone()
            if tup==None:
                messagebox.showerror('login','Invalid ACN/Pass')
            else:
                global uname
                uname=tup[2]
                frm.destroy()
                welcome_user_screen()
        else:
            messagebox.showerror('login','Invalid Role')
    acn_label=Label(frm,font=('Times New Roman',20),bg='white',fg='black',text="Account No")
    acn_label.place(relx=.3,rely=.1)

    acn_entry=Entry(frm,font=('Times New Roman',20),bd=2)
    acn_entry.place(relx=.45,rely=.1)
    acn_entry.focus()

    pass_label=Label(frm,font=('Times New Roman',20),bg='white',fg='black',text="Password")
    pass_label.place(relx=.3,rely=.2)

    pass_entry=Entry(frm,font=('Times New Roman',20),bd=2,show='*')
    pass_entry.place(relx=.45,rely=.2)

    role_label=Label(frm,font=('Times New Roman',20),bg='white',fg='black',text="Role")
    role_label.place(relx=.3,rely=.3)

    role_cb=Combobox(frm,font=('Times New Roman',20),width=19,values=['User','Admin'])
    role_cb.current(1)
    role_cb.place(relx=.45,rely=.3)

    gen_captcha_label=Label(frm,font=('Times New Roman',20),width=7,bg='lightgreen',fg='green',text=genrate_captcha())
    gen_captcha_label.place(relx=.55,rely=.4)

    captcha_label=Label(frm,font=('Times New Roman',20),bg='white',fg='black',text="Captcha")
    captcha_label.place(relx=.3,rely=.5)

    captcha_entry=Entry(frm,font=('Times New Roman',20),bd=3)
    captcha_entry.place(relx=.45,rely=.5)


    login_btn=Button(frm,text='Login',font=('Times New Roman',20),bg='blue',fg='white',bd=3,height=1,command=login_click)
    login_btn.place(relx=.45,rely=.65)

    reset_btn=Button(frm,command=reset,text='Reset',font=('Times New Roman',20),height=1,bg='blue',fg='white',bd=3)
    reset_btn.place(relx=.58,rely=.65)

    forgot_pass_label=Label(frm,font=('Times New Roman',15,'underline'),bg='white',fg='blue',text='forgot password',cursor='hand2')
    forgot_pass_label.place(relx=.55,rely=.8)
    forgot_pass_label.bind('<Button-1>',lambda e:forgot_password_screen())


def welcome_admin_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='white')
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.67)

    def logout_click():
        resp=messagebox.askyesno('logout','Do you want to logout,Kindly confirm?')
        if resp:
            frm.destroy()
            main_screen()
   
    def create_click():
        ifrm=Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.7)

        def open_acn():
            uname=name_entry.get()
            umob=mob_entry.get()
            uemail=email_entry.get()
            uadhar=adhar_entry.get()
            ubal=0
            upass=str(random.randint(100000,999999))

            if len(uname)==0 or len(umob)==0 or len(uemail)==0 or len(uadhar)==0:
                messagebox.showerror('create','Empty fields are not allowed')
                return
            
            if not re.fullmatch('[a-zA-Z ]+',uname):
                messagebox.showerror('create','Kindly enter valid name')
                return

            if not re.fullmatch('[6-9][0-9]{9}',umob):
                messagebox.showerror('create','Kindly enter valid mob no')
                return
            
            if not re.fullmatch('[a-z0-9_.]+@[a-z]+[.][a-z]+',uemail):
                messagebox.showerror('create','Kindly enter valid email')
                return
            
            if not re.fullmatch('[0-9]{12}',uadhar):
                messagebox.showerror('create','Kindly enter valid adhar')
                return

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('insert into users(users_pass,users_name,users_mob,users_email,users_bal,users_adhar,users_opendate) values(?,?,?,?,?,?,?)',(upass,uname,umob,uemail,ubal,uadhar,current_date))
            con_obj.commit()
            con_obj.close()

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select max(users_acno) from users')
            tup=cur_obj.fetchone()
            uacn=tup[0]
            con_obj.close()

            try:
                gmail_con=gmail.GMail('shahalam72195@gmail.com','vpwa ymcz ufhr ihbb')
                umsg=f'''Hello,{uname}
                Welcome to ABC Bank
                Your ACN is: {uacn}
                Your Pass is: {upass}
                Kindly change your password when you login first time

                Thanks
                '''
                msg=gmail.Message(to=uemail,subject='Account Opened',text=umsg)
                gmail_con.send(msg)
                messagebox.showinfo('open acn','account created and kindly check your email for acn/pass')
            except:
                messagebox.showerror('open acn','something went wrong')

        title_ifrm=Label(ifrm,font=('Times New Roman',18),bg='white',text="This is create user screen",fg='black')
        title_ifrm.pack()

        name_label=Label(ifrm,font=('Times New Roman',15),bg='white',text="Name",fg='black')
        name_label.place(relx=.1,rely=.2)

        name_entry=Entry(ifrm,font=('Times New Roman',18),bd=3)
        name_entry.place(relx=.1,rely=.3)
        name_entry.focus()

        mob_label=Label(ifrm,font=('Times New Roman',15),bg='white',text="Mob",fg='black')
        mob_label.place(relx=.1,rely=.5)

        mob_entry=Entry(ifrm,font=('Times New Roman',18),bd=3)
        mob_entry.place(relx=.1,rely=.6)

        email_label=Label(ifrm,font=('Times New Roman',15),bg='white',text="Email",fg='black')
        email_label.place(relx=.6,rely=.2)

        email_entry=Entry(ifrm,font=('Times New Roman',18),bd=3)
        email_entry.place(relx=.6,rely=.3)

        adhar_label=Label(ifrm,font=('Times New Roman',15),bg='white',text="Adhar No",fg='black')
        adhar_label.place(relx=.6,rely=.5)

        adhar_entry=Entry(ifrm,font=('Times New Roman',18),bd=3)
        adhar_entry.place(relx=.6,rely=.6)

        open_btn=Button(ifrm,command=open_acn,text='Open',font=('Times New Roman',20),bg='blue',fg='white',bd=3)
        open_btn.place(relx=.3,rely=.8)

        reset_btn=Button(ifrm,text='Reset',font=('Times New Roman',20),bg='blue',fg='white',bd=3)
        reset_btn.place(relx=.6,rely=.8)


    def view_click():
        ifrm=Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.1,relwidth=.7,relheight=.7)

        title_ifrm=Label(ifrm,font=('Times New Roman',18),bg='white',text="This is view user screen",fg='black')
        title_ifrm.pack()

        # Create a Frame (Fix for NoneType error)
        frame = Frame(ifrm)
        frame.place(relx=.1,rely=.1,relwidth=.7)

        data={}
        i=1
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute("select * from users")

        for tup in cur_obj:
            data[f"{i}"]= {"Acno": tup[0], "Balance":tup[5], "Adhar": tup[6],"Opendate":tup[7],"Email":tup[4],"Mob":tup[3]}
            i+=1

        con_obj.close()
        # Create Table Model
        model = TableModel()
        model.importDict(data)  # Load data into the model

        # Create Table Canvas inside Frame (Important Fix)
        table = TableCanvas(frame, model=model, editable=True)
        table.show()

    
    def delete_click():
        ifrm=Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.7)

        title_ifrm=Label(ifrm,font=('Times New Roman',18),bg='white',text="This is delete user screen",fg='black')
        title_ifrm.pack()

        def reset_acn():
            acn_entry.delete(0,"end")

        def delete_db():
            uacn=acn_entry.get()
            if len(uacn)==0:
                messagebox.showerror('Warning','Please Enter Accont  Number')
            else:
                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('select * from users where users_acno=?',(uacn,))
                tup=cur_obj.fetchone()
                if tup==None:
                    messagebox.showerror('Delete','Invalid Account Number')            
                else:
                    con_obj=sqlite3.connect(database='bank.sqlite')
                    cur_obj=con_obj.cursor()
                    cur_obj.execute("delete from users where users_acno=?",(uacn,))
                    cur_obj.execute("delete from txn where txn_acno=?",(uacn,))
                    con_obj.commit()
                    con_obj.close()
                    messagebox.showinfo("delete",f"User with Acn {uacn} deleted")

        acn_label=Label(ifrm,font=('Times New Roman',15),bg='white',text="ACN",fg='blue')
        acn_label.place(relx=.3,rely=.3)

        acn_entry=Entry(ifrm,font=('Times New Roman',18),bd=2)
        acn_entry.place(relx=.3,rely=.4)
        acn_entry.focus()

        delete_btn=Button(ifrm,command=delete_db,text='delete',font=('Times New Roman',20),bg='blue',fg='white',bd=2)
        delete_btn.place(relx=.3,rely=.6)

        reset_btn=Button(ifrm,command=reset_acn,text='reset',font=('Times New Roman',20),bg='blue',fg='white',bd=2)
        reset_btn.place(relx=.5,rely=.6)

    wel_label=Label(frm,font=('Times New Roman',20),bg='white',text="Welcome,Admin",fg='blue')
    wel_label.place(relx=0,rely=0)

    logout_btn=Button(frm,command=logout_click,text='Logout',font=('Times New Roman',20),bg='blue',fg='white',bd=2)
    logout_btn.place(relx=.92,rely=0)

    create_btn=Button(frm,command=create_click,width=12,text='create user',font=('Times New Roman',20),bg='green',bd=2,fg='white')
    create_btn.place(relx=0,rely=.1)

    view_btn=Button(frm,command=view_click,width=12,text='view users',font=('Times New Roman',20),bg='blue',fg='white',bd=2)
    view_btn.place(relx=0,rely=.3)

    delete_btn=Button(frm,command=delete_click,width=12,text='delete user',font=('Times New Roman',20),bg='red',bd=2,fg='white')
    delete_btn.place(relx=0,rely=.5)



def forgot_password_screen():
    frm=Frame(win)
    frm.configure(bg='white')
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.67)

    def back_click():
        frm.destroy()
        main_screen()
   
    def get_password():
        uacn=acn_entry.get()
        umob=mob_entry.get()
        uemail=email_entry.get()

        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select users_name,users_pass from users where users_acno=? and users_email=? and users_mob=?',(uacn,uemail,umob))
        tup=cur_obj.fetchone()
        con_obj.close()

        if tup==None:
            messagebox.showerror('forgot pass','Invalid Details')
        else:
            try:
                print(111)
                gmail_con=gmail.GMail('shahalam72195@gmail.com','vpwa ymcz ufhr ihbb')
                print(222)
                umsg=f'''Hello,{tup[0]}
                Welcome to ABC Bank
                Your Pass is: {tup[1]}
               
                Thanks
                '''
                print(333)
                msg=gmail.Message(to=uemail,subject='Password Recovery',text=umsg)
                gmail_con.send(msg)
                print(444)
                messagebox.showinfo('forgot password','kindly check your email for pass')
            except Exception as e:
                messagebox.showerror('forgot password','something went wrong')
                print(e)


    back_btn=Button(frm,command=back_click,text='Back',font=('Times New Roman',20,),bg='blue',fg='white',bd=2)
    back_btn.place(relx=.01,rely=.01)

    acn_label=Label(frm,font=('Times New Roman',20),bg='white',text="ACN")
    acn_label.place(relx=.3,rely=.1)

    acn_entry=Entry(frm,font=('Times New Roman',20),bd=2)
    acn_entry.place(relx=.4,rely=.1)
    acn_entry.focus()

    email_label=Label(frm,font=('Times New Roman',20),bg='white',text="Email")
    email_label.place(relx=.3,rely=.2)

    email_entry=Entry(frm,font=('Times New Roman',20),bd=2)
    email_entry.place(relx=.4,rely=.2)

    mob_label=Label(frm,font=('Times New Roman',20),bg='white',text="Mob")
    mob_label.place(relx=.3,rely=.3)

    mob_entry=Entry(frm,font=('Times New Roman',20),bd=2)
    mob_entry.place(relx=.4,rely=.3)

    submit_btn=Button(frm,command=get_password,text='Submit',font=('Times New Roman',20),bg='blue',fg='white',bd=2)
    submit_btn.place(relx=.5,rely=.4)


def welcome_user_screen():
    frm=Frame(win)
    frm.configure(bg='white')
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.67)

    if os.path.exists(f"{uacn}.png"):
        img=ImageTk.PhotoImage(Image.open(f'{uacn}.png').resize((120,120)),master=win)
    else:
        img=ImageTk.PhotoImage(Image.open('default.png').resize((120,120)),master=win)
    pic_label=Label(frm,image=img)
    pic_label.image=img
    pic_label.place(relx=.01,rely=.05)

    def update_photo():
        path=filedialog.askopenfilename()
        shutil.copy(path,f"{uacn}.png")

        img=ImageTk.PhotoImage(Image.open(path).resize((120,120)),master=win)
        pic_label=Label(frm,image=img)
        pic_label.image=img
        pic_label.place(relx=.01,rely=.05)

    btn_update_pic=Button(frm,text="Update Photo",bg='blue',fg='white',command=update_photo)
    btn_update_pic.place(relx=.1,rely=.34)

    def logout_click():
        resp=messagebox.askyesno('logout','Do you want to logout,Kindly confirm?')
        if resp:
            frm.destroy()
            main_screen()
        

    def check_click():
        ifrm=Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.15,relwidth=.7,relheight=.75)

        title_ifrm=Label(ifrm,font=('Times New Roman',18),bg='white',text="This is check balance screen",fg='black')
        title_ifrm.pack()

        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select users_bal,users_opendate,users_adhar from users where users_acno=?',(uacn,))
        tup=cur_obj.fetchone()
        con_obj.close()

        lbl_bal=Label(ifrm,text=f'Available Balance:\t\t{tup[0]}',fg='blue',font=('Times New Roman',15),bg='white')
        lbl_bal.place(relx=.2,rely=.2)

        lbl_opendate=Label(ifrm,text=f'Account opendate:\t\t{tup[1]}',fg='blue',font=('Times New Roman',15),bg='white')
        lbl_opendate.place(relx=.2,rely=.4)

        lbl_adhar=Label(ifrm,text=f'User Adhar:\t\t{tup[2]}',fg='blue',font=('Times New Roman',15),bg='white')
        lbl_adhar.place(relx=.2,rely=.6)


    def update_click():
        ifrm=Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.15,relwidth=.7,relheight=.75)

        title_ifrm=Label(ifrm,font=('Times New Roman',18),bg='white',text="This is update screen",fg='black')
        title_ifrm.pack()


        def update_details():
            uname=name_entry.get()
            umob=mob_entry.get()
            uemail=email_entry.get()
            upass=pass_entry.get()

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('update users set users_name=?,users_pass=?,users_email=?,users_mob=? where users_acno=?',(uname,upass,uemail,umob,uacn))
            con_obj.commit()
            con_obj.close()
            messagebox.showinfo('update','details updated')


        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select * from users where users_acno=?',(uacn,))
        tup=cur_obj.fetchone()
        con_obj.close()


        name_label=Label(ifrm,font=('Times New Roman',15),bg='white',text="Name",fg='blue')
        name_label.place(relx=.1,rely=.2)

        name_entry=Entry(ifrm,font=('Times New Roman',18),bd=2)
        name_entry.place(relx=.1,rely=.27)
        name_entry.insert(0,tup[2])
        name_entry.focus()

        mob_label=Label(ifrm,font=('Times New Roman',15),bg='white',text="Mob",fg='blue')
        mob_label.place(relx=.1,rely=.4)

        mob_entry=Entry(ifrm,font=('Times New Roman',18),bd=2)
        mob_entry.place(relx=.1,rely=.47)
        mob_entry.insert(0,tup[3])

        email_label=Label(ifrm,font=('Times New Roman',15),bg='white',text="Email",fg='blue')
        email_label.place(relx=.6,rely=.2)

        email_entry=Entry(ifrm,font=('Times New Roman',18),bd=2)
        email_entry.place(relx=.6,rely=.27)
        email_entry.insert(0,tup[4])

        pass_label=Label(ifrm,font=('Times New Roman',15),bg='white',text="Pass",fg='blue')
        pass_label.place(relx=.6,rely=.4)

        pass_entry=Entry(ifrm,font=('Times New Roman',18),bd=2)
        pass_entry.place(relx=.6,rely=.47)
        pass_entry.insert(0,tup[1])

        update_btn=Button(ifrm,command=update_details,text='update',font=('Times New Roman',20),bg='blue',fg='white',bd=2)
        update_btn.place(relx=.45,rely=.7)


    def deposit_click():
        ifrm=Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.15,relwidth=.7,relheight=.75)

        title_ifrm=Label(ifrm,font=('Times New Roman',18),bg='white',text="This is deposit screen",fg='black')
        title_ifrm.pack()


        def deposit_db():
            uamt=float(amt_entry.get())

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_bal from users where users_acno=?',(uacn,))
            ubal=cur_obj.fetchone()[0]
            con_obj.close()


            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('update users set users_bal=users_bal+? where users_acno=?',(uamt,uacn))
            con_obj.commit()
            con_obj.close()

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(uacn,'Cr(+)',time.strftime('%d-%b-%Y %r'),uamt,ubal+uamt))
            con_obj.commit()
            con_obj.close()

            messagebox.showinfo("deposit",f"Amount {uamt} deposited and updated bal {ubal+uamt}")

        
        amt_label=Label(ifrm,font=('Times New Roman',20),bg='white',text="Amount",fg='blue')
        amt_label.place(relx=.25,rely=.3)

        amt_entry=Entry(ifrm,font=('Times New Roman',20),bd=2)
        amt_entry.place(relx=.4,rely=.3)

        deposit_btn=Button(ifrm,command=deposit_db,text='deposit',font=('Times New Roman',20),bg='blue',fg='white',bd=2)
        deposit_btn.place(relx=.6,rely=.5)

    def withdraw_click():
        ifrm=Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.15,relwidth=.7,relheight=.75)

        title_ifrm=Label(ifrm,font=('Times New Roman',18),bg='white',text="This is withdraw screen",fg='black')
        title_ifrm.pack()


        def withdraw_db():
            uamt=float(amt_entry.get())

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_bal from users where users_acno=?',(uacn,))
            ubal=cur_obj.fetchone()[0]
            con_obj.close()

            if ubal>=uamt:
                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('update users set users_bal=users_bal-? where users_acno=?',(uamt,uacn))
                con_obj.commit()
                con_obj.close()

                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(uacn,'Db(-)',time.strftime('%d-%b-%Y %r'),uamt,ubal-uamt))
                con_obj.commit()
                con_obj.close()

                messagebox.showinfo("withdraw",f"Amount {uamt} withdrawn and updated bal {ubal-uamt}")
            else:
                messagebox.showerror("withdraw",f"Insufficient Bal {ubal}")


        amt_label=Label(ifrm,font=('Times New Roman',20),bg='white',text="Amount",fg='blue')
        amt_label.place(relx=.25,rely=.3)

        amt_entry=Entry(ifrm,font=('Times New Roman',20),bd=2)
        amt_entry.place(relx=.4,rely=.3)

        withdraw_btn=Button(ifrm,command=withdraw_db,text='withdraw',font=('Times New Roman',20),bg='blue',fg='white',bd=2)
        withdraw_btn.place(relx=.6,rely=.5)


    def transfer_click():
        ifrm=Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.15,relwidth=.7,relheight=.75)

        title_ifrm=Label(ifrm,font=('Times New Roman',18),bg='white',text="This is transfer screen",fg='black')
        title_ifrm.pack()

        def transfer_db():
            uamt=float(amt_entry.get())
            toacn=int(to_entry.get())

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_bal,users_email from users where users_acno=?',(uacn,))
            tup=cur_obj.fetchone()
            ubal=tup[0]
            uemail=tup[1]
            con_obj.close()

            if ubal>=uamt:
                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute("select * from users where users_acno=?",(toacn,))
                tup=cur_obj.fetchone()
                con_obj.close()

                if tup==None:
                    messagebox.showerror("transfer","To ACN does not exist")
                else:
                    otp=random.randint(1000,9999)
                    try:
                        gmail_con=gmail.GMail('shahalam72195@gmail.com','vpwa ymcz ufhr ihbb')
                        umsg=f'''Hello,{uname}
                        Welcome to ABC Bank
                        Your OTP is: {otp}
                        
                        Kindly verify this otp to complete your txn

                        Thanks
                        '''
                        msg=gmail.Message(to=uemail,subject='Account Opened',text=umsg)
                        gmail_con.send(msg)
                        messagebox.showinfo('txn','we have send otp to your registered email')

                        uotp=simpledialog.askinteger("OTP","Enter OTP")
                        if otp==uotp:
                            con_obj=sqlite3.connect(database='bank.sqlite')
                            cur_obj=con_obj.cursor()
                            cur_obj.execute('update users set users_bal=users_bal-? where users_acno=?',(uamt,uacn))
                            cur_obj.execute('update users set users_bal=users_bal+? where users_acno=?',(uamt,toacn))
                            
                            con_obj.commit()
                            con_obj.close()

                            tobal=tup[5]

                            con_obj=sqlite3.connect(database='bank.sqlite')
                            cur_obj=con_obj.cursor()
                            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(uacn,'Db(-)',time.strftime('%d-%b-%Y %r'),uamt,ubal-uamt))
                            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(toacn,'Cr(+)',time.strftime('%d-%b-%Y %r'),uamt,ubal+uamt))
                            
                            con_obj.commit()
                            con_obj.close()

                            messagebox.showinfo("transfer",f"Amount {uamt} transfered and updated bal {ubal-uamt}")
                        else:
                            messagebox.showerror('otp','Invalid OTP')
                    except:
                        messagebox.showerror('txn','something went wrong')
            else:
                messagebox.showerror("transfer",f"Insufficient Bal {ubal}")



        to_label=Label(ifrm,font=('Times New Roman',20),bg='white',text="To ACN",fg='blue')
        to_label.place(relx=.25,rely=.3)

        to_entry=Entry(ifrm,font=('Times New Roman',20),bd=2)
        to_entry.place(relx=.4,rely=.3)

        amt_label=Label(ifrm,font=('Times New Roman',20),bg='white',text="Amount",fg='blue')
        amt_label.place(relx=.25,rely=.45)

        amt_entry=Entry(ifrm,font=('Times New Roman',20),bd=2)
        amt_entry.place(relx=.4,rely=.45)

        transfer_btn=Button(ifrm,command=transfer_db,text='transfer',font=('Times New Roman',20),bg='blue',fg=
        'white',bd=2)
        transfer_btn.place(relx=.6,rely=.65)


    def history_click():
        ifrm=Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.15,relwidth=.7,relheight=.75)

        title_ifrm=Label(ifrm,font=('Times New Roman',18),bg='white',text="This is history screen",fg='black')
        title_ifrm.pack()


        # Create a Frame (Fix for NoneType error)
        frame = Frame(ifrm)
        frame.place(relx=.1,rely=.1,relwidth=.7)

        data={}
        i=1
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute("select * from txn where txn_acno=?",(uacn,))

        for tup in cur_obj:
            data[f"{i}"]= {"Txn Id": tup[0], "Txn Amt":tup[4], "Txn Date": tup[3],"Txn Type":tup[2],"Updated Bal":tup[5]}
            i+=1

        con_obj.close()
        # Create Table Model
        model = TableModel()
        model.importDict(data)  # Load data into the model

        # Create Table Canvas inside Frame (Important Fix)
        table = TableCanvas(frame, model=model, editable=True)
        table.show()


    wel_label=Label(frm,font=('Times New Roman',20),bg='white',text=f"Welcome,{uname}",fg='blue')
    wel_label.place(relx=.01,rely=0)

    logout_btn=Button(frm,command=logout_click,text='logout',font=('Times New Roman',20),bg='blue',fg='white',bd=2)
    logout_btn.place(relx=.92,rely=0)

    check_btn=Button(frm,command=check_click,width=15,text='check balance',font=('Times New Roman',20),bg='purple',bd=2,fg='white')
    check_btn.place(relx=0,rely=.4)

    update_btn=Button(frm,command=update_click,width=15,text='update details',font=('Times New Roman',20),bg='blue',bd=2)
    update_btn.place(relx=0,rely=.5)

    deposit_btn=Button(frm,command=deposit_click,width=15,text='deposit amt',font=('Times New Roman',20),bg='green',bd=2,fg='white')
    deposit_btn.place(relx=0,rely=.6)

    withdraw_btn=Button(frm,command=withdraw_click,width=15,text='withdraw amt',font=('Times New Roman',20),bg='red',bd=2,fg='white')
    withdraw_btn.place(relx=0,rely=.7)

    transfer_btn=Button(frm,command=transfer_click,width=15,text='transfer amt',font=('Times New Roman',20),bd=2,bg='blue')
    transfer_btn.place(relx=0,rely=.8)

    history_btn=Button(frm,command=history_click,width=15,text='txn history',font=('Times New Roman',20),bg='green',bd=2,fg='white')
    history_btn.place(relx=0,rely=.9)

main_screen()
footer_title=Label(win,text="Developed By: Shah Alam\tEmail:shahalam72195@gmail.com\nProject Guide:Mr. Aditya Sir (Ducat Sec-16 Noida)",font=('Times New Roman',20),bg='light gray')
footer_title.pack(side='bottom')
win.mainloop()