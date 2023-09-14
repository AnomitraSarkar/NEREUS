'''
(IF RUNNING THE CODE RUN IT DIRECTLY IN CMD OR AS AN EXE FILE)
~ANOMITRA SARKAR
'''

# IMPORT and INSTALLATION----------------------------

import os

install = input("Do you want to install packages?(Y/N): ")
if install.upper() == "Y":
    print("installing package")
    list = ['pyautogui', 'tabulate', 'mysql-connector-python']
    for i in list:
        if os.system(f"pip install {i}"):
            print(f"RAN INTO AN ERROR...\nCOULDN'T INSTALL {i}")

# ---------------

from tabulate import tabulate as table_creator
import pyautogui as pag
from time import sleep as delay
import mysql.connector
import csv

# FUNCTIONS ----------------------------------------


def clear_screen(): return os.system("cls")


def connection(x):
    global db
    global cursor
    db = mysql.connector.connect(host="localhost", user='root', password=x)
    cursor = db.cursor()


def intialize(x):
    global username
    global name
    try:
        connection(x)
    except:
        print("Authentication Denied!")
        return False
    print('Success: Inside The Server')
    passcode = pag.password(text='Enter your Password', title='PASSWORD')
    try:
        cursor.execute('create database if not exists water_general;')
        cursor.execute('create database if not exists water_home;')
        cursor.execute('use water_general;')
        cursor.execute(
            f"SELECT USERNAME, NAME FROM WATER_GENERAL.MUNICIPAL WHERE PASSWORD = '{passcode}';")
        check_user = cursor.fetchone()
        if check_user == None:
            print("User Doesn't Exists")
        username = check_user[0]
        name = check_user[1]
        print(f"Verfied User, Hello! {name}\nUsername => {username}")
        delay(2.5)
    except Exception as e:
        print('Error: ' + str(e))
        return False
    cursor.execute(
        'create table if not exists memb(USERNAME varchar(10) not null primary key, NAME Char(30) not null, Capacity int not null);')
    cursor.execute(
        'create table if not exists municipal(USERNAME varchar(10) not null primary key, NAME varchar(30) not null, PASSWORD varchar(8) not null);')
    cursor.execute(
        'create table if not exists req_water(REQ_USERNAME varchar(10) not null primary key, REQ_WATER int not null, STATUS char(1) not null);')
    cursor.execute(
        'create table if not exists notification(TICKET_NO int not null auto_increment primary key, NOTIFICATIONS text not null);')
    db.commit()
    print("Necessary Tables Made...\n")
    delay(2.5)
    clear_screen()
    return True


def Access_Profile_Settings():
    menu_list_header = ["S.no", "Action"]
    menu_list_content_1 = [
                          ["1.", " Show Info"],
                          ["2.", " Add Info"],
                          ["3.", " Edit Info"],
                          ["4.", " Delete Info"]
    ]
    print(table_creator(menu_list_content_1,
          menu_list_header, tablefmt="fancy_grid"))
    opt = int(input("Enter Your Choice: "))
    if opt == 1:
        l1 = [["1.", " Show All Data"],
              ["2.", " Show Particular Data"], ]
        print(table_creator(l1, menu_list_header, tablefmt="fancy_grid"))
        choice = int(input("What will you like to do? : "))
        if choice == 1:
            Cumilated_basic_action(
                'show_all', 'municipal', '*', ['Username', 'Name', 'Password'])
        elif choice == 2:
            pointer = input("Enter the username of the member you seek: ")
            Cumilated_basic_action(
                'show_only', 'municipal', "*", ['Username', 'Name', 'Password'], where=pointer)
        else:
            print("ERROR: Invalid Input...\tTry Again Later...")

    elif opt == 2:
        n_user = input("Enter the new username(10 chr): ")
        n_name = input("Enter the new name(30 chr): ")
        n_pass = input("Enter the new password(8 chr): ")
        query = [f"'{n_user}'", f"'{n_name}'", f"'{n_pass}'"]
        Cumilated_basic_action("add", 'municipal', query, [
                               'Username', 'Name', 'Password'])

    elif opt == 3:
        pointer = input("Enter the username of the edited: ")
        l2 = [
            ["1.", " Edit Username "],
            ["2.", " Edit Name "],
            ["3.", " Edit Password "]
        ]
        print(table_creator(l2, menu_list_header, tablefmt="fancy_grid"))
        choice = int(input("What will you like to edit? : "))
        if choice == 1:
            _header = "Username"
            _query = input("Edited value: ")
            Cumilated_basic_action("edit", "municipal",
                                   f"'{_query}'", _header, pointer)
        elif choice == 2:
            _header = "Name"
            _query = input("Edited value: ")
            Cumilated_basic_action("edit", "municipal",
                                   f"'{_query}'", _header, pointer)
        elif choice == 3:
            _header = "Password"
            _query = input("Edited value: ")
            Cumilated_basic_action("edit", "municipal",
                                   f"'{_query}'", _header, pointer)
        else:
            print("ERROR: Invalid Input...\tTry Again Later...")

    elif opt == 4:
        pointer = input("Enter the username of the deleted: ")
        Cumilated_basic_action('delete', 'municipal',
                               None, None, where=pointer)
    else:
        print("ERROR: Invalid Input...\tTry Again Later...")


