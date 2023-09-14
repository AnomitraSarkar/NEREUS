'''
THIS IS THE FIRST VERSION OF THE HOME WATER MANAGEMENT SYSTEM
WITH ONLY LIMITED FEATURES FOR NOW
TO ADD WATER OPTIONS LIKE AUTOMATE FILL IS THE ONLY OPTIONS AVAILABLE, ETC
THIS VERSION IS A BRIEF IDEA OF THE CONCEPT
PAYMENT METHODS ARE NOT ADDED...
(IF RUNNING THE CODE RUN IT DIRECTLY IN CMD OR AS AN EXE FILE)
~ANOMITRA SARKAR

'''

# IMPORTS ---------------------------------------------------------

import os

install = input("Do you want to install packages?(Y/N): ")
if install.upper() == "Y":
    print("installing package")
    list = ['pyautogui', 'tabulate', 'mysql-connector-python']
    for i in list:
        if os.system(f"pip install {i}"):
            print(f"RAN INTO AN ERROR...\nCOULDN'T INSTALL {i}")

# ---------------

from time import sleep as delay
import csv
import datetime
import mysql.connector
from tabulate import tabulate as table_creator
import pyautogui as pag


# Rate ------------------------------------------------------------
rate = 0.005
# per litre of water for domestic purpose, to be edited statically


# FUNCTIONS -------------------------------------------------------

def clear_screen(): return os.system("cls")


def connection(x):
    global db
    global cursor
    db = mysql.connector.connect(
        host="localhost", user="root", password=x)
    cursor = db.cursor()


def intialize(x):
    global username
    global name
    global capacity
    try:
        connection(x)
    except:
        print("Authentication Denied!")
        return False
    print('Success: Inside The Server')
    username = pag.password(text='Enter your Username', title="USERNAME")
    try:
        cursor.execute("create database if not exists water_general;")
        cursor.execute("create database if not exists water_home;")
        cursor.execute("use water_general;")
        cursor.execute(
            f"SELECT NAME, CAPACITY FROM water_general.MEMB WHERE USERNAME = '{username}';")
        check_user = cursor.fetchone()
        if check_user == None:
            print("User Doesn't Exists")
        capacity = check_user[1]
        name = check_user[0]
        print(
            f"Verified User, Hello! {name}\nLocal Tank Capacity => {capacity}")
        delay(2.5)
    except Exception as e:
        print("Error: " + str(e))
        return False
    cursor.execute("use water_home;")
    cursor.execute(
        f"create table if not exists local_{capacity}_{username}(Current_Water_Level int not null, Date date not null);")
    cursor.execute(
        "create table if not exists ParentTank(Current_Water_Level int not null, Date date not null);")
    cursor.execute(
        f"create table if not exists bill_{username}(Transaction_ID int not null auto_increment primary key, Date date not null, Water_Filled int, Request_Water int, Amount int not null)")
    db.commit()
    print("Necessary Tables Made...")
    DefaultForNewEntry()
    warnings = generalCheckup()
    print("Checkup Summary: ", end=" ")
    for i in warnings:
        print(i, end=", ")
    print("")
    if warnings != []:
        print("Resolving warnings...")
        resolve_warnings(warnings)
    delay(3)
    clear_screen()
    return True


def DefaultForNewEntry():
    global newEntryStatus
    cursor.execute(f"select * from local_{capacity}_{username}")
    data = cursor.fetchone()
    if data == None:
        cursor.execute(
            f"insert into local_{capacity}_{username} values(0, '0000-00-00');")
        db.commit()
        print("Entered Default Data for New Entry")
        pre_data = [
            ['username', username],
            ['capacity', capacity],
            ['allowance', 0],
            ['start_code', 0],
            ['start_date', 0000-00-00],
            ['end_code', 0],
            ['end_date', 0000-00-00]
        ]
        f = open(f"local_{capacity}_{username}.csv", "w", newline="")
        csv_writer = csv.writer(f)
        csv_writer.writerows(pre_data)
        print("Created Default File for New Entry")
        f.close()
        newEntryStatus = True
    else:
        newEntryStatus = False


