#! /usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
import tkinter as tk
import mariadb
# import MySQLdb #pip install mysqlclient
import sys
from datetime import datetime

global searchwdw


class DB:

    def __init__(self):
        pass

    def connect(self, user, passw):
        self.cur = None
        try:
            conn = mariadb.connect(
                user=user,  # "root",
                password=passw,  # "admin",
                host="127.0.0.1",
                port=3306,
                database="hcac"  # "hcac"
            )
            self.cur = conn.cursor()
            conn.autocommit = True
        except Exception as ex:
            print("error in mariadb" + str(ex))
            sys.exit(1)
        finally:
            return self.cur

    def __del__(self):
        self.cur.close()

    def fetch_details(self):
        try:
            self.cur.execute("SELECT * from civil_details")
            det = self.cur.fetchall()
        except Exception as ex:
            print("exception nin fetch details"+str(ex))
        finally:
            return det

    def fetch_details_from_aadhar(self, adhar):
        self.cur.execute("SELECT * from civil_details WHERE Aadhar_NO =" + adhar)
        det = self.cur.fetchall()
        print(det)
        return det

    def add_details(self, rank, name, adhar, mobile, vechile, vmm, purp, indi):
        ret = self.cur.execute("INSERT into civil_details (`Rank`,  `Name`,  `Aadhar_No`,  `Mobile_Number`,  `Vechile_Number`,`Vechile_Make_and_Model`, `Purpose`, `Individuals`) \
         VALUES (?,?,?,?,?,?,?,?)", (rank, name, adhar, mobile, vechile, vmm, purp, indi))
        return ret

    def update_details(self, rank, name, adhar, mobile, vechile, vmm, purp, indi):
        query = "UPDATE  civil_details SET `Rank`='" + str(
            rank) + "' ,`Mobile_Number`=" + mobile + " ,`Vechile_Number`='" + str(vechile) \
                + "' ,`Vechile_Make_and_Model`='" + str(vmm) + "' ,`Purpose`='" + str(purp) + "' ,`Individuals`='" + str(
            indi) + "' WHERE `Aadhar_No`=" + adhar + \
                " and `Name`='" + str(name)+"'"
        # print(query)
        ret = self.cur.execute(query)
        return ret

    def fetch_name_from_aadhar(self, aad):
        self.cur.execute("SELECT Name from civil_details WHERE Aadhar_NO =" + aad)
        det = self.cur.fetchall()
        return det


DB = DB()


class Table:

    def __init__(self, root, det):

        # code for creating table
        for i in range(len(det)):
            for j in range(len(det[i])):
                self.e = Entry(root, width=15, fg='blue',
                               font=('Arial', 16, 'bold'))

                self.e.grid(row=i + 8, column=j)
                self.e.insert(END, str(det[i][j]))


def login():
    # window
    global tkWindow
    global username
    global password
    tkWindow = Tk()
    tkWindow.geometry('300x100+200+200')
    tkWindow.title('Login page')

    # username label and text entry box
    usernameLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
    username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)

    # password label and password entry box
    passwordLabel = Label(tkWindow, text="Password").grid(row=1, column=0)
    password = StringVar()
    passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)

    # login button
    loginButton = Button(tkWindow, text="Login", command=validateLogin).grid(row=4, column=0)

    tkWindow.mainloop()


def validateLogin():
    val = DB.connect(username.get(), password.get())
    if (val == None):
        password_not_recognised()
    else:
        delete_login_page()
        civil_entry()


def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(tkWindow)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()


def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_login_page():
    tkWindow.destroy()


def civil_entry():
    global civilwdw
    global aadhar
    global mobile
    global aadharLabel
    civilwdw = tk.Tk()
    civilwdw.geometry('300x100+200+200')

    civilwdw.title("Civil Details")
    w = Label(civilwdw, text="Holta Camp Area Details").grid(row=0, column=0)

    aadharLabel = Label(civilwdw, text="Aadhar no").grid(row=1, column=0)
    aadhar = StringVar()
    aadharEntry = Entry(civilwdw, textvariable=aadhar).grid(row=1, column=1)

    # password label and password entry box
    MobileLabel = Label(civilwdw, text="Mobile").grid(row=3, column=0)
    mobile = StringVar()
    MobileEntry = Entry(civilwdw, textvariable=mobile).grid(row=3, column=1)

    SearchButton = Button(civilwdw, text="Search", command=searchentry).grid(row=6, column=0)
    addButton = Button(civilwdw, text="ADD", command=insertentry).grid(row=6, column=1)

    # Code to add widgets will go here...

    civilwdw.mainloop()