def Members_Profile_Settings():
    menu_list_header = ["S.no", "Action"]
    menu_list_content_1 = [
                          ["1.", " Show Info"],
                          ["2.", " Add Info"],
                          ["3.", " Edit Info"],
                          ["4.", " Delete Info"]
    ]
    print(table_creator(menu_list_content_1,
          menu_list_header, tablefmt="fancy_grid"))
    opt = int(input("Enter Your Choice: "))
    if opt == 1:
        l1 = [["1.", " Show All Data"],
              ["2.", " Show Particular Data"], ]
        print(table_creator(l1, menu_list_header, tablefmt="fancy_grid"))
        choice = int(input("What will you like to do? : "))
        if choice == 1:
            Cumilated_basic_action(
                'show_all', 'memb', '*', ['Username', 'Name', 'Capacity'])
        elif choice == 2:
            pointer = input("Enter the username of the member you seek: ")
            Cumilated_basic_action(
                'show_only', 'memb', "*", ['Username', 'Name', 'Capacity'], where=pointer)
        else:
            print("ERROR: Invalid Input...\tTry Again Later...")

    elif opt == 2:
        n_user = input("Enter the new username(10 chr): ")
        n_name = input("Enter the new name(30 chr): ")
        n_cap = input("Enter the new capacity(8 chr): ")
        query = [f"'{n_user}'", f"'{n_name}'", n_cap]
        Cumilated_basic_action("add", 'memb', query, [
                               'Username', 'Name', 'Capacity'])
    elif opt == 3:
        pointer = input("Enter the username of the edited: ")
        l2 = [
            ["1.", " Edit Username "],
            ["2.", " Edit Name "],
            ["3.", " Edit Capacity "]
        ]
        print(table_creator(l2, menu_list_header, tablefmt="fancy_grid"))
        choice = int(input("What will you like to edit? : "))
        if choice == 1:
            _header = "Username"
            _query = input("Edited value: ")
            Cumilated_basic_action(
                "edit", "memb", f"'{_query}'", _header, pointer)
        elif choice == 2:
            _header = "Name"
            _query = input("Edited value: ")
            Cumilated_basic_action(
                "edit", "memb", f"'{_query}'", _header, pointer)
        elif choice == 3:
            _header = "Capacity"
            _query = input("Edited value: ")
            Cumilated_basic_action("edit", "memb", _query, _header, pointer)
        else:
            print("ERROR: Invalid Input...\tTry Again Later...")

    elif opt == 4:
        pointer = input("Enter the username of the deleted: ")
        Cumilated_basic_action('delete', 'memb', None, None, where=pointer)
    else:
        print("ERROR: Invalid Input...\tTry Again Later...")


def Requestors_Profile_Settings():
    print('The Pending Requestor Porfiles: ')
    delay(1.5)
    Cumilated_basic_action('show_only', 'req_water', '*', [
                           'Requestor', 'Requested Capacity', 'Status'], where='P', where_pointer='Status')
    opt = input("Do yo want to change status to Done for all profiles?(Y/N)")
    if opt.upper() == 'Y':
        print("Converting all pending requests...")
        Cumilated_basic_action('edit', 'req_water', "'D'",
                               'Status', where='P', where_pointer='Status')


