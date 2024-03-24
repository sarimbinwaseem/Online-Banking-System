import json
import random
import time
from abc import ABC, abstractmethod

data = {}  # contains account number
data_value = {}  # contains username password balance etc passed as a value to data{}
track = {}  # has another dictionary passed to d containing time/date etc. key: date, value: day
deposit = {} #contains all deposit history

#FileMaking: This class is responsible for loading and dumping data to a JSON file (my_history.json).
# It has methods load_file() to load the data from the file and dump_file() to save the data back to the file.
class FileMaking: #FILING FUNCTIONS
    def __init__(self):
        self.content = {}

    def load_file(self):
        try:
            with open('my_history.json', 'r') as f:
                self.content = json.load(f)
        except FileNotFoundError:
            print("File not found.")
            self.content = None
        except PermissionError:
            print("Permission denied.")
            self.content = None

    def dump_file(self):
        with open('my_history.json', 'w') as f:
            json.dump(self.content, f)

#DataHandling: This class extends FileMaking and provides methods for searching and retrieving customer account data from the loaded file.
# It also has a method customer_history() to display the transaction history of a customer.
class DataHandling(FileMaking):
    def __init__(self):
        super().__init__()

    def __getitem__(self, key):
        return self.content[key]

    def search(self, acc_num): #returns bank account number after searching in the content
        if acc_num in self.content:
            self.value = self.content[acc_num]
            return self.value
        else:
            return None

    def customer_history(self, account): #prints a customer's details
        self.load_file()
        info = self.search(account)
        try:
            print("==================================")
            print(f" CUSTOMER: {info['name'][0]} {info['name'][1]}")
            print("==================================")
            time.sleep(1)
            print(f"YOUR ACCOUNT TYPE:{info['account type']}")
            print(f"YOUR CURRENT BALANCE:{info['balance']}\n")
            time.sleep(1)
            print("**********************")
            print("TRANSACTION HISTORY:")
            print("**********************")
            time.sleep(1)
            for key, value in info["track"].items():
                print("-------------------------", end="")
                print(f"""\nDATE: {key} 
    -------------------------
    Withdrawn: {value}""")
            print("\nX:X:X:X:X:X:X:X:X:X:X:X:X:X")

            for key, value in info["deposit"].items():
                print("-------------------------")
                print(f"""\nDATE: {key} 
    -------------------------
    Deposited: {value}""")

            if info['account type'] == 'Checking Account':
                time.sleep(1)
                print(f"\n==============================================")
                print(f" HAVE TO RETURN AMOUNT: {info['returning amount']}")
                print(f"=================================================")

            elif info['account type'] == 'Loan Account':
                time.sleep(1)
                print(f"\n==============================================")
                print(f" HAVE TO RETURN AMOUNT: {info['loan']}")
                print(f"=================================================\n")
        except:
            print("\n-----------------------------")
            print("INVALID ACCOUNT NUMBER")
            print("--------------------------------")
            time.sleep(1)
            a=input("ENTER YOUR ACCOUNT NUMBER: ")
            print("")
            self.customer_history(a)

#Account (abstract class): This is an abstract base class that defines common attributes and methods for different types of bank accounts.
# It has methods for depositing, withdrawing, and checking the balance of an account.
# The withdraw() method is defined as an abstract method, which needs to be implemented in the derived classes.

class Account(ABC): #abstract class having all basic methods required for sub-classes
    def __init__(self, instance, account_number, balance=0):
        self.instance = instance  # object passed
        self.accountNumber = account_number
        self.balance = balance

    def deposit(self): #deposits amount
        while True:
            try:
                self.dep = float(input('Enter the amount which u want to deposit:'))
                if self.dep >= 0:
                    self.balance += self.dep
                    existing_transactions = self.instance.content[self.accountNumber]['deposit']
                    existing_transactions[self.curr_date] = self.dep
                    self.instance.content[self.accountNumber]['deposit'] = existing_transactions
                    break
                else:
                    print('Invalid deposit')
            except ValueError:
                print('Invalid input. Please enter a valid amount.')

    @abstractmethod
    def withdraw(self):
        pass

    def balance_enquiry(self):
        data_value.update({'balance': self.balance})
        return self.balance

    def current_time(self): #takes date as an input and checks it for being out of range
        while True:
            try:
                self.curr_date = input('Enter the current date in (YYYY MM DD) format: ')
                print("---------------------------------------------------")
                a = self.curr_date.split()
                b = []
                for i in a:
                    b.append(int(i))
                if b[0] < 2023 or 12 < b[1] or b[1] <= 0 or 31 < b[2] or b[2] < 1:  # FOR PRINTING WITH IN RANGE
                    raise ValueError
                else:
                    break

            except ValueError:
                print('Invalid input. Please enter a valid date.')

    def time_management(self, months=0): #checks if it has been a month
        self.months = months
        year, month, day = map(int, self.curr_date.split())

        extract = DataHandling()
        extract.load_file()  # loads file into self.content
        find = self.instance.content[self.accountNumber]['track']  # track is a key here

        last_element = list(find.items())[-1]
        last_key = last_element[0]  # ????
        self.last_date = last_key

        l_year, l_month, l_day = map(int, self.last_date.split())
        self.duration = ((year * 365) + (month * 30) + day) - ((l_year * 365) + (l_month * 30) + l_day)
        if self.duration > 30:
            while True:
                self.duration -= 30
                self.months += 1
                if self.duration < 30:
                    break
        else:
            print('Your duration is less than a month')

