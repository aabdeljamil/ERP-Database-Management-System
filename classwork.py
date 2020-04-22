import psycopg2
import psycopg2.sql
import sys
from psycopg2.extensions import AsIs
from psycopg2 import sql

class Connection:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = "8080"
        self.database = "postgres"
        self.cIdCounter = 0
        self.iIdcounter = 0

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
            Password = input("Enter a password: ")
            confPassword = input("Confirm the password: ")
            if Pasword == confPassword:
                try:
                    #manually scrub username for errors- special case
                    myCursor.execute("Create user %s with password %s", (AsIs(usrName),Password, )) #(AsIs(usrName), Pasword, ))
                    userType = input("What type user is this user: ")
                    myCursor.execute("Grant %s to %s", (AsIs(userType),AsIs(usrName)))
                    print("New User has been added")
                    invalid=False
                except(Exception,psycopg2.Error) as error:
                    if error == 42710: #User does not exist 
                        print("User already exist, try a new username")
                    else:
                        print("Error : ", str(error))

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
    #Abdallah
    def customerIdCounter(self):
        rtrn = self.cIdCounter + 1
        self.cIdCounter += 1
        return rtrn
    def newCustomer(self,conn):
        myCursor = conn.cursor()
        fName = input("Enter First Name: ")
        lName = input("\nEnter Last Name: ")
        myCursor.execute("select * from customer where firstName = %s and lastName = %s", (fName, lName))
        duplicateName = myCursor.fetchall() #if this list is empty then the customer has not been added yet
        if duplicateName:
            ques = input("Customer with that name already exists. Is this a different customer with the same name? (Y/N)")
            if ques == "Y":
                cId = customerIdCounter() 
                myCursor.execute("Insert into Customer (customerid,firstname,lastname) values (%s,%s)", (cId, fName,lName))
        else:
            cId = customerIdCounter() 
            myCursor.execute("Insert into Customer (customerid,firstname,lastname) values (%s,%s)", (cId, fName,lName))
    def updateCustomer(self,conn):
        myCursor = conn.cursor()
        invalid = True
        tryAgain = "Y"
        while invalid == True and tryAgain == "Y":
            confirmCId = input("Please enter the ID of the customer you want to update: ")
            myCursor.execute("select * from Customer where customerId = %s", (confirmCId))
            idExists = myCursor.fetchall() #list of that customerId, should not be empty
            if idExists:
                invalid = False
            else:
                tryAgain = input("Customer ID does not exist. Would you like to try another ID? (Y/N)")
                if tryAgain != "Y":
                    return
        fName = input("\nEnter new First Name: ")
        lName = input("\nEnter new Last Name: ")
        myCursor.execute("update Customer set firstName = %s, lastName = %s where customerId = %s", (fName, lName, confirmCId))
    def viewCustomers(self,conn):
        print("Customer ID\tFirst Name\tLast Name")
        myCursor = conn.cursor()
        myCursor.execute("select * from Customer")
        allCust = myCursor.fetchall()
        for i in range(len(all)):
            print(allCust[i][0], "\t\t", allCust[i][1], "\t\t", allCust[i][2])

    #Model function calls
    #Abdallah
    def inventoryIdCounter(self):
        rtrn = self.iIdcounter + 1
        self.iIdcounter += 1
        return rtrn
    def newModel(self,conn):
        myCursor = conn.cursor()
        invalid = True
        tryAgain = "Y"
        while invalid == True and tryAgain == "Y":
            dsnNmbr = input("Please enter the design ID of the design that you would like to make a model and add to the inventory: ")
            myCursor.execute("select designid from design where designid = %s", (dsnNmbr))
            doesExist = myCursor.fetchall()
            if doesExist:
                invalid = False
            else:
                ques = input("Invalid model number. Would you like to try another model number? (Y/N)")
                if ques != "Y":
                    return
        name = input("Please enter a name for this model: ")
        cost = input("Please enter how much it cost for this model to be manufactured: ")
        price = input("Please enter a price for this model: ")
        time = input("Please enter how long it took to manufacturer this model: ")
        category = input("Please enter a category for this model: ")
        quantity = input("Please enter a quantity for this model: ")
        invId = inventoryIdCounter()
        myCursor.execute("insert into Model (modelname, costmodel, designid, leadtime) values (%s, %s, %s, %s)", 
                        (name, cost, doesExist[0], time))
        myCursor.execute("insert into inventory (inventoryId, saleprice, category, modelname, quantity) values \
                        (%s, %s, %s %s, %s)", (invId, price, category, name, quantity))
    def updateModel(self,conn): 
        myCursor = conn.cursor()
        return

    #Design function calls- verify why the double employee id check
    def newDesign(self,conn):
        myCursor = conn.cursor()
        employeeID = input("Enter your employee ID: ")
        myCursor.execute("Select employeeId from employee where employeeId='%s'", employeeID)
        checkempID = myCursor.fetchall()
        invalid=True
        if employeeID == checkempID[0]:
            while(invalid):
                modelNumber = input("Enter the new model number: ")
                try:
                    myCursor.execute("Select modelNumber from model where modelNumber=%s", modelNumber)#should throw an error

                    print("Please try another model number") 

                except(Exception, psycopg2.Error) as error:
                    if error == '02':
                        itemCost = input("Enter the items cost: ")
<<<<<<< HEAD
                        myCursor.execute("Insert into model (employeeid,modelnumber,costitem) values (%s,%s,%s)", (employeeID,modelNumber,itemCost))
                        myCursor.execute("Insert into design () values ()")
=======
                        myCursor.execute("Insert into model (employeeid,costnumber,modelcost) values (%s,%s,%s)", (employeeID,modelNumber,itemCost))
>>>>>>> f506f765a0dbff78fe96a85c13f81227abc2bc76
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

    #Przmek
    #Report function calls
    def createReport(self,conn):
        myCursor = conn.cursor()
        return
    def viewReport(self,conn):
        myCursor = conn.cursor()
        return
    def newTable(self,conn):
        myCursor = conn.cursor()
        return
    def updateTable(self,conn):
        myCursor = conn.cursor()
        return
    #Part of Employee Function Calls
    def updateEmployee(self,conn):
        myCursor = conn.cursor()

    #Andrew
    #Inventory function calls
    #there is newModel() no need for addModel()
    def deleteModel(self,conn):
        invalid = True
        while(invalid):
            try:
                myCursor = conn.cursor()
                delModel = input("What model would you like to delete: ")
                modelNum = input("What is the model number you would like to delete: ")
                myCursor.execute("delete from model where modelnumber=%s and modelname=%s", (delModel,modelNum))
                print("Model has been created")
                invalid = False
            except(Exception, psycopg2.Error) as error:
                        if error == 42704:
                            print("Error occured",error)
                            invalid = True
        return
                            

    def viewInventory(self,conn): #Abdallah
        print("Inventory ID\tSale Price\tCategory\tModel Name\tQuantity")
        myCursor = conn.cursor()
        myCursor.execute("select * from Inventory")
        allInv = myCursor.fetchall()
        for i in range(len(all)):
            print(allInv[i][0], "\t\t", allInv[i][1], "\t\t", allInv[i][2], "\t\t", allInv[i][3], "\t\t", allInv[i][4])

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
    #Part of Employee Function calls
    def employeeInfo(self,conn): #Engineers have limited view of emplyee info like name, title, etc.
        myCursor = conn.cursor()
        return
    