from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime , timedelta
from notification_manager import NotificationManager
from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
import os

window = Tk()
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

window.title("Cheap Flight Ticket Finder")
window.minsize(width=600,height=750)
window.configure(bg="mint cream")


def post_data():
    currentCity = input_1.get()
    DestinationCity = input_2.get()
    lowestPrice = int(input_3.get())

    data_manager.post_destination_data(DestinationCity,lowestPrice)

def radioButton_used():
    if(radio_state.get() == 1):
        input_1.config(state="normal")
        input_2.config(state="normal")
        input_3.config(state="normal")
        button1.config(state="normal")
        button_2.config(state="normal")
        button_4.config(state="disabled")

    elif radio_state.get() == 2:
        button_4.config(state="active")
        input_1.config(state="disabled")
        input_2.config(state="disabled")
        input_3.config(state="disabled")
        button1.config(state="disabled")
        button_2.config(state="disabled")

def clear_data():
    input_1.delete(0,END)
    input_2.delete(0, END)
    input_3.delete(0, END)
    inputArea.delete(1.0, END)


def showList():
    sheet_data = data_manager.get_destination_data()
    inputArea.delete("1.0","end")
    inputArea.insert(INSERT,list(sheet_data[0].keys())[0])
    inputArea.insert(INSERT, " ")
    inputArea.insert(INSERT, list(sheet_data[1].keys())[1])
    inputArea.insert(INSERT, " ")
    inputArea.insert(INSERT, list(sheet_data[1].keys())[2])
    inputArea.insert(INSERT, " ")
    inputArea.insert(INSERT, "\n")
    for data in sheet_data:
        inputArea.insert(INSERT,data["city"])
        inputArea.insert(INSERT, " ")
        inputArea.insert(INSERT, data["iataCode"])
        inputArea.insert(INSERT, " ")
        inputArea.insert(INSERT, data["lowestPrice"])
        inputArea.insert(INSERT, "\n")

def iataCodeSetter():
    sheet_data = data_manager.get_destination_data()
    flag = False

    for row in sheet_data:
        if row['iataCode'] == "":
            row['iataCode'] = flight_search.get_destination_code(row["city"])
            flag = True
        else:
            flag = False

    print(f"sheet_data:\n {sheet_data}")

    if flag == True:
        data_manager.destination_data = sheet_data
        data_manager.update_destination_codes()

def flightNotification():
    sheet_data = data_manager.get_destination_data()
    tomorrow = datetime.now() + timedelta(days=1)
    six_month_from_today = datetime.now() + timedelta(days=(6*30))

    for destination in sheet_data:
        flight = flight_search.check_flight(destination["iataCode"],tomorrow.strftime("%d/%m/%Y"),six_month_from_today.strftime("%d/%m/%Y"))
        if flight is not None and flight.price < int(destination["lowestPrice"]):
            notification_manager.send_mail(message=f"Low Price Alert !\n\n Our Project help's the customer to find the Lowest price deal and also inform them via email \n Flight Deal Information:- \nOnly ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport},\n from {flight.out_date} to {flight.return_date}.\n\n Thanks & Regard\n Shivansh Chauhan")

    messagebox.showinfo("Flight Alert!","Please Check Your Email Account All The Details Are Send !!\n"
                                        "Thank You For Using Our Service")
    print("Credit:- SHIVANSH CHAUHAN")

heading = Label(text="Flight Ticket Finder System",font=("Arial",18,"bold"),background="mint cream")
heading.place(x=180,y=0)

canvas = Canvas(width=150,height=100,bg="mint cream")
canvas.place(x=240,y=50)
photo = Image.open("airplane.png")
newPhoto = photo.resize((150,100))
img = ImageTk.PhotoImage(newPhoto)
canvas.create_image(0,0,image=img,anchor=NW)

my_label = Label(text="Enter Current City Name",font=("Arial",12),background="mint cream")
my_label.place(x=30,y=180)

input_1 = Entry(width=25)
input_1.place(x=300,y=180)

label_2 = Label(text="Enter Destination City's Name",font=("Arial",12),background="mint cream")
label_2.place(x=30,y=215)

input_2 = Entry(width=25)
input_2.place(x=300,y=215)

my_label_3 = Label(text="Enter Your Affordable Price ",font=("Arial",12),background="mint cream")
my_label_3.place(x=30,y=250)

input_3 = Entry(width=25)
input_3.place(x=300,y=250)

button1 = Button(text="Add City's",width=24,height=2,command=post_data)
button1.place(x=170,y=300)

label_3 = Label(text="Click Set IATACODE Button After Adding All Favourite City's",font=("Arial",12),background="mint cream")
label_3.place(x=30,y=360)

button_2 = Button(text="Set IataCode",width=12,height=2,command=iataCodeSetter)
button_2.place(x=470,y=350)

label_4 = Label(text="View Favourite List",font=("Arial",12),background="mint cream")
label_4.place(x=220,y=400)

inputArea = Text(window,height=10,width=40)
inputArea.place(x=130,y=420)

button_3 = Button(text="Show List",width=24,command=showList)
button_3.place(x=200,y=590)

label_5 = Label(text="Choose Appropriate Option ",font=("Arial",12),background="mint cream")
label_5.place(x=30,y=630)

radio_state = IntVar()
radioButton_1 = Radiobutton(text="Add City's",value=1,variable=radio_state,command=radioButton_used,background="mint cream")
radioButton_2 = Radiobutton(text="Get Result",value=2,variable=radio_state,command=radioButton_used,background="mint cream")
radioButton_1.place(x=240,y=630)
radioButton_2.place(x=340,y=630)
radioButton_1.select()


button_4 = Button(text="Get Results",width=24,height=2,command=flightNotification,state="disabled")
button_4.place(x=80,y=670)

button_5 = Button(text="Clear",width=24,height=2,command=clear_data)
button_5.place(x=380,y=670)






window.mainloop()