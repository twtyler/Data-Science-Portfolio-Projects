from tkinter import *
import sqlite3
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt


# ===================================================================

# Initialize
# ===================================================================
root = Tk()
root.title("Walmart")
root.geometry("500x200")
conn = sqlite3.connect("data.db")
cur = conn.cursor()






# ===================================================================

# dropdown configuration
# ===================================================================
# Dropdown menu options
options = ['A','B','C']
  
# datatype of menu text
clicked = StringVar()
  
# initial menu text
clicked.set('A')
  
# Create Dropdown menu
drop = OptionMenu( root , clicked , *options )

# ===================================================================
# ===================================================================




# ===================================================================
# Variables
# ===================================================================
resultVar = IntVar()
storeVar  = IntVar()
deptVar = IntVar()


storeVar.set(1)
deptVar.set(1)


# ===================================================================
# Funtions
# ===================================================================


def computeMean():
    data = cur.execute("select size from store_data where type = '{}'".format(clicked.get()))
    df  = []
    for item in data:
        df.append(item[0])
    count = 0
    for fig in df:
        count += 1
    res = sum(df)/count
    resultVar.set(res)
   
    


def graph():
    sales = []
    date = []
    data = cur.execute("select weekly_sales,date from sales_data where store = {} and  department={} ".format(storeVar.get(),deptVar.get()))
    for item in data:
        sales.append(item[0])
        date.append(item[1])
    print(sales)
    print(date)
    date_time = pd.to_datetime(date)
    DF = pd.DataFrame()
    DF['value'] = sales
    DF = DF.set_index(date_time)
    plt.scatter(date_time,DF)
    plt.gcf().autofmt_xdate()
    plt.show()
    

# ===================================================================
# labels
# ===================================================================

titleLabel = Label(root,text="GUI TO UPDATE MANAGER OF A STORE",font="arial 12")
dropLabel = Label(root,text="Select store type:",font="arial 10")

storeLabel = Label(root,text="Store:",font="arial 10")
deptLabel = Label(root,text="Department:",font="arial 10")




# ===================================================================
# TextFields - Entry
# ===================================================================
resultField = Entry(root,textvariable=resultVar)
storeField = Entry(root,textvariable=storeVar)
departmentField = Entry(root,textvariable=deptVar)


# ===================================================================
# buttons
# ===================================================================

computeBtn=Button(root,command=computeMean,text="Compute mean",width=18,height=1,bg="white",fg="black",)

graphBtn=Button(root,command=graph,text="Plot graph",width=18,height=1,bg="white",fg="black",)



    
# ===================================================================
# everything arranged on screen
# ===================================================================
# titleLabel.grid(row=1,column=,)

dropLabel.grid(row=1,column=1)
drop.grid(row=1,column=2)

computeBtn.grid(row=1,column=3)

resultField.grid(row=1,column=5, padx=10)

# ==============================================================



storeLabel.grid(row=3,column=2, pady=(20,0))
storeField.grid(row=3,column=3,pady=(20,0))



deptLabel.grid(row=4,column=2,)
departmentField.grid(row=4,column=3,)


graphBtn.grid(row=5,column=3,pady=(10,0))










root.mainloop()