#CheckingAccount, SavingsAccount, and LoanAccount: These classes inherit from the Account class and implement the withdraw() method based on the specific rules for each account type.
# They also have additional methods for account creation and handling specific account operations.

class CheckingAccount(Account): #child class of account
    def __init__(self, credit_limit, instance, account_number):  # c=5000
        super().__init__(instance, account_number, balance=0)
        self.creditLimit = credit_limit  # per day
        data_value.update({'account type': 'Checking Account'})

    def previous(self): #gets balance
        self.balance = self.instance.content[self.accountNumber]['balance']
        Account.deposit(self)

    def acc_created(self): #stores the account creation date
        Account.current_time(self)
        track.update({self.curr_date: 'none, ACCOUNT CREATED'})

    def withdraw(self):  # ir=0.1 (10%) works based on of withdrawal policy
        self.interest_rate = 0.1
        self.balance = self.instance.content[self.accountNumber]['balance']
        self.returning_amount = self.instance.content[self.accountNumber]['returning amount']

        while True:
            try:
                self.cash_out = float(input('Enter the withdraw amount: '))
                if self.cash_out<0:
                    raise ValueError
                elif self.cash_out > self.balance:
                    extra = self.cash_out - self.balance    # to check extra money cashed out

                    if extra > self.creditLimit:
                        print("\n======================================")
                        print('You have exceeded your credit limit')
                        print("=======================================\n")
                        time.sleep(1)
                        self.balance = 0
                        self.exceed = extra - self.creditLimit   # credit limit exceeded or not
                        interest_rate = self.exceed * self.interest_rate
                        returns = extra + interest_rate
                        self.returning_amount += returns
                        print("\n========================================================")
                        print('the amount that u will return is: ', self.returning_amount)
                        print("==========================================================\n")
                        time.sleep(1)
                        break

                    else:
                        self.balance = 0
                        self.returning_amount += extra
                        print("\n========================================================")
                        print('The amount that u have to return is: ', self.returning_amount)
                        print("==========================================================\n")
                        time.sleep(1)

                else:
                    self.balance -= self.cash_out

                existing_transactions = self.instance.content[self.accountNumber]['track']
                existing_transactions[self.curr_date] = self.cash_out
                self.instance.content[self.accountNumber]['track'] = existing_transactions
                break

            except ValueError:
                print("\n--------------------------------------------")
                print('Invalid input. Please enter a valid amount.')


class SavingsAccount(Account): #child class of account
    def __init__(self, ir, min_amount, instance, account_number):  # ir=0.01 (1% per month), min_amount=500
        self.interestRate, self.minimumAmount = ir, min_amount
        super().__init__(instance, account_number, balance=0)
        data_value.update({'account type': 'Savings Account'})

    def previous(self): ##gets balance
        self.balance = self.instance.content[self.accountNumber]['balance']
        Account.deposit(self)

    def acc_created(self): #stores account creation date
        Account.current_time(self)
        track.update({self.curr_date: 'none, ACCOUNT CREATED'})

    def withdraw(self): #works as per our saving account withdrawal policy
        self.balance = self.instance.content[self.accountNumber]['balance']
        while True:
            try:
                self.cash_out = float(input('Enter the withdraw amount: '))
                if self.cash_out<0:
                    raise ValueError
                elif self.balance >= self.minimumAmount and self.cash_out <= self.balance:
                    super().time_management()
                    bonus = round(((self.balance * self.interestRate) * self.months), 2)
                    self.balance -= self.cash_out
                    print("============================================================================")
                    print(f"You are back after {self.months} months")
                    print(f"Your withdrawn amount is {self.cash_out + bonus} with a bonus of {bonus}")
                    print("============================================================================\n")
                    time.sleep(1)
                    existing_transactions = self.instance.content[self.accountNumber]['track']
                    existing_transactions[self.curr_date] = self.cash_out + bonus
                    self.instance.content[self.accountNumber]['track'] = existing_transactions
                    break

                else:
                    print('\n BANK BALANCE INSUFFICIENT')
                    min_bal = self.balance - self.minimumAmount
                    print("========================================")
                    print(f'you can only withdraw {min_bal} amount')
                    print("========================================\n")

            except ValueError:
                print("--------------------------------------------")
                print('Invalid input. Please enter a valid amount.')
                time.sleep(1)


