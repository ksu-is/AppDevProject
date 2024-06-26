import sqlite3
from sqlite3 import Error

conn = sqlite3.connect('automtc.ed')

c=conn.cursor()

sql_query = """SELECT name FROM sqlite_master WHERE type='table';"""
c.execute(sql_query)
results = c.fetchall()
results_list = [item[0] for item in results]
if 'maintenance' not in results_list:
    c.execute("""CREATE TABLE maintenance (
                vehicle text,
                service text,
                date text,
                mileage text
                )""")

conn.commit()

def insert_data():
    vehicle = input("What vehicle is it?: ")
    service = input("What service was done?: ")
    date = input ("When was the service done?: ")
    mileage = input("How many miles did the vehicle have when it was done?: ")
    try:      
        sqlresult = conn.execute("INSERT INTO maintenance (vehicle,service,date,mileage)\
            values("+"'"+ str(vehicle) +"'" + ",'"+ str(service) +"', '"+ str(date) +"','"+ str (mileage)+"')")
        result = conn.commit()
        if result == None:
            print("*** Data saved to database. ***")
    except Error as e:
        print ("*** Insert error: ",e)
        pass
def view_data():
    try:
        cursor = conn.execute ("SELECT vehicle,service,date,mileage FROM maintenance")
        alldata = []
        alldata.append(["vehicle","service","date","mileage"])
        for row in cursor:
            thisrow=[]
            for x in range(4):
                thisrow.append(row[x])
            alldata.append(thisrow)
        return alldata
    except Error as e:
        print (e)
        pass

def update_data():
    for row in view_data():
            thisrow = "  --> "
            for item in row:
                thisrow += str(item) + "  "
            print (thisrow)
    print('''1 = edit vehicle\n 2 = edit service\n 3 = edit date\n 4 = edit mileage''')
    update_ID = input("Enter the vehicle you want to update: ")
    feature = input("Enter which feature of the data you want to edit: ")
    update_value = input ("Editing "+feature+ ": enter the new data: ")

    if(feature == "1"):
        sql = "UPDATE maintenance set vehicle = ? where vehicle = ?"
    elif (feature == "2"):
       sql = "UPDATE maintenance set service = ? where vehicle =  ?" 
    elif (feature == "3"):
       sql = "UPDATE maintenance set date = ? where vehicle =  ?"
    elif (feature == "4"):
       sql = "UPDATE maintenance set mileage  = ? where vehicle =  ?"
    try:
        conn.execute(sql, (update_value, update_ID))
        conn.commit()
        print("Data updated successfully.")
    except Error as e:
        print("Error updating data:", e)

def delete_data():
    for row in view_data():
            thisrow = "  --> "
            for item in row:
                thisrow += str(item) + "  "
            print (thisrow)
    id_  =  input("Enter the vehicle you want to delete:")
    cursor = conn.cursor()
    cursor.execute("select vehicle from maintenance where vehicle = ?",(id_,))
    delete_item = cursor.fetchall()
    confirm = input("Are you sure you want to delete " + id_ + " " + str(delete_item[0]) + "? (Enter 'y' to confirm.)")
    if confirm.lower() == "y":
        try:
            delete_sql = "DELETE FROM maintenance WHERE vehicle = ?"
            conn.execute(delete_sql, (id_,))
            result = conn.commit()
            if result == None:
                print (id_ + " " + str(delete_item[0]) + " deleted.")
            else:
                print ("Deletion failed during SQL execution.")
        except Error as e:
            print (e)
            pass
    else:
        print("Deletion aborted.")

def tip_data():
    service_perf = input("What service was/will be performed?\n 1 = Oil Change\n 2 = Tire Replacement\n 3 = Air Filter Replacement\n 4 = Brake Pad Replacements\n 5 = Coolant Change\n 6 = Other\n Choose an operation to perform: ")
    if service_perf == '1':
        amiles = input("How many miles are/were on the car before?: ")
        print("Your next oil change should be at", int(amiles) + 4000, "miles!")
        print("We recommend oil changes every 4,000-5,000 miles but always be sure to check your vehicle's owner's manual!")
    if service_perf == '2':
        amiles = input("How many miles are/were on the car before?: ")
        print("Your next tire replacement should be at", int(amiles) + 50000, "miles!")
        print("We recommend tire replacements every 60,000-75,000 miles but always be sure to check your vehicle's owner's manual!")
    if service_perf == '3':
        amiles = input("How many miles are/were on the car before?: ")
        print("Your next air filter replacement should be at", int(amiles) + 50000, "miles!")
        print("We recommend air filter replacements every 15,000-30,000 miles but always be sure to check your vehicle's owner's manual!")
    if service_perf == '4':
        amiles = input("How many miles are/were on the car before?: ")
        print("Your next brake pad replacements should be at", int(amiles) + 25000, "miles!")
        print("We recommend brake pad replacements every 25,000-50,000 miles but always be sure to check your vehicle's owner's manual!")
    if service_perf == '5':
        amiles = input("How many miles are/were on the car before?: ")
        print("Your next coolant change should be at", int(amiles) + 30000, "miles!")
        print("We recommend coolant changes every 30,000-45,000 miles but always be sure to check your vehicle's owner's manual!")
    if service_perf == '6':
        print("We recommend to check up on all your services at least every 5,000 miles but always be sure to check your vehicle's owner's manual!")
    

while True:
    print("Welcome to MyAutoCare! How may we assist you today?\n 1 = View Vehicle Information\n 2 = Insert new Vehicle Information\n 3 = Update Vehicle Information\n 4 = Delete Vehicle Information\n 5 = Helpful Tips\n 6 = Exit")
    name = input ("Choose an operation to perform: ")
    if (name =="1"):
        for row in view_data():
            thisrow = "  --> "
            for item in row:
                thisrow += str(item) + "  "
            print (thisrow)
    elif(name == "2"):
        insert_data()
    elif(name == "3"):
        update_data()
    elif(name == "4"):
        delete_data()
    elif(name == "5"):
        tip_data()
    elif(name == "6"):
        conn.close()
        break