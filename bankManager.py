import mysql.connector as ms
import random
import time

db = ms.connect(host='localhost', user='root', passwd='yourpass', database='yourdatabase')
myc = db.cursor()


def choice():
    print("1. Create account")
    print("2. Login")
    inputChoice = int(input("Enter your choice: "))
    if (inputChoice == 1):
        SignUp()
    elif (inputChoice == 2):
        Login()
    else:
        choice()


def SignUp():
    print("\n" * 20)
    userName = input("Enter User Name to Sign Up: ")
    myc.execute("select Name from account where Name='{Name}'".format(Name=userName))
    tmp1 = myc.fetchall()
    ac = random.randint(10000, 99999)

    if (tmp1 == []):
        password = input("Enter Password for your account: ")
        upi_id = input("Enter upi ID for your account: ")    #upi exists?
        upi_pass = input("Enter upi password for your account: ")
        sql = "insert into account values('{}','{}',{},'{}',{},{})".format(userName, password, ac, upi_id, 0, upi_pass)
        myc.execute(sql)
        db.commit()

        print("\n(+_+) Your account has been created")
        Login()
    else:
        print("\nOops!Seems a account already exists with this name.Please try with different name")


def Login():
    print("\n" * 20)
    userName = input("Enter User Name: ")
    com = "select Name from account where Name='{Name}'".format(Name=userName)
    myc.execute(com)
    tmp1 = myc.fetchall()

    if (tmp1 != []):
        password = input("Enter Password: ")
        com = "select Password from account where Name='{Name}'".format(Name=userName)
        myc.execute(com)
        tmp2 = myc.fetchall()
        # print(tmp2)
        for i in tmp2:
            if (i[0] == password):
                DashBoard(userName)
            else:
                print("password incorrect")
    else:
        print("Account not found")


def DashBoard(user):
    print("\n" * 20)
    print("\nHi,", user)
    print("\t1. Send\n\t2. Request from others\n\t3. Accept Request\n\t4. Mini Statement of Credits")
    myc.execute("select Balance,upi from account where Name='{Name}'".format(Name=user))
    inData=myc.fetchall()
    print("\tBalance:",inData[0][0],"\n\tUPI: ",inData[0][1]+"\n")
    myc.execute("select * from pending where Requested='{upi}' and status='{status}'".format(upi=inData[0][1],status="Pending"))
    requestData = myc.fetchall()
    #print("\tRequests\n\t"+"Requested from: "+requestData[0][2]+"for"+requestData[0][3])
    for i in range(len(requestData)):
        print("\t"+str(i+1)+")Requested from: " + requestData[i][2] , "for" , requestData[i][3])
    choice = int(input("\n\tEnter your choice: "))
    if (choice == 1):
        toSend = input("\tEnter UPI ID of receiver: ")  # validate id
        amount = int(input("\tEnter amount to send: "))
        type="Direct"
        Send(user, inData[0][0],inData[0][1],toSend,amount,type,amount)
    if (choice == 2):
        Request(user,inData[0][1])
    if(choice == 3):
        sendTo=int(input("\tEnter no to send: "))
        type2 ="Requested"
        if sendTo<=len(requestData):
            Send(user, inData[0][0], inData[0][1], requestData[sendTo - 1][2], requestData[sendTo - 1][3], type2,
                 requestData[sendTo - 1][0])
        else:
            print("\tYou request seems to be wrong")
    if(choice == 4):
        myc.execute("select * from transactions where Sender='{upi}'".format(upi=inData[0][1]))
        tranData = myc.fetchall()
        for i in range(len(tranData)):
            print("\t"+str(i+1)+")Paid to "+tranData[i][2],"Rs."+str(tranData[i][5])+". Closing balance:",tranData[i][3])

def Send(user,balance,userUpi,toSend,amount,type,trNo):
    if amount <= balance:
        myc.execute("select Balance from account where upi='{upi}'".format(upi=toSend))
        rB = myc.fetchall()
        sTmp = balance - amount
        rTmp = rB[0][0] + amount
        myc.execute("select TranNo from transactions")
        totalTrans = myc.fetchall()
        myc.execute("update account set Balance={value} where Name='{Name}'".format(value=sTmp, Name=user))
        db.commit()
        myc.execute("update account set Balance={value} where upi='{upi}'".format(value=rTmp, upi=toSend))
        db.commit()
        sql = "insert into transactions values({},'{}','{}',{},{},{},'{}')".format(len(totalTrans) + 1, userUpi, toSend,
                                                                                sTmp, rTmp,amount, type)
        myc.execute(sql)
        db.commit()
        if (type=="Requested"):
            myc.execute("update pending set status='{status}' where No={no}".format(status="Sent",no=trNo))
            db.commit()
            print(f'\tRequested money Rs.{amount} sent successfully')
        else:
            print(f'\tPayment Successful! Rs.{amount} has been sent to {toSend}')
            DashBoard(user)
    else:
        print("No enough balance")
        DashBoard()

def Request(user,userUpi):
    toRequest=input("\tEnter UPI ID to request: ")
    amount=int(input("\tEnter amount to request: "))
    myc.execute("select No from pending")
    totalTrans = myc.fetchall()
    sql = "insert into pending values({},'{}','{}',{},'{}')".format(len(totalTrans) + 1, toRequest, userUpi, amount,"Pending")
    myc.execute(sql)
    db.commit()
    print("\tAmount request successful")
    DashBoard(user)
choice()