class LoanAccount(Account): #child class of account
    def __init__(self, pa, ir, ld, instance, account_number):  # pa=0 , ir=0.1, ld=12 months
        self.principleAmount, self.interestRate, self.loanDuration = pa, ir, ld
        super().__init__(instance, account_number, balance=0)

    def acc_created(self): #stores account creation date
        Account.current_time(self)
        track.update({self.curr_date: 'none, ACCOUNT CREATED'})

    def loan(self): #provides loan
        self.principleAmount = float(input('Please enter the amount u want as a loan from bank:'))
        try:
            if self.principleAmount>0:
                print("::::::::::::::::::::::::::::::::::::::::::::::::")
                print(f': Congratulations you have been grated the loan :')
                print(":::::::::::::::::::::::::::::::::::::::::::::::")
                self.balance += self.principleAmount
            else:
                raise ValueError
        except ValueError:
            print("\n--------------------------")
            print("INVALID INPUT\n")
            time.sleep(1)
            self.loan()

    def withdraw(self): #for withdrawal
        self.balance = self.instance.content[self.accountNumber]['balance']
        while True:
            try:
                self.cash_out = float(input('Enter the withdraw amount: '))
                if self.cash_out<0:
                    raise ValueError
                elif self.cash_out < self.balance :
                    self.balance -= self.cash_out
                    break

                else:
                    print("======================")
                    print('Insufficient balance')
                    print("======================\n")
                    time.sleep(1)
                    break
            except ValueError:
                print("\n_____________________________________________")
                print('Invalid input. Please enter a valid amount.')

    def calculation(self): #calculates returning amount with interest
        self.cal = self.principleAmount * self.interestRate
        self.final_cal = (self.principleAmount + self.cal)
        data_value.update({'account type': 'Loan Account', 'loan': self.final_cal})
        time.sleep(1)
        print(f"\n=============================================")
        print(f'you will RETURN the amount {self.final_cal}')
        print(f"===============================================")

    def final(self): #function for the payed back loan
        self.balance = self.instance.content[self.accountNumber]['balance']
        self.principleAmount = self.instance.content[self.accountNumber]['loan']
        super().time_management()
        while True:
            try:
                if self.months > 12 and self.principleAmount != 0:
                    self.interestRate = 0.12
                    LoanAccount.calculation(self)
                elif self.months < 12 and self.principleAmount <= 0:
                    self.principleAmount = 0
                    time.sleep(1)
                    print("+++++++++++++++++++++++++++++++++++++++++++++++")
                    print('+ CONGRATULATION! YOU HAVE PAID YOUR LOAN OFF.+')
                    print("+++++++++++++++++++++++++++++++++++++++++++++++")

                dep = float(input('Enter the amount for returning loan: '))
                if dep>0:

                    existing_transactions = self.instance.content[self.accountNumber]['deposit']
                    existing_transactions[self.curr_date] = dep
                    self.instance.content[self.accountNumber]['deposit'] = existing_transactions

                    self.principleAmount -= dep

                    existing_transactions = self.instance.content[self.accountNumber]
                    existing_transactions['loan'] = self.principleAmount
                    self.instance.content[self.accountNumber] = existing_transactions
                    break
                else:
                    raise ValueError
            except ValueError:
                print("--------------------------------------------")
                print('Invalid input. Please enter a valid amount.')
                time.sleep(1)

