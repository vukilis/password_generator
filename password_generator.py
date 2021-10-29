from pathlib import Path
from tkinter import *
from tkinter import ttk
import tkinter as tk
from random import randint
import pyperclip, re
import hashlib
import argon2, binascii
import time
import webbrowser
from tkinter import messagebox
import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

window = Tk()
window.title("Password Generator | Vuk1lis™")
window.iconbitmap('./assets/logo3.ico')
app_width = 1200
app_height = 720
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2 ) - (app_height / 2)
window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
window.configure(bg = "#FFFFFF")
window.attributes('-alpha', 0.99)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

canvas = Canvas(window,bg = "#FFFFFF", height = 720, width = 1200, bd = 0, highlightthickness = 0, relief = "ridge")
canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(600.0, 360.0, image=image_image_1)
psw = chr(randint(33,126))
########################################################GENERATOR#####################################################
def new_rand():
    effectBtn()
    psw_entry['state'] = NORMAL
    psw_entry.delete(0, END)
    pswd_length = int(my_entry.get())
    
    psw = ''
    for x in range(pswd_length):
        if psw_entry.get():
            psw_entry['state'] = DISABLED
        elif pswd_length:
            psw += chr(randint(33,126)) 
    psw_entry.insert(0, psw)
    pswChecker(psw)
    psw_entry['state'] = DISABLED
