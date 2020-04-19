import psycopg2
import sys
from psycopg2.extensions import AsIs
class Connection:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = "5432"
        self.database = "postgres"

    #Login/out function calls
    def loginIn(self,usrName,Pasword):
        try:
            conn = psycopg2.connect(user = usrName,
                                    password = Pasword,
                                    host = self.host,
                                    port = self.port,
                                    database = self.database)
            print("after connecting")
            return conn
        except(Exception, psycopg2.Error) as error:
            print ("Error while connecting to PostgreSQL", error)
            return
    
    def loginOut(self,conn):
        conn.close()
        print("PostgeSQL connection is closed")
        return


    #User function calls- changed recursive calls
    def newUser(self,conn):
        myCursor = conn.cursor()
        invalid=True
        while(invalid):
            usrName = input("Enter a username: ")
            Pasword = input("Enter a password: ")
            confPassword = input("Confirm the password: ")
            if Pasword == confPassword:
                try:
                    myCursor.execute("Create user %s with password %s", (AsIs(usrName),Pasword))
                    userType = input("What type user is this user: ")
                    myCursor.execute("Grant %s privileges on database %s to %s", (userType,self.database,usrName))
                    print("New User has been added")
                    invalid=False
                except(Exception,psycopg2.Error) as error:
                    if error == 42710: #User does not exist 
                        print("User already exist, try a new username")
                    else:
                        print("Error %d occured", error)

            else:
                print("Passwords do not match, please try again")
        return

    def updateUser(self,conn): #updated so no recursive calls
        myCursor = conn.cursor()
        usrName = input("Enter a username you want to update: ")
        newPasword = input("Enter a password: ")
        confnewPassword = input("Confirm the password")
        invalid=True
        if newPasword == confnewPassword:
            while(invalid):
                try:
                    myCursor.execute("Alter user %s with password %s", (usrName,newPasword))
                    userType = input("What type of user is this user: ")
                    myCursor.execute("Grant %s privileges on database %s to %s", (userType,self.database,usrName))
                    print("New User has been added")
                    invalid=False
                except(Exception,psycopg2.Error) as error:
                    if error == 42704:
                        print("User does not exit")
                    else:
                        print("Error %d occured", error)
                    return -1    
        else:
            print("Password did not match")
        return

    #Customers function calls
    def newCustomer(self,conn):
        myCursor = conn.cursor()
        fn = input("Enter First Name: ")
        ln = input("Enter Last Name: ")
        myCursor.execute("Insert into Customer (customerid,firstname,lastname) values (%s,%s)", (fn,ln,))
        return
    def updateCustomer(self,conn):
        myCursor = conn.cursor()
        return
    def viewCustomers(self,conn):
        myCursor = conn.cursor()
        return

    #Model function calls
    def newModel(self,modelNumber,itemCost,orderNumber,conn):
        myCursor = conn.cursor()
        return
    def updateModel(self,conn): 
        myCursor = conn.cursor()
        return

    #Design function calls- verify why the double employee id check
    def newDesign(self,employeeID,conn):
        myCursor = conn.cursor()
        checkempID = myCursor.execute("Select employeeId from employee where employeeId='%s'", employeeID)
        employeeID = input("Enter your employee ID: ")
        invalid=True
        if employeeID == checkempID:
            while(invalid):
                modelNumber = input("Enter the new model number: ")
                try:
                    myCursor.execute("Select modelNumber from model where modelNumber=%s", modelNumber)#should throw an error

                    print("Please try another model number") 

                except(Exception, psycopg2.Error) as error:
                    if error == '02':
                        itemCost = input("Enter the items cost: ")
                        myCursor.execute("Insert into model (employeeif,costnumber,modelcost) values (%s,%s,%s)", (employeeID,modelNumber,itemCost))
                        invalid=False
                        return
        else:
            print("Invalid Employee id")#check what this might be for

    #Employee function calls
    def newEmployee(self,conn):
        myCursor = conn.cursor()
        employeeid = input("Enter the Employees ID: ")
        firstname = input("Enter the Employees first mame: ")
        lastname = input("Enter the Employees last name: ")
        ssn = input("Enter the Employees ssn: ")
        paytype = input("Enter the Employees paytype: ")
        jobtype = input("Enter the Employees job type: ")
        myCursor.execute("Insert into Employee (employeeid,firstname,lastname,ssn,paytype,jobtype) values (%s,%s,%s,%s,%s,%s)", (employeeid,firstname,lastname,ssn,paytype,jobtype))
        return

    def employeeInfo(self,conn): #Engineers have limited view of emplyee info like name, title, etc.
        myCursor = conn.cursor()
        return

    def updateEmployee(self,conn):
        myCursor = conn.cursor()


    #Report function calls
    def createReport(self,conn):
        myCursor = conn.cursor()
        return
    def viewReport(self,conn):
        myCursor = conn.cursor()
        return
    
    #Inventory function calls
    #there is newModel() no need for addModel()
    def deleteModel(self,conn):
        myCursor = conn.cursor()
        return
    def viewInventory(self,conn):
        myCursor = conn.cursor()
        return

    #Order function calls
    def createOrder(self,conn):
        myCursor = conn.cursor()
        return
    def updateOrder(self,conn):
        myCursor = conn.cursor()
        return
    def viewOrders(self,conn):
        myCursor = conn.cursor()
        return


    def newTable(self,conn):
        myCursor = conn.cursor()
        return
    def updateTable(self,conn):
        myCursor = conn.cursor()
        return
