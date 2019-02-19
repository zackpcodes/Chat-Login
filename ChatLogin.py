#Author: Zackary Pulaski
import bcrypt
import mysql.connector
from tkinter import *
from tkinter import messagebox
from cryptography.fernet import Fernet

chat = Tk()
#Connect to MySQL database
try:
    loginFRetrieve = open("LK.bin", "rb")
    retrivedKey =  loginFRetrieve.read()
    loginFRetrieve.close()
    loginFRetrieve = open("LC.bin", "rb")
    retrivedLC = loginFRetrieve.read()
    loginFRetrieve.close()

    cipher = Fernet(retrivedKey)
    retrivedLC = cipher.decrypt(retrivedLC)
    retrivedLC = retrivedLC.decode('utf-8')
    lC = retrivedLC.split()

    mydb = mysql.connector.connect(host=lC[0],user=lC[1],passwd=lC[2],database=lC[3])
    del(lC)
except mysql.connector.Error as err:
    chat.withdraw()
    messagebox.showerror("Database Error", "Failed to connect to database")
    exit()



mycursor = mydb.cursor()

#hashPass hashes and returns a string of characters using bcrypt
def hashPass(hP):
    hP = str.encode(hP)
    return bcrypt.hashpw(hP, bcrypt.gensalt())

#userExists checks a database too see if username exists in the database
def userExists(userName):
    mycursor.execute("SELECT username FROM logins WHERE username = %s;", (userName,))
    userResult = mycursor.fetchall()
    if userResult:
        return True
    return False

#Creates a new user in the connected SQL database.
def newUser(nU, nP):
    if userExists(nU) == False:
        hashedPass = hashPass(nP)
        sql = "INSERT INTO logins(username, passwordhash) VALUES(%s,%s)"
        val = (nU, hashedPass)
        mycursor.execute(sql, val)
        mydb.commit()
        chat.title(string="User created")
    else:
        messagebox.showwarning("User Creation Error", "User already exists")

#Checks the connected SQL database for an existing user.
def existingUser(uN, pW):
    if userN.get() != "":
        if userExists(uN) == True:
            pW = str.encode(pW)
            mycursor.execute("SELECT * FROM logins WHERE username = %s;", (uN,))
            passResult = mycursor.fetchall()
            for row in passResult:
                if row[1] == uN and bcrypt.checkpw(pW,str.encode(row[2])):
                    chat.title(string="Login Successful!")
                    mycursor.close()
                elif row[1] == uN and bcrypt.checkpw(pW,str.encode(row[2])) == False:
                    messagebox.showerror("Login Error", "Password/username incorrect")        
        else:
            messagebox.showerror("Login Error", "User does not exist")
    else:
        messagebox.showwarning("Login Error", "Please enter a username")
        


#Main login window
chat.geometry("400x100")
chat.resizable(width=False, height =False)
chat.title(string="Chat")
userN = Entry(master=chat, relief=RAISED)
userN.pack()
userN.place(bordermode=OUTSIDE,height=25, width=125, x=150, y= 20)
userNLabel = Label(master=chat, text="Username:")
userNLabel.pack()
userNLabel.place(bordermode=OUTSIDE,height=25, width=125, x=25, y= 20)

passW = Entry(master=chat, relief=RAISED, show="*")
passW.pack()
passW.place(bordermode=OUTSIDE,height=25, width=125, x=150, y= 50)
passWLabel = Label(master=chat, text="Password:")
passWLabel.pack()
passWLabel.place(bordermode=OUTSIDE,height=25, width=125, x=25, y= 50)

login = Button(master=chat, text='Login',command=lambda: existingUser(userN.get(),passW.get()))
login.pack()
login.place(height=25, width=70, x=300, y=20)

loginCreate = Button(master=chat, text='Create',command=lambda: newUser(userN.get(),passW.get()))
loginCreate.pack()
loginCreate.place(height=25, width=70, x=300, y=50)
    

chat.mainloop()