########################################################PASSWORDMETER#####################################################
def pswChecker(psw):
    global msgbox, msgbox2
    msgbox.destroy()
    msgbox2.destroy()
    if len(psw) == 0:
        msgbox = Label(lf, text="You can't enter 0!", font="Helvetica 14 bold", fg='red', bg="#363739")
        msg.delete(0, 'end')
        msgbox.pack(pady=20, padx=20)
        return psw_entry.delete(0, END)
    if len(psw) < 8:
        print (len(psw))
        print ('Your password is too weak. You need minimum 8 characters')
        msgbox = Label(lf, text="Your password is too weak. You need minimum 8 characters!", font="Helvetica 14 bold", fg='red', bg="#363739")
        msg.delete(0, 'end')
        msgbox.pack(pady=20, padx=20)
        return False
    if len(psw) > 1000:
        print (len(psw))
        print ('Too much characters!!!')
        msgbox = Label(lf, text="Too much characters!!!", font="Helvetica 14 bold", fg='red', bg="#363739")
        msg.delete(0, 'end')
        msgbox.pack(pady=20, padx=20)
        return psw_entry.delete(0, END)
    psw_regex = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-,`:;~)()]).{8,}$')
    if not(psw_regex.search(psw)):
        print ('Your password is weak, can be better! ' + str(psw))
        msgbox = Label(lf, text="Your password is weak, can be better!", font="Helvetica 14 bold", fg='yellow', bg="#363739")
        msg.delete(0, 'end')
        msgbox.pack(pady=20, padx=20)
    else:
        print ('Your password is strong. ' + str(psw))
        msgbox = Label(lf, text="Your password is strong!", font="Helvetica 14 bold", fg='green', bg="#363739")
        msg.delete(0, 'end')
        msgbox.pack(pady=20, padx=20)
        return True

########################################################KOPIRANJE#####################################################
def clipper():
    if hash_entry.get():
        window.clipboard_clear()
        window.clipboard_append(hash_entry.get())
    elif not hash_entry.get():
        window.clipboard_clear()
        window.clipboard_append(psw_entry.get())
########################################################DELETE ALL#####################################################
def delete_all():
    global msgbox, msgbox2
    msgbox.destroy()
    msgbox2.destroy()
    my_entry.delete(0, 'end')
    psw_entry['state'] = NORMAL
    psw_entry.delete(0, END)
    hash_entry['state'] = NORMAL
    hash_entry.delete(0, 'end')
    hash_entry['state'] = DISABLED
    psw_entry['state'] = DISABLED
########################################################PROVERAVA UNETI TIP###############################################
def checkType(input):
    global msgbox, msgbox2
    msgbox.destroy()
    msgbox2.destroy()
    if input.isdigit():
        print(input)
        return True
    elif input == "":
        print(input)
        return True
    else:
        psw_entry.delete(0, END)
        text = "Please enter a number!"
        msgbox = Label(lf, text=text, font=("Helvetica", 14), fg='red', bg="#363739")
        msg.delete(0, 'end')
        msgbox.pack(pady=20, padx=20)
        return False
########################################################CONVERT TO HASH 256 AND Argon2#####################################################
def convert_to_hash():
    global msgbox, msgbox2
    msgbox.destroy()
    msgbox2.destroy()
    hash_entry['state'] = NORMAL
    hash_entry.delete(0, "end")
    psw_to_hash = psw_entry.get()
    psw_to_bytes = bytes(psw_to_hash, 'utf-8')
    salt = os.urandom(16)
    if is_on == False and psw_to_hash:
        hash = argon2.hash_password_raw(
            time_cost=1, memory_cost=2**15, parallelism=8, hash_len=32,
            password=psw_to_bytes, salt=salt, type=argon2.low_level.Type.ID)
        print("Argon2 raw hash:", binascii.hexlify(hash))
        argon2Hasher = argon2.PasswordHasher(
            time_cost=1, memory_cost=2**15, parallelism=8, hash_len=32, salt_len=64)
        hash = argon2Hasher.hash(psw_to_bytes)
        print("Argon2 hash (random salt):", hash)
        verifyValid = argon2Hasher.verify(hash, psw_to_bytes)
        print("Argon2 verify (correct password):", verifyValid)
        try:
            argon2Hasher.verify(hash, "wrong123")
        except:
            print("Argon2 verify (incorrect password):", False)
        msgbox = Label(lf, text="Password is converted to Argon2id", font=("Helvetica", 14), fg='#EFC69B', bg="#363739")
        msg.delete(0, 'end')
        msgbox.pack(pady=20, padx=20)
        text = hash
        hash_entry.insert(0, text)
    elif is_on == True and psw_to_hash:
        hs = hashlib.sha256(psw_to_hash.encode('utf-8'))
        print(hs.hexdigest())
        text = hs.hexdigest()
        hash_entry.insert(0, text)
        msgbox = Label(lf, text="Password is converted to SHA-256", font=("Helvetica", 14), fg='#EFC69B', bg="#363739")
        msg.delete(0, 'end')
        msgbox.pack(pady=20, padx=20)
    elif not my_entry.get() or my_entry.get() == "0":
        text = "Nothing to convert!"
        msgbox = Label(lf, text=text, font=("Helvetica", 14), fg='red', bg="#363739")
        msg.delete(0, 'end')
        msgbox.pack(pady=20, padx=20)
    hash_entry['state'] = DISABLED
########################################################PRIKAZ COPY PORUKA#####################################################
def showmsg():
    global msgbox, msgbox2
    msgbox.destroy()
    msgbox2.destroy()
    if not psw_entry.get():
        expandB()
        msgbox = Label(lf, text="Nothing to copy!", font=("Helvetica", 14), fg='red', bg="#363739")
        msg.delete(0, 'end')
        msgbox.pack(pady=20, padx=20)
        msgbox2.pack()
    if  psw_entry.get() == "Generate strong password!":
            msgbox = Label(lf, text="Nothing to copy!", font=("Helvetica", 14), fg='red', bg="#363739")
            msg.delete(0, 'end')
            msgbox.pack(pady=20, padx=20)
            msgbox2.pack()
    if hash_entry.get():
        msgbox = Label(lf, text="Hash is copied: ", font=("Helvetica", 14), fg='#EFC69B', bg="#363739")
        msgbox2 = Label(lf, text="\""+hash_entry.get()+"\"", font=("Helvetica", 14), fg='#dbb837', bg="#363739")
        msg.delete(0, 'end')
        msgbox.pack(pady=20, padx=20)
        msgbox2.pack()
    else:
        msgbox = Label(lf, text="Password is copied: ", font=("Helvetica", 14), fg='#EFC69B', bg="#363739")
        msgbox2 = Label(lf, text="\""+psw_entry.get()+"\"", font="Helvetica 16 bold", fg='#EFC69B', bg="#363739")
        msg.delete(0, 'end')
        msgbox.pack(pady=20, padx=20)
        msgbox2.pack()
###################################################FOKUS#####################################################
def handle_focus(event):
    psw_entry['state'] = NORMAL
    print("I have gained the focus")
    psw_entry.delete('0', 'end')
    psw_entry['state'] = DISABLED
def handle_outFocus(event):
    psw_entry['state'] = NORMAL
    print("I have gained the outfocus")
    if psw_entry.get():
        psw_entry.delete('0', 'end')
        psw_entry['state'] = DISABLED
        return True
    else:
        psw_entry.insert(0, 'Generate strong password!')
        psw_entry['state'] = DISABLED
###################################################BUTTON-EFFECTS#####################################################
#######################BUTTON-IMG-CHANGE-ON-CLICK-GENERATE#############################
countA = 0
countB = 0
countC = 0
countD = 0
xposA = 277
xposB = 277
xposC = 660
xposD = 641.0
def contractA():
    global countA, xposA
    if countA <= 5 and countA > 0:
        xposA -= 1
        button_1.place(x=xposA) 
        countA -= 1
        window.after(5, contractA)
def expandA():
    global countA, xposA
    if countA < 5:
        xposA += 1
        button_1.place(x=xposA) 
        countA += 1 
        window.after(5, expandA)
    elif countA == 5:
        contractA()
#######################BUTTON-IMG-CHANGE-ON-CLICK-COPY#############################
def contractB():
    global countB, xposB
    if countB <= 5 and countB > 0:
        xposB -= 1
        button_2.place(x=xposB) 
        countB -= 1
        window.after(5, contractB)
def expandB():
    global countB, xposB
    if countB < 5:
        xposB += 1
        button_2.place(x=xposB) 
        countB += 1 
        window.after(5, expandB)
    elif countB == 5:
        contractB()
#######################BUTTON-IMG-CHANGE-ON-CLICK-DELETE#############################
def contractC():
    global countC, xposC
    if countC <= 5 and countC > 0:
        xposC -= 1
        delete_button.place(x=xposC) 
        countC -= 1
        window.after(5, contractC)
def expandC():
    global countC, xposC
    if countC < 5:
        xposC += 1
        delete_button.place(x=xposC) 
        countC += 1 
        window.after(5, expandC)
    elif countC == 5:
        contractC()
#######################BUTTON-IMG-CHANGE-ON-CLICK-HASH#############################
def contractD():
    global countD, xposD
    if countD <= 5 and countD > 0:
        xposD -= 1
        button_3.place(x=xposD) 
        countD -= 1
        window.after(5, contractD)
def expandD():
    global countD, xposD
    if countD < 5:
        xposD += 1
        button_3.place(x=xposD) 
        countD += 1 
        window.after(5, expandD)
    elif countD == 5:
        contractD()
######################BUTTON-IMG-CHANGE-ON-EMPTY-ENTRY##############################  
def effectBtn():
    global msgbox, msgbox2
    msgbox.destroy()
    msgbox2.destroy()
    img = ["image=button_image_1", "image=button_image_5"]
    for x in img:
        if x == "image=button_image_1" and not my_entry.get():
            button_1.config(image=button_image_5)
            expandA()
            msgbox = Label(lf, text="You need to fill entry field!", font=("Helvetica", 14), fg='red', bg="#363739")
            msg.delete(0, 'end')
            msgbox.pack(pady=20, padx=20)
            hash_entry.delete(0, 'end')
            break
        elif x == "image=button_image_5" and my_entry.get(): 
            button_1.config(image=button_image_1)
            print("promena slike iz 2 u 1")
            break
####################################################WIDGETS############################################################

lf = LabelFrame(window, fg="#CAE5FF", cursor="arrow", bd=0, font="Helvetica 12 bold",labelanchor="n", bg="#363739")
lf.pack(pady=220)

msgbox = Label(lf)
msgbox2 = Label(lf)

msgFrame = Frame(window, bg="#363739")
msg = Entry(msgFrame, text="")
msg.place(x=394.5, y=143.0, width=410.0, height=77.0)

def limitSizeEntry(*args):
    value = entrValue.get()
    if len(value) > 4: entrValue.set(value[:4])

entrValue = StringVar()
entrValue.trace('w', limitSizeEntry)

my_entry = Entry(bd=0, bg="#CAE5FF", highlightthickness=0, font=("Helvetica", 24), fg="#292e38", borderwidth=10, relief=FLAT, textvariable=entrValue)
my_entry.focus()
my_entry.place(x=394.5, y=143.0, width=410.0, height=50.0)
reg = my_entry.register(checkType)
my_entry.config(validate="key", validatecommand=(reg, '%P'))

psw_entry = Entry(bd=0, bg="#363739", highlightthickness=0, font=("Helvetica", 24), fg="#CAE5FF", justify='center', state='disabled', cursor="arrow")
psw_entry.config(disabledbackground="#363739", disabledforeground="#CAE5FF", insertbackground='#CAE5FF', exportselection=0)
psw_entry.place(x=394.5, y=320.0, width=410.0, height=77.0)
psw_entry.bind("<FocusIn>", handle_focus)
psw_entry.bind("<FocusOut>", handle_outFocus)
psw_entry.bind("Button-1", lambda:[handle_outFocus(),handle_focus()])

hash_entry = Entry(bd=0, bg="#363739", highlightthickness=0, font=("Helvetica", 18), fg="#96ccff", justify='center', state='disabled', cursor="arrow")
hash_entry.config(disabledbackground="#363739", disabledforeground="#96ccff", insertbackground='#EFC69B', exportselection=0)
hash_entry.place(x=394.5, y=380.0, width=410.0, height=50.0)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))

button_1 = Label(image=button_image_1, relief=GROOVE, activebackground='#363739', borderwidth=0, highlightthickness=0, cursor="hand2")
button_1.bind("<1>", lambda args:[new_rand(), expandA()])
button_1.place(x=277.0, y=486.0, width=281.0, height=74.0)    

button_2 = Label(image=button_image_2, relief=GROOVE, activebackground='#363739', borderwidth=0, highlightthickness=0, cursor="hand2")
button_2.bind("<1>", lambda args:[clipper(),showmsg(), expandB()])
button_2.place(x=277.0, y=598.0, width=281.0, height=74.0)

button_3 = Label(image=button_image_3, relief=GROOVE, activebackground='#363739', borderwidth=0, highlightthickness=0, cursor="hand2")
button_3.bind("<1>", lambda args:[convert_to_hash(), expandD()])
button_3.place(x=641.0, y=598.0, width=281.0, height=74.0)

is_on = True
def switch():
    global is_on
    if is_on:
        on_button.config(image=off)
        button_3.config(image=button_image_4)
        is_on = False
    else:
        on_button.config(image=on)
        button_3.config(image=button_image_3)
        is_on = True
hamburger = True
def hamburger_switch():
    global hamburger
    if hamburger:
        hamburger_close.config(image=hamburger_open_img)
        hamburger = False
    else:
        hamburger_close.config(image=hamburger_close_img)
        hamburger = True

off = PhotoImage(file=relative_to_assets("SHA-256.png"))
on = PhotoImage(file=relative_to_assets("Argon2.png"))
delete_img = PhotoImage(file=relative_to_assets("button_8.png"))
hamburger_close_img = PhotoImage(file=relative_to_assets("button_7.png"))
hamburger_open_img = PhotoImage(file=relative_to_assets("button_6.png"))
    
on_button = Label(window, image=on, bg="#363739", activebackground='#363739', bd=0, cursor="hand2")
on_button.bind("<1>", lambda args:[switch()])
on_button.place(x=790, y=500)

delete_button = Label(image=delete_img, relief=GROOVE, activebackground='#363739', borderwidth=0, highlightthickness=0, cursor="hand2")
delete_button.bind("<1>", lambda args:[delete_all(), expandC()])
delete_button.place(x=660, y=500)

logo = PhotoImage(file=relative_to_assets("logo3.png"))
btnState = False
def switchMenu():
    global btnState
    if btnState is True:
        navRoot.place(x=1201, y=0)
        window.config(bg="gray17")
        btnState = False
    else:
        window.config(bg="green")
        navRoot.place(x=900, y=0)
        btnState = True
    y = 80
    options = ["GITHUB", "HELP", "ABOUT", "LOGO"]
    for option in range(4):
        global myBtn1, myBtn2, myBtn3, nestoooo
        if option == options.index("GITHUB"):
            myBtn1 = Button(navRoot, text=options[option], command=github, font="BahnschriftLight 15", bg="gray17", fg="#CAE5FF", activebackground="gray17", activeforeground="#e6a80b", bd=0, cursor="hand2")
            y += 40
            myBtn1.place(x=25, y=y)
            myBtn1.bind("<Enter>", btnHoverEnterA)
            myBtn1.bind("<Leave>", btnHoverLeaveA)
        if option == options.index("HELP"):
            myBtn2 = Button(navRoot, text=options[option], font="BahnschriftLight 15", bg="gray17", fg="#CAE5FF", activebackground="gray17", activeforeground="#e6a80b", bd=0, cursor="hand2")
            y += 40
            myBtn2.place(x=25, y=y)
            myBtn2.bind("<Enter>", btnHoverEnterB)
            myBtn2.bind("<Leave>", btnHoverLeaveB)
            myBtn2.bind("<1>", lambda args:[help()])
        if option == options.index("ABOUT"):
            myBtn3 = Button(navRoot, text=options[option], font="BahnschriftLight 15", bg="gray17", fg="#CAE5FF", activebackground="gray17", activeforeground="#e6a80b", bd=0, cursor="hand2")
            y += 40
            myBtn3.place(x=25, y=y)
            myBtn3.bind("<Enter>", btnHoverEnterC)
            myBtn3.bind("<Leave>", btnHoverLeaveC)
            myBtn3.bind("<1>", lambda args:[about()])
        if option == options.index("LOGO"):
            nestoooo = Label(navRoot, image=logo, bg="grey17")
            y += 250
            nestoooo.place(x=25, y=y)
def github():  
    webbrowser.open_new(r"https://github.com/vukilis/password_generator")
def btnHoverEnterA(e):
    myBtn1["fg"] = "#EFC69B"
def btnHoverLeaveA(e):
    myBtn1["fg"] = "#CAE5FF"
def btnHoverEnterB(e):
    myBtn2["fg"] = "#EFC69B"
def btnHoverLeaveB(e):
    myBtn2["fg"] = "#CAE5FF"
def btnHoverEnterC(e):
    myBtn3["fg"] = "#EFC69B"
def btnHoverLeaveC(e):
    myBtn3["fg"] = "#CAE5FF"

def about():
    global pop
    pop = Toplevel(window)
    pop.title("About")
    pop_width = 600
    pop_height = 200
    screen_width = pop.winfo_screenwidth()
    screen_height = pop.winfo_screenheight()
    x = (screen_width / 2) - (pop_width / 2)
    y = (screen_height / 2 ) - (pop_height / 2)
    pop.geometry(f'{pop_width}x{pop_height}+{int(x)}+{int(y)}')
    pop.config(bg="gray17")
    
    about_text = " I made this app as a project in purpose to learn python.\nThis is app that I built to generate random password, Also,\n I challenged myself and made that you can convert password\n to two given hash algorithm: SHA-256 and Argon2id\n\nThis project I was started with simple code, then wanted to\n make gui app and finished all of that with using tkinter gui\n framework"
    pop_label = Label(pop, text=about_text,fg="#EFC69B", cursor="arrow", bd=0, font="Helvetica 14 bold", bg="#272729", width=600, height=200,anchor=CENTER, justify=LEFT, relief=RAISED)
    pop_label.pack()

def help():
    pop = Toplevel(window)
    pop.title("Help")
    pop_width = 700
    pop_height = 320
    screen_width = pop.winfo_screenwidth()
    screen_height = pop.winfo_screenheight()
    x = (screen_width / 2) - (pop_width / 2)
    y = (screen_height / 2 ) - (pop_height / 2)
    pop.geometry(f'{pop_width}x{pop_height}+{int(x)}+{int(y)}')
    pop.config(bg="#272729")
    
    title_text = "► Password strength is measured according to:"
    pop_label2 = Label(pop, text=title_text,fg="#e6a80b", cursor="arrow", bd=0, font="Helvetica 14 bold", bg="#272729", justify=LEFT, relief=RAISED, width=700, anchor=CENTER)
    pop_label2.pack(pady=10)  
    help_text = " - At least one upper case English letter\n - At least one lower case English letter\n - At least one digit\n - At least one special character\n - Minimum eight in length"
    pop_label = Label(pop, text=help_text,fg="#EFC69B", cursor="arrow", bd=0, font="Helvetica 12 bold", bg="#272729", justify=LEFT, relief=RAISED, width=700, anchor=CENTER)
    pop_label.pack(pady=10)   
    
    title_text2 = "► What is Argon2:"
    pop_label3 = Label(pop, text=title_text2,fg="#e6a80b", cursor="arrow", bd=0, font="Helvetica 14 bold", bg="#272729", justify=LEFT, relief=RAISED, width=700, anchor=CENTER)
    pop_label3.pack(pady=10)  

    help_text2 = " - Argon2 is a password-hashing function that summarizes the state of the art\n   in the design of memory-hard functions and can be used to hash passwords for\n   credential storage, key derivation, or other applications.\n   Argon2 has three variants: Argon2i, Argon2d, and Argon2id\n   Argon2 is now the winner of the Password Hashing Competition!"
    pop_label4 = Label(pop, text=help_text2,fg="#EFC69B", cursor="arrow", bd=0, font="Helvetica 12 bold", bg="#272729", justify=LEFT, relief=RAISED, width=700, anchor=CENTER)
    pop_label4.pack(pady=10)  

navRoot = Frame(window, bg="gray17", height=720, width=300)
navRoot.place(x=1200, y=0)

hamburger_close = Button(image=hamburger_close_img, relief=GROOVE, activebackground='#363739', borderwidth=0, highlightthickness=0, cursor="hand2")
hamburger_close.bind("<1>", lambda args:[hamburger_switch(), switchMenu()])
hamburger_close.place(x=1110.0, y=30.0, width=60.0, height=50.0)  


window.resizable(False, False)
window.mainloop()