def searchentry():
    try:
        searchwdw.destroy()
    except:
        print("No window available")

    searchwdw = tk.Tk()
    det = DB.fetch_details()
    list = []
    for i in det:
        if mobile.get().strip() == str(i[4]) or aadhar.get().strip() == str(i[3]):
            print(i)
            list.append(i)
    list.insert(0, (
    "S.No", "Rank", "Name", "Aadhar_No", "Mobile_Number", "Vechile_Number", "Vechile_Make_and_Model", "Time", "Purpose",
    "Individuals"))
    t = Table(searchwdw, list)


def insertentry():
    global civildetailform
    global Rank
    global Name
    global Vehicle
    global Vehiclemm
    global Purpose
    global Individuals
    civildetailform = Toplevel(civilwdw)
    civilwdw.geometry('300x300')
    alldetails = DB.fetch_details_from_aadhar(aadhar.get())
    civilwdw.title("Civil Details Entry")

    RankLabel = Label(civildetailform, text="Rank").grid(row=1, column=0)
    Rank = StringVar()
    RankEntry = Entry(civildetailform, textvariable=Rank).grid(row=1, column=1)

    # password label and password entry box
    NameLabel = Label(civildetailform, text="Name").grid(row=3, column=0)
    Name = StringVar()
    NameEntry = Entry(civildetailform, textvariable=Name).grid(row=3, column=1)
    # n = ()
    # n = DB.fetch_name_from_aadhar(aadhar.get())
    # if(n):
    #     Name.set(n[0])
    #     n=()
    GaadiLabel = Label(civildetailform, text="Vehicle Number").grid(row=5, column=0)
    Vehicle = StringVar()
    NameEntry = Entry(civildetailform, textvariable=Vehicle).grid(row=5, column=1)

    GaadidetailLabel = Label(civildetailform, text="Vehicle Make & Model").grid(row=7, column=0)
    Vehiclemm = StringVar()
    NameEntry = Entry(civildetailform, textvariable=Vehiclemm).grid(row=7, column=1)

    PurposeLabel = Label(civildetailform, text="Purpose of visit").grid(row=9, column=0)
    Purpose = StringVar()
    PurposeEntry = Entry(civildetailform, textvariable=Purpose).grid(row=9, column=1)

    IndividualsLabel = Label(civildetailform, text="Number of Individuals").grid(row=11, column=0)
    Individuals = StringVar()
    IndividualsEntry = Entry(civildetailform, textvariable=Individuals).grid(row=11, column=1)
    if (alldetails):
        Name.set(alldetails[0][2])
        Vehicle.set(alldetails[0][5])
        Vehiclemm.set(alldetails[0][6])
        Rank.set(alldetails[0][1])

    # login button

    submit = Button(civildetailform, text="Submit", command=Submit).grid(row=13, column=0)


def Submit():
    det = DB.fetch_details()
    # print(det)
    list = []
    for i in det:
        if mobile.get().strip() == str(i[4]) or aadhar.get().strip() == str(i[3]):
            list.append(i)
    if (list):
        val = DB.update_details(Rank.get(), Name.get(), aadhar.get(), mobile.get(), Vehicle.get(), Vehiclemm.get(),
                                Purpose.get(), Individuals.get())
    else:
        val = DB.add_details(Rank.get(), Name.get(), aadhar.get(), mobile.get(), Vehicle.get(), Vehiclemm.get(),
                             Purpose.get(), Individuals.get())
    if (val == None):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        civildetailform.destroy()
        f = open("Details.txt", 'w')
        f.write("\n ENTRY DETAILS \n")
        f.write("\nName               :\t" + str(Name.get()))
        f.write("\nAadhar No          :\t" + str(aadhar.get()))
        f.write("\nMobile             :\t" + str(mobile.get()))
        f.write("\nVehicle no         :\t" + str(Vehicle.get()))
        f.write("\nVehicle model      :\t" + str(Vehiclemm.get()))
        f.write("\nPurpose of visit   :\t" + str(Purpose.get()))
        f.write("\nEntry Time         :\t" + str(dt_string))
        f.write("\nNo. of Individuals :\t" + str(Individuals.get()))
        f.close()


if __name__ == '__main__':
    login()
    # add_details(1234, "inu", 1234567, 968197, "Hp12312141", "maruti ciaz 2002")
    # fetch_details()
    # root = tk.Tk()
    # portFrame = HiLabels(root)
    # portFrame.grid(w=0, column=0, padx=10)
    # root.mainloop()