def Cumilated_basic_action(action, tablename, query, header, where=False, dbase="water_general", where_pointer='username'):
    connection(x)
    if action == "show_all":
        record = []
        cursor.execute(f"select {query} from {dbase}.{tablename};")
        for i in cursor:
            record.append(i)
        clear_screen()
        print(table_creator(record, header, tablefmt="fancy_grid"))
    elif action == "show_only":
        record = []
        cursor.execute(
            f"select {query} from {dbase}.{tablename} where {where_pointer} = '{where}';")
        for i in cursor:
            record.append(i)
        clear_screen()
        print(table_creator(record, header, tablefmt="fancy_grid"))
    elif action == "add":
        cursor.execute(
            f"insert into {dbase}.{tablename}({header[0]},{header[1]},{header[2]}) values({query[0]},{query[1]},{query[2]});")
        print("Making Changes...")
        db.commit()
        print("Success...")
    elif action == "delete":
        cursor.execute(
            f"delete from {dbase}.{tablename} where {where_pointer} = '{where}'")
        print("Making Changes...")
        db.commit()
        print("Success...")
    elif action == 'edit':
        cursor.execute(
            f"update {dbase}.{tablename} set {header} = {query} where {where_pointer} = '{where}'")
        print("Making Changes...")
        db.commit()
        print("Success...")
    else:
        print('Resultant Query Not Found')


def Notifications_Settings():
    connection(x)
    menu_list_header = ["S.no", "Action"]
    menu_list_content_1 = [
                          ["1.", " Read Top 5 Latest Notifications "],
                          ["2.", " Resolve Top 5 Latest Notifications"],
        #   ["3.", " Automate Notifications"],
    ]
    print(table_creator(menu_list_content_1,
          menu_list_header, tablefmt="fancy_grid"))
    opt = int(input("Enter Your Choice: "))
    if opt == 1:
        clear_screen()
        rec = []
        cursor.execute(
            "select * from water_general.notification order by ticket_no desc limit 5;")
        try:
            for i in cursor:
                rec.append(i)
            print(table_creator(
                rec, ['TICKET_NO', 'NOTIFICATIONS'], tablefmt="fancy_grid"))
        except:
            pass
    elif opt == 2:
        cursor.execute(
            "select ticket_no from water_general.notification order by ticket_no desc limit 1;")
        upper_limit = cursor.fetchone()[0]
        cursor.execute(
            f"delete from water_general.notification where ticket_no <= {upper_limit} and ticket_no >= {upper_limit-4}")
        db.commit()
        print('Resolved...')
    else:
        print("ERROR: Invalid Input...\tTry Again Later...")


def Backup_Settings():
    menu_list_header = ["S.no", "Action"]
    menu_list_content_1 = [
                          ["1.", " Save to Backup"],
                          ["2.", " Update from Backup"]
    ]
    print(table_creator(menu_list_content_1,
          menu_list_header, tablefmt="fancy_grid"))
    opt = int(input("Enter Your Choice: "))
    try:
        if opt == 1:
            saveToBackup()
        elif opt == 2:
            updateFromBackup()
    except:
        print('Ran Into An Error...\nCheck your Backup and Current Data for Anomalies.')


def saveToBackup():
    pag.alert("This operation will store the backup only for access, members and requestors profiles. Notifications will not be saved.")
    f_muncipal = open("backup_municipal.csv", "w", newline='')
    f_memb = open("backup_memb.csv", "w", newline='')
    f_req_water = open("backup_req_water.csv", "w", newline='')
    csv_writer_municipal = csv.writer(f_muncipal)
    csv_writer_memb = csv.writer(f_memb)
    csv_writer_req_water = csv.writer(f_req_water)
    csv_writer_municipal.writerows(converted_data("water_general.municipal"))
    csv_writer_memb.writerows(converted_data("water_general.memb"))
    csv_writer_req_water.writerows(converted_data("water_general.req_water"))
    f_muncipal.close()
    f_memb.close()
    f_req_water.close()
    print("Data Processing Completed...")
    print("Backup saved in the same folder as root folder of the softwarem with name: \n'" +
          f_req_water.name+"' and \n'"+f_memb.name+"' and \n'" + f_muncipal.name+"'.")