#Customer: This class represents a bank customer and handles the creation of new accounts and account selection for existing customers.
# It interacts with the DataHandling class to update and save customer account data.
class Customer:
    def __init__(self):
        self.firstName = input('Enter your first name: ')
        self.lastName = input('Enter your last name: ')
        self.username = input('Enter your username: ')
        self.gmail = input('Enter your gmail: ')
        self.phoneNumber = input('Enter your phoneNumber: ')
        self.password = input('Enter your password: ')
        pin = random.sample(range(1, 10), 4) #generates account number
        self.accountNumber = ''.join(map(str, pin)) #assigns account number
        time.sleep(1)
        print("\n=================================================")
        print(f'YOUR ACCOUNT NUMBER IS {self.accountNumber} ')
        print("==================================================")
        time.sleep(1)
        print(f' (Do not forget your account number otherwise u wont be able to use your account again)')
        print(".........................................................................................\n")
        time.sleep(1)

        self.object = DataHandling() #creates an object for retrieval of data
        self.object.load_file()

    def diff_account(self):
        while True:
            try:
                create_account = int(input('''WHICH ACCOUNT WOULD YOU LIKE TO CREATE: 
                1. Checking Account
                2. Saving Account
                3. Loan Account
                ENTER: '''))
                print("::::::::::::::::::::::::::::::::::::::::::::::::::::::\n") #account creation based on customer's choice
                time.sleep(1)
                if create_account == 1:
                    c = CheckingAccount(5000, self.object, self.accountNumber)
                    c.acc_created()
                    c.deposit()
                    print("")
                    time.sleep(1)
                    print("======================================")
                    print('YOUR BALANCE IS:', c.balance_enquiry())
                    print("=======================================")
                    break
                elif create_account == 2:
                    save = SavingsAccount(0.01, 500, self.object, self.accountNumber)
                    save.acc_created()
                    save.deposit()
                    print("")
                    time.sleep(1)
                    print("=======================================")
                    print('YOUR BALANCE IS:', save.balance_enquiry())
                    print("=======================================")
                    break
                elif create_account == 3:
                    loan = LoanAccount(0, 0.05, 12, self.object, self.accountNumber)
                    loan.acc_created()
                    loan.loan()
                    print("")
                    time.sleep(1)
                    print("=======================================")
                    print('YOUR BALANCE IS:', loan.balance_enquiry())
                    print("=======================================")
                    loan.calculation()
                    break
                else:
                    raise ValueError
            except ValueError:
                print("--------------")
                print('INVALID ENTRY\n')
            time.sleep(1)



    def update(self): #updates the info for storage and further procedures
        data_value.update(
            {'username': self.username, 'name': [self.firstName, self.lastName], 'track': track, 'deposit': deposit, 'returning amount': 0})
        self.object.content[self.accountNumber] = data_value

    def filing(self): #dumps the file
        self.object.dump_file()

#Admin: This class provides an interface for administrative tasks such as accessing customer details, changing credentials, and printing customer information.
# It interacts with the DataHandling class to retrieve and display customer data.
class Admin:
    @staticmethod
    def interface(): #loads admin interface
        time.sleep(1)
        print("\n:::::::::::::::::::::::::::::::::::::::")
        print("""1) ACCESS CUSTOMER'S DETAILS 
2) ACCESS A "PARTICULAR CUSTOMER'S" DETAILS 
3) CHANGE USERNAME AND PASSWORD 
4) TO EXIT""")
        print(":::::::::::::::::::::::::::::::::::::::\n")
        time.sleep(1)

    def set_credentials(self): #sets new credentials
        self.username = input("Enter new Username: ")
        self.password = input("Enter new Password: ")
        with open("me.txt", "w") as f:
            f.write(self.username + " " + self.password)
        print("NEW USERNAME/PASSWORD SET!")

    @staticmethod
    def printing(): #prints all customer history
        obj = DataHandling()
        obj.load_file()
        for key, value in obj.content.items():
            account = key
            print(f"ACCOUNT NUMBER : {key}")
            print('==========================')
            obj.customer_history(account)
            print("""+++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++\n \n""")
            time.sleep(2)

    @staticmethod
    def p_printing(): #prints a particular customer's history
        obj = DataHandling()
        pin = input("Enter account number: ")
        obj.customer_history(pin)


    def admin_interface(self): #provides option for selection
        while True:
            self.interface()
            try:
                choice = input("Here: ")
                if choice == "1":
                    self.printing()
                elif choice == "2":
                    self.p_printing()
                elif choice == "3":
                    self.set_credentials()
                elif choice == "4":
                    break
                else:
                    print('INVALID VALUE')
            except ValueError:
                print('Invalid input. Please enter a valid option.')

