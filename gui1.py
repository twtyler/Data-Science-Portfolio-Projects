from tkinter import *
import sqlite3
from tkinter import messagebox
import re


# ===================================================================

# Initialize
# ===================================================================
root = Tk()
root.title("Walmart")
root.geometry("500x300")
conn = sqlite3.connect("data.db")
cur = conn.cursor()

data = cur.execute("select store from manager_store order by store ASC")

df  = []
for item in data:
    df.append(item[0])
print(df)
   



# ===================================================================

# dropdown configuration
# ===================================================================
# Dropdown menu options
options = df
  
# datatype of menu text
clicked = StringVar()
  
# initial menu text
clicked.set( df[0] )
  
# Create Dropdown menu
drop = OptionMenu( root , clicked , *options )

# ===================================================================
# ===================================================================


# ===================================================================
# Variables
# ===================================================================
firstVar = StringVar()
lastVar = StringVar()
emailVar = StringVar()
addrVar = StringVar()
cityVar = StringVar()
stateVar = StringVar()
postalVar = IntVar()
yamVar = IntVar()




# ===================================================================
# Funtions
# ===================================================================
regex = r'\b[A-Za-z0-9._%+-]+@walmart.org\b'
# [A-Za-z0-9.-]+\.[A-Z|a-z]{2,}
def update():
    if firstVar.get() != "" :
        if lastVar.get() != "":
            if postalVar.get() != "" :
                if stateVar.get() != "":
                    if cityVar.get() != "":
                        if addrVar.get() != "":
                            if yamVar.get() != "":
                                if emailVar.get() != "" and re.fullmatch(regex, emailVar.get()):
                                    cur.execute("select postal_code from address where postal_code={}".format(postalVar.get()))
                                    result = cur.fetchone();
                                    print(result)
    #                                 for item in data:
    #                                     value = item
                                    if result:
                                        cur.execute("update manager set first_name='{}', last_name='{}', email = '{}',postal_code='{}', year_as_manager={} where manager_id={}".format(firstVar.get(),lastVar.get() ,emailVar.get(),postalVar.get(),yamVar.get(),clicked.get()))
                                        conn.commit()
                                        firstVar.set("")
                                        lastVar.set("")
                                        cityVar.set("")
                                        emailVar.set("")
                                        addrVar.set("")
                                        yamVar.set(0)
                                        postalVar.set(0)
                                        stateVar.set("")
                                    else:
                                        cur.execute("insert into address (postal_code,city,state,address) values(?,?,?,?)",(postalVar.get(),cityVar.get(), stateVar.get(),addrVar.get()))
                                        cur.execute("update manager set first_name='{}', last_name='{}', email = '{}',postal_code={}, year_as_manager={} where manager_id={}".format(firstVar.get(),lastVar.get() ,emailVar.get(),postalVar.get(),yamVar.get(),clicked.get()))
                                        conn.commit()
                                        firstVar.set("")
                                        lastVar.set("")
                                        cityVar.set("")
                                        emailVar.set("")
                                        addrVar.set("")
                                        yamVar.set(0)
                                        stateVar.set("")
                                        postalVar.set(0)
                                        print("data inserted successfullly")
                                    
                    
                                else:
                                    messagebox.showinfo("showinfo", "email must be properly formarted e.g xxx.yyy@walmart.org")
                            else:
                                messagebox.showinfo("showinfo", "year as manager cannot be blank")

                        else:
                            messagebox.showinfo("showinfo", "Address cannot be blank")
                    else:
                        messagebox.showinfo("showinfo", "City cannot be blank")
                else:
                    messagebox.showinfo("showinfo", "State cannot be blank")    
            else:
                messagebox.showinfo("showinfo", "Postal Code field cannot be blank")
        else:
            messagebox.showinfo("showinfo", "Last Name cannot be blank")
    else:
        messagebox.showinfo("showinfo", "First Name cannot be blank")
        
    
   
        
    
    
    


    
    

    
# ===================================================================
# labels
# ===================================================================

titleLabel = Label(root,text="GUI TO UPDATE MANAGER OF A STORE",font="arial 12")
dropLabel = Label(root,text="Store Number:",font="arial 10")
firstNameLabel = Label(root,text="First Name:",font="arial 10")
lastNameLabel = Label(root,text="Last Name:",font="arial 10")
emailLabel = Label(root,text=" Email:",font="arial 10")
postalLabel =  Label(root,text="Postal Code:",font="arial 10")
stateLabel =  Label(root,text="State:",font="arial 10")
cityLabel =  Label(root,text="City:",font="arial 10")
addrLabel =  Label(root,text="Address:",font="arial 10")
yearsAsManagerLabel =  Label(root,text="Years as Manager:",font="arial 10")


# ===================================================================
# TextFields - Entry
# ===================================================================
firstField = Entry(root,textvariable=firstVar)
lastField = Entry(root,textvariable=lastVar)
emailField = Entry(root,textvariable=emailVar)
postalField = Entry(root,textvariable=postalVar)
stateField = Entry(root,textvariable=stateVar)
cityField = Entry(root,textvariable=cityVar)
addrField = Entry(root,textvariable=addrVar)
yamField = Entry(root,textvariable=yamVar)


# ===================================================================
# buttons
# ===================================================================

updateBtn=Button(root,command=update,text="Update",width=18,height=1,bg="white",fg="black",)


# ===================================================================
# # everything arranged on screen
# ===================================================================
titleLabel.grid(row=1,column=2,)

dropLabel.grid(row=2,column=1,)
drop.grid(row=2,column=2,)

firstNameLabel.grid(row=3,column=1,)
firstField.grid(row=3,column=2,)

lastNameLabel.grid(row=4,column=1,)
lastField.grid(row=4,column=2,)

emailLabel.grid(row=5,column=1,)
emailField.grid(row=5,column=2,)

yearsAsManagerLabel.grid(row=6,column=1,)
yamField.grid(row=6,column=2,)

postalLabel.grid(row=7,column=1,)
postalField.grid(row=7,column=2,)

stateLabel.grid(row=8,column=1,)
stateField.grid(row=8,column=2,)


cityLabel.grid(row=9,column=1,)
cityField.grid(row=9,column=2,)


addrLabel.grid(row=10,column=1,)
addrField.grid(row=10,column=2,)




updateBtn.grid(row=11,column=2,pady=20)











root.mainloop()