def converted_data(table_name):
    list = []
    cursor.execute(f"select * from {table_name};")
    for row in cursor:
        rec = []
        for i in row:
            rec.append(i)
        list.append(rec)
    return list


def updateFromBackup():
    warning = "You're system might already have some data in your database\nUsing the backup option will delete the existing data and replace the data with the new backup data\nDo you still want to continue?"
    pag.alert(
        "Make sure that the Backup files are in the same directory as the software's")

    opt = pag.confirm(warning, buttons=['Yes', 'No'])
    if opt == 'Yes':
        print("Loading Backup...")
        for i in ('municipal', 'memb', 'req_Water'):
            cursor.execute(f"drop table water_general.{i};")
        cursor.execute(
            "create table water_general.Memb(UserName varchar(10) primary key, Name char(30) not null, Capacity int not null);")
        cursor.execute(
            "create table water_general.Req_Water(Req_UserName varchar(10), Req_Water int, Status char(1));")
        cursor.execute(
            "create table water_general.Municipal(Username varchar(10) primary key, Name char(30) not null, Password varchar(8) not null);")
        backup_municipal_data = DataListConverter("backup_municipal.csv")
        backup_memb_data = DataListConverter("backup_memb.csv")
        backup_req_water_data = DataListConverter("backup_req_water.csv")
        print("Loaded Backup...\nWriting Backup Data...")
        for row in backup_municipal_data:
            cursor.execute(
                f"insert into water_general.municipal(Username, name, password) values('{row[0]}', '{row[1]}', '{row[2]}');")
        for row in backup_memb_data:
            cursor.execute(
                f"insert into water_general.memb(Username, name, capacity) values('{row[0]}', '{row[1]}', {row[2]});")
        for row in backup_req_water_data:
            cursor.execute(
                f"insert into water_general.req_water(Req_Username, Req_water, status) values('{row[0]}', {row[1]}, '{row[2]}');")
        db.commit()
        print("Successful...")
        return 1
    else:
        return 0


def DataListConverter(filename):
    allrec = []
    f = open(filename, 'r')
    csv_reader = csv.reader(f)
    for row in csv_reader:
        allrec.append(row)
    return allrec


def menu():
    menu_list_header = ["S.no", "Action"]
    menu_list_content = [
        ["1.", " Access Profile Settings"],
        ["2.", " Members Profile Settings"],
        ["3.", " Requestors Profile Settings"],
        ["4.", " Notifications Settings"],
        ["5.", " Backup Settings"],
        ["6.", " Exit"]
    ]
    print(
        f"--------------------WELCOME {name}, TO THE HOME WATER MANAGEMENT SYSTEM--------------------")
    print(table_creator(menu_list_content, menu_list_header, tablefmt="fancy_grid"))
    opt = int(input("Enter Your Choice: "))
    if opt == 1:
        clear_screen()
        print("-----Access Profile Settings-----")
        Access_Profile_Settings()
        input("\nPress Enter to continue...")
        clear_screen()
    elif opt == 2:
        clear_screen()
        print("-----Members Profile Settings-----")
        Members_Profile_Settings()
        input("\nPress Enter to continue...")
        clear_screen()
    elif opt == 3:
        clear_screen()
        print("-----Requestors Profile Settings-----")
        Requestors_Profile_Settings()
        input("\nPress Enter to continue...")
        clear_screen()
    elif opt == 4:
        clear_screen()
        print("-----Notifications Settings-----")
        Notifications_Settings()
        input("\nPress Enter to continue...")
        clear_screen()
    elif opt == 5:
        clear_screen()
        print("-----Backup Settings-----")
        Backup_Settings()
        input("\nPress Enter to continue...")
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
    while True:
        try:
            x = pag.password(
                text='Enter Your Database Access Passcode', title='PASSWORD REQUIRED')
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