def generalCheckup():
    global ParentEmpty
    ParentEmpty = False
    connection(x)
    warn = []
    if f'local_{capacity}_{username}.csv' not in os.listdir(os.getcwd()):
        warn.append('NO_BASE_FILE')
    cursor.execute('select current_water_level from water_home.parenttank;')
    parentCap = cursor.fetchall()[-1][0]
    if parentCap == 0:
        warn.append('PARENT_TANK_EMPTY')
        ParentEmpty = True
    cursor.execute(
        f'select req_water from water_general.req_water where req_username = "{username}" and status = "D"')
    reqw = cursor.fetchall()
    if reqw != []:
        warn.append(reqw)
    return warn
    # this will insure that the status quotient is at the end


def resolve_warnings(warn_list):
    connection(x)
    if 'PARENT_TANK_EMPTY' in warn_list:
        cursor.execute(
            'insert into water_general.notification(notifications) values("~Status:Parent Tank:Empty")')
        db.commit()
        # make request to fill the parent tank
        # cancel add water for unavailability

    if 'NO_BASE_FILE' in warn_list:
        pre_data = [
            ['username', username],
            ['capacity', capacity],
            ['allowance', 0],
            ['start_code', 0],
            ['start_date', 0000-00-00],
            ['end_code', 0],
            ['end_date', 0000-00-00]
        ]
        with open(f"local_{capacity}_{username}.csv", "w", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(pre_data)
            print("Created Default File for New Entry")

    for ls in warn_list:
        if type(ls) == list:
            allrec = []
            cursor.execute(
                f"delete from water_general.req_water where req_username = '{username}' and status = 'D'")
            db.commit()

            with open(f'local_{capacity}_{username}.csv') as f:
                csv_reader = csv.reader(f)
                for i in csv_reader:
                    allrec.append(i)

            cap_allowed = 0
            for i in ls:
                cap_allowed += int(i[0])

            allrec[2][1] = cap_allowed

            cursor.execute(
                f"insert into water_home.bill_{username}(Date, Request_Water, Amount) values(curdate(), {cap_allowed},{rate}*{cap_allowed});")
            db.commit()
            print(f"Requested Water of {cap_allowed} Added to Allowance!")
            with open(f'local_{capacity}_{username}.csv', 'w', newline='') as f1:
                csv_writer = csv.writer(f1)
                csv_writer.writerows(allrec)

    print("Resolved problems...")
    print("Adviced to contact Administrator...")


def Referesh(NEState=False):
    allrec = []
    connection(x)
    cursor.execute("use water_home;")
    if NEState:
        f = open(f"local_{capacity}_{username}.csv")
        csv_reader = csv.reader(f)
        for rec in csv_reader:
            allrec.append(rec)
        f.close()
        cursor.execute(
            f"select * from water_home.bill_{username} order by transaction_id desc limit 2;")
        ref_data = cursor.fetchall()
        cursor.execute(
            f"select * from water_home.bill_{username} order by transaction_id desc limit 2;")
        ref_data = cursor.fetchall()
        start_code = ref_data[0][0]
        start_date = ref_data[0][1]
        allrec[3][1] = start_code
        allrec[4][1] = start_date
        f1 = open(f"local_{capacity}_{username}.csv", "w", newline="")
        csv_writer = csv.writer(f1)
        csv_writer.writerows(allrec)
        f1.close()
        NEState = False
    else:
        cursor.execute(
            f"select * from water_home.bill_{username} order by transaction_id desc limit 2;")
        ref_data = cursor.fetchall()
        print("Wait a mintute...\tChecking Something...")
        print(ref_data)
        if len(ref_data) == 1:
            print("Still a new entry...")
        else:
            cur_date = ref_data[0][1]
            prev_date = ref_data[1][1]
            print(prev_date, "and", cur_date)
            print(prev_date.strftime("%B"), "and", cur_date.strftime("%B"))
            if prev_date.strftime("%B") != cur_date.strftime("%B"):
                print("New Month Identified...\nMaking bill for the new month...")
                cur_code = ref_data[0][0]
                prev_code = ref_data[1][0]
                f = open(f"local_{capacity}_{username}.csv")
                csv_reader = csv.reader(f)
                rec = []
                for i in csv_reader:
                    rec.append(i)
                start_code = rec[3][1]
                start_date = rec[4][1]
                f.close()
                makeBillforMonth(start_code, start_date, prev_code, prev_date)
                f = open(f"local_{capacity}_{username}.csv")
                allrec, reader = [], csv.reader(f)
                for i in reader:
                    allrec.append(i)
                f.close()
                allrec[3][1] = cur_code
                allrec[4][1] = cur_date
                f1 = open(f"local_{capacity}_{username}.csv", "w", newline="")
                csv_writer = csv.writer(f1)
                csv_writer.writerows(allrec)
                f1.close()
            else:
                pass


def makeBillforMonth(start_code, start_date, end_code, end_date):
    connection(x)
    cursor.execute("use water_home")
    cursor.execute(
        f"select sum(water_filled), sum(amount), sum(request_water) from water_home.bill_{username} where transaction_id>={start_code} and transaction_id<={end_code};")
    ls = cursor.fetchone()
    total_Waterfilled, total_Amount, total_Requestwater = ls[0], ls[1], ls[2]
    f = open(
        f"bill_{username}_{end_date.strftime('%B')}-{end_date.strftime('%Y')}.csv", 'w', newline='')
    structure = [
        ['USERNAME:', username, 'CATAGORY:', 'General'],
        ['NAME:', name, 'CAPACITY:', capacity],
        ['START CODE:', start_code, 'END CODE:', end_code],
        ['START DATE:', start_date, 'END DATE:', end_date],
        ['TOTAL WATER WITDRAWN:', total_Waterfilled,
            'MONTH OF BILL:', end_date.strftime("%B")],
        ['TOTAL REQUESTED WATER:', total_Requestwater,
            'YEAR OF BILL:', end_date.strftime("%Y")],
        ['TOTAL BILL AMOUNT:', total_Amount, 'PAYTO:',
            'Municipal Corp - 9687XXXX01']
    ]
    csv_writer = csv.writer(f)
    csv_writer.writerows(structure)
    f.close()
    print("Bill Made for the Month:", f.name)


def updation(fill_amount):
    connection(x)
    if fill_amount >= current_parent_level:
        fill_amount = current_parent_level
    cursor.execute(
        f"insert into water_home.parenttank values({current_parent_level}-{fill_amount}, curdate());")
    cursor.execute(
        f"insert into water_home.local_{capacity}_{username} values({current_water_level}+{fill_amount}, curdate());")
    cursor.execute(
        f"insert into water_home.bill_{username}(Date, Water_filled, Amount) values(curdate(), {fill_amount},{rate}*{fill_amount});")
    allrec[2][1] = str(allowance)
    f = open(f"local_{capacity}_{username}.csv", "w", newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerows(allrec)
    f.close()
    db.commit()


def Add_Water_Automated(ParentEmpty=False):

    # the water level of parent tank and local tank is monitored according to a sensor,
    # so the model is successful for positive values hence creating a real life simulation of the model.

    if ParentEmpty:
        print("Cannot Add Water in Local Tank...\nParent Tank is Empty...")

    else:
        global allrec
        global allowance
        global current_water_level
        global current_parent_level
        global last_date
        global current_date
        global fill_amount
        connection(x)
        cursor.execute("use water_home;")
        print("Filling Water Accordingly...")
        allrec = []
        f = open(f"local_{capacity}_{username}.csv")
        csv_reader = csv.reader(f)
        for i in csv_reader:
            allrec.append(i)
        f.close()
        allowance = int(allrec[2][1])
        cursor.execute(
            f"SELECT * from water_home.local_{capacity}_{username};")
        record = cursor.fetchall()[-1]
        current_water_level = record[0]
        last_date = record[1]
        cursor.execute(f"SELECT * from water_home.parenttank;")
        current_parent_level = cursor.fetchall()[-1][0]
        current_date = datetime.date.today()
        fill_amount = capacity - current_water_level

        if fill_amount == 0:
            print("OVERFLOW:\tTANK ALREADY FULL...")

        elif last_date == current_date and allowance == 0:
            print("OVERFLOW:\tNO ALLOWANCE WATER LEFT...")

        elif last_date != current_date:
            fill_amount = capacity - current_water_level
            allowance += current_water_level
            updation(fill_amount)
            print("STATUS:\tTANK FILLED...")

        elif last_date == current_date and allowance <= fill_amount and allowance != 0:
            fill_amount = allowance
            allowance = 0
            updation(fill_amount)
            print("STATUS:\tTANK FILLED...")

        elif last_date == current_date and allowance > fill_amount and allowance != 0:
            allowance -= fill_amount
            updation(fill_amount)
            print("STATUS:\tTANK FILLED...")

        else:
            print("STATUS:\tRAN INTO A PROBLEM, TRY LATER...")


def SHOW_BILL():
    bill_dat = []
    try:
        month = input("Enter month number(1-12): ")
        year = input("Enter year: ")
        flname = f"bill_{username}_{datetime.datetime.strptime(month,'%m').strftime('%B')}-{year}.csv"
        if flname in os.listdir(os.getcwd()):
            with open(flname) as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    bill_dat.append(row)
                print("\n<< "+f.name.upper()+" >>")
                print(table_creator(bill_dat, tablefmt="fancy_grid"))
                del bill_dat
        else:
            print("Bill file for the corresponding month is not available...")
    except:
        print("Ran into an Error...\tTry Again Later...")


def Request_Water():
    connection(x)
    demand_capacity = input("Capacity of Water Demanded: ")
    choice = pag.confirm(
        "Requested Water Capacity will be added in your Bill automatically when satisfied by administrator on restart of the software.\nDo You Want To Continue?", buttons=['Yes', 'No'])
    if choice == 'Yes':
        cursor.execute("use water_general;")
        cursor.execute(
            f"insert into req_water values('{username}',{demand_capacity}, 'P')")
        db.commit()
        print("Your Request is Submitted...")


def PROF_EDIT_REQUEST():
    connection(x)
    menu_list_header = ["S.no", "Action"]
    menu_list_content_1 = [
        ["1.", " Edit Profile Info"],
        ["2.", " Delete Profile Info"],
    ]
    menu_list_content_2 = [
        ["1.", " Edit Username"],
        ["2.", " Edit Name"],
        ["3.", " Edit Capacity"]
    ]
    print(table_creator(menu_list_content_1,
          menu_list_header, tablefmt="fancy_grid"))
    opt = int(input("Enter Your Choice: "))
    if opt == 1:
        clear_screen()
        cursor.execute("use water_general")
        print(table_creator(menu_list_content_2,
              menu_list_header, tablefmt="fancy_grid"))
        choice = int(input("Enter Your Choice: "))
        if choice == 1:
            if pag.confirm("Are you sure you want to change your username?\nIf the change is resolved then you may use your new username.", buttons=['Continue', 'Cancel']) == 'Continue':
                new_data = input("Please Enter Your New Username: ")
                print("Sending Edit Profile Request...")
                cursor.execute("use water_general")
                cursor.execute(
                    f"insert into water_general.notification(notifications) values('{username}:Edit:username-{new_data}')")
                delay(1.5)
                db.commit()
                print("Request Sent...")
                cursor.execute(
                    "select ticket_no from notification order by ticket_no desc limit 1;")
                print("Ticket No For Reference:", cursor.fetchone()[0])
        elif choice == 2:
            if pag.confirm("Are you sure you want to change your membership name?\nIf the change is resolved then you will be addressed with the new name.", buttons=['Continue', 'Cancel']) == 'Continue':
                new_data = input("Please Enter Your New Membership Name: ")
                print("Sending Edit Profile Request...")
                cursor.execute("use water_general")
                cursor.execute(
                    f"insert into water_general.notification(notifications) values('{username}:Edit:name-{new_data}')")
                delay(1.5)
                db.commit()
                print("Request Sent...")
                cursor.execute(
                    "select ticket_no from notification order by ticket_no desc limit 1;")
                print("Ticket No For Reference:", cursor.fetchone()[0])
        elif choice == 3:
            if pag.confirm("Are you sure you want to change your capacity?\nIf the change is resolved then you will sent water acoordingly", buttons=['Continue', 'Cancel']) == 'Continue':
                new_data = input("Please Enter Your New Capacity: ")
                print("Sending Edit Profile Request...")
                cursor.execute("use water_general")
                cursor.execute(
                    f"insert into water_general.notification(notifications) values('{username}:Edit:capacity-{new_data}')")
                delay(1.5)
                db.commit()
                print("Request Sent...")
                cursor.execute(
                    "select ticket_no from notification order by ticket_no desc limit 1;")
                print("Ticket No For Reference:", cursor.fetchone()[0])
        else:
            print("ERROR: Invalid Input...\tTry Again Later...")

    elif opt == 2:
        pag.confirm("Are you sure you want to delete your profile?\nIf opted for deletion your profile might not work after your request is resolved.", buttons=[
                    'Continue', 'Cancel'])
        print("Sending Delete Profile Request...")
        cursor.execute("use water_general")
        cursor.execute(
            f"insert into water_general.notification(notifications) values('{username}:Delete-Profile')")
        delay(1.5)
        db.commit()
        print("Request Sent...")
        cursor.execute(
            "select ticket_no from notification order by ticket_no desc limit 1;")
        print("Ticket No For Reference:", cursor.fetchone()[0])

    else:
        print("ERROR: Invalid Input...\tTry Again Later...")


def payment_redirect():
    # we are assuming that this function redirects the user to the payment windows
    # when the user pays it will return True,
    # so as of now True returned by default
    return True


def PAYMENT():
    bill_dat = []
    try:
        month = input("Enter month number(1-12): ")
        year = input("Enter year: ")
        flname = f"bill_{username}_{datetime.datetime.strptime(month,'%m').strftime('%B')}-{year}.csv"
        if flname in os.listdir(os.getcwd()):
            print("Bill Found for the specific month-year...")
            with open(flname) as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    bill_dat.append(row)
            if pag.confirm(f"Amount to be paid: Rs.{bill_dat[6][1]}\nDo you want to pay?", buttons=['Yes', 'No']) == "Yes":
                if payment_redirect() == True:
                    os.remove(flname)
                    print("Payment Successful...\t Bill Closed...")
        else:
            print("Bill file for the Corresponding Month is not Available...")
    except:
        print("Ran into an Eroor...\tTry Again Later...")


def menu():
    menu_list_header = ["S.no", "Action"]
    menu_list_content = [
        ["1.", " Add Water: Automated"],
        ["2.", " Request More Water"],
        ["3.", " Show Monthly Bill"],
        ["4.", " Edit Profile Details Request"],
        ["5.", " Pay Bill"],
        ["6.", " Exit"]
    ]
    print(
        f"--------------------WELCOME {name.upper()}, TO THE HOME WATER MANAGEMENT SYSTEM--------------------")
    print(table_creator(menu_list_content, menu_list_header, tablefmt="fancy_grid"))
    opt = int(input("Enter Your Choice: "))
    if opt == 1:
        clear_screen()
        print("-----Add Water: Automated-----")
        print("\n(Automate Tank Fill Activating...)")
        delay(0.7)
        Add_Water_Automated(ParentEmpty)
        Referesh(newEntryStatus)
        input("\nPress Enter to continue...")
        clear_screen()
    elif opt == 2:
        clear_screen()
        print("-----Request More Water-----")
        Request_Water()
        input("\nPress Enter To Continue...")
        clear_screen()
    elif opt == 3:
        clear_screen()
        print("-----Show Monthly Bill-----")
        SHOW_BILL()
        input("\nPress Enter To Continue...")
        clear_screen()
    elif opt == 4:
        clear_screen()
        print("-----Edit Profile Details Request-----")
        PROF_EDIT_REQUEST()
        input("\nPress Enter To Continue...")
        clear_screen()
    elif opt == 5:
        clear_screen()
        print("--------------Payment--------------")
        PAYMENT()
        input("\nPress Enter To Continue...")
        clear_screen()
    elif opt == 6:
        print("Exiting Console...")
        delay(0.7)
        db.close()
        print("Bye!")
        delay(1)
        clear_screen()
        exit()


if __name__ == '__main__':
    clear_screen()
    global x
    pag.alert("Please, Make Sure That You'Re Running The Software In Its Present Directory\nIf No You Can Not Access Certain Functionalities")
    while True:
        try:
            x = pag.password(text='Enter Your Database Access Password',
                             title="PASSWORD REQUIRED")
            if intialize(x) == True:
                while True:
                    menu()
            else:
                _opt = input("Do you want to try again(y/n): ")
                if _opt.lower() == "n":
                    print("Exiting console...")
                    delay(0.5)
                    print("Bye!")
                    delay(1)
                    clear_screen()
                    exit()

        except Exception as e:
            print("Main Func Error: " + str(e))