#Start: This class is responsible for starting the banking system and handling user input to navigate between customer
# and administrative functionalities.
class Start: #generates opening interface
    def starting(self):
        print("                              @:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@")
        print('                              @        ~    WELCOME TO SSR BANK    ~      @')
        print("                              @:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@")
        time.sleep(1)

        while True: #loops for smooth execution
            print('\n1. Admin  \n2. Customer')
            response = input("ENTER: ")
            print("::::::::::::::::::::\n")
            time.sleep(1)
            if response == '2':
                print('1. New Account \n2. Old Account')
                # while True:
                reply = input("ENTER: ")
                print("::::::::::::::::::::::::::::")
                print("")
                time.sleep(1)
                if reply == '1': #working based on user's selection
                    c = Customer()
                    c.update()
                    c.diff_account()
                    c.update()
                    c.filing()
                    break

                elif reply == '2':
                    while True:
                        acc_num = input('ENTER YOUR ACCOUNT NUMBER: ')
                        print(":::::::::::::::::::::::::::::\n")
                        time.sleep(1)
                        self.dh = DataHandling()
                        self.dh.load_file()
                        find = self.dh.search(acc_num)
                        if find:
                            acc = find['account type']
                            print("=============================")
                            print(f'YOU HAVE A {acc}')
                            print("=============================\n")
                            time.sleep(1)
                            while True:
                                print('1) TO DEPOSIT \n2) TO WITHDRAW \n3) TO VIEW BALANCE AND HISTORY \n4) TO EXIT')

                                options = input("ENTER: ")
                                print(":::::::::::::::\n")
                                time.sleep(1)
                                if options == '3':
                                    h = DataHandling()
                                    h.customer_history(acc_num)
                                elif options == '4':
                                    break

                                elif acc == 'Checking Account':
                                    c = CheckingAccount(5000, self.dh, acc_num)
                                    c.current_time()
                                    if options == '1':
                                        c.previous()
                                        self.dh.content[acc_num]['balance'] = c.balance
                                    elif options == '2':
                                        c.withdraw()
                                        self.dh.content[acc_num]['balance'] = c.balance
                                        self.dh.content[acc_num]['returning amount'] = c.returning_amount
                                    else:
                                        print("\n---------------------")
                                        print('Invalid entry\n')
                                    time.sleep(1)
                                    print("\n=======================================")
                                    print('YOUR BALANCE IS:', c.balance_enquiry())
                                    print("=========================================\n")
                                    time.sleep(1)

                                elif acc == 'Savings Account':
                                    save = SavingsAccount(0.01, 500, self.dh, acc_num)
                                    save.current_time()
                                    if options == '1':
                                        save.previous()
                                        self.dh.content[acc_num]['balance'] = save.balance
                                    elif options == '2':
                                        save.withdraw()
                                        self.dh.content[acc_num]['balance'] = save.balance
                                    else:
                                        print("\n---------------------")
                                        print('Invalid entry\n')
                                    time.sleep(1)
                                    print("\n=======================================")
                                    print('YOUR BALANCE IS:', save.balance_enquiry())
                                    print("=========================================\n")
                                    time.sleep(1)

                                elif acc == 'Loan Account':
                                    loan = LoanAccount(0, 0.05, 12, self.dh, acc_num)
                                    loan.current_time()
                                    if options == '1':
                                        loan.final()
                                        self.dh.content[acc_num]['balance'] = loan.balance
                                    elif options == '2':
                                        loan.withdraw()
                                        time.sleep(1)
                                        print("\n=======================================")
                                        print('YOUR BALANCE IS:', loan.balance_enquiry())
                                        print("=========================================\n")
                                        time.sleep(1)
                                        self.dh.content[acc_num]['balance'] = loan.balance
                                    else:
                                        print("\n---------------------")
                                        print('Invalid entry\n')
                                    time.sleep(1)
                                    print("\n=======================================")
                                    print('YOUR BALANCE IS:', loan.balance_enquiry())
                                    print("=========================================\n")
                                    time.sleep(1)

                                else:
                                    print("\n---------------------")
                                    print('Invalid entry\n')
                                    time.sleep(1)

                            self.dh.dump_file()
                            break
                        else:
                            print("---------------------")
                            print('ACCOUNT NOT FOUND\n')
                        time.sleep(1)

                    break
                else:
                    print("\n---------------------")
                    print('Invalid entry\n')
                time.sleep(1)

                # break
            elif response == '1':
                a = Admin()
                username_a = input("Username: ")
                password_a = input("Password: ")
                with open('me.txt') as admin:
                    admin = admin.read()
                    admin = admin.split()
                if username_a == admin[0] and password_a == admin[1]: #checks whether the credentials match
                    a.admin_interface()
                    break
                else:
                    print('INVALID USERNAME OR PASSWORD')

            else:
                print('Invalid entry')


s = Start()
s.starting() #starts the program

