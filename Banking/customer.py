import time
import random
from Banking.checking_acc import CheckingAccount
from Banking.loan_acc import LoanAccount
from Banking.savings_acc import SavingsAccount
from Banking.datahandling import DataHandling


class Customer:
    """
    Customer: This class represents
    a bank customer and handles the creation of new accounts
    and account selection for existing customers.
    It interacts with the DataHandling class to update and save
    customer account data.
    """

    def __init__(self):
        self.firstName = ""
        self.lastName = ""
        self.username = ""
        self.email = ""
        self.phoneNumber = ""
        self.password = ""
        self.accountNumber = ""
        self.data_value = {}
        # creates an object for retrieval of data
        self.dh_object = DataHandling()
        self.dh_object.load_file()

    def diff_account(self):
        flag = True
        while flag:
            try:
                create_account = int(
                    input(
                        """WHICH ACCOUNT WOULD YOU LIKE TO CREATE: 
                1. Checking Account
                2. Saving Account
                3. Loan Account
                ENTER: """
                    )
                )
                print(
                    "::::::::::::::::::::::::::::::::::::::::::::::::::::::\n"
                )  # account creation based on customer's choice
                time.sleep(0.2)
                if create_account == 1:
                    c = CheckingAccount(5000, self.dh_object, self.accountNumber)
                    c.acc_created()
                    c.deposit()
                    print("")
                    time.sleep(0.2)
                    print("======================================")
                    print("YOUR BALANCE IS:", c.balance_enquiry())
                    print("=======================================")
                    break
                elif create_account == 2:
                    save = SavingsAccount(0.01, 500, self.dh_object, self.accountNumber)
                    save.acc_created()
                    save.deposit()
                    print("")
                    time.sleep(0.2)
                    print("=======================================")
                    print("YOUR BALANCE IS:", save.balance_enquiry())
                    print("=======================================")
                    break
                elif create_account == 3:
                    loan = LoanAccount(0, 0.05, 12, self.dh_object, self.accountNumber)
                    loan.acc_created()
                    loan.loan()
                    print("")
                    time.sleep(0.2)
                    print("=======================================")
                    print("YOUR BALANCE IS:", loan.balance_enquiry())
                    print("=======================================")
                    loan.calculation()
                    break
                else:
                    raise ValueError
            except ValueError:
                print("--------------")
                print("INVALID ENTRY\n")
            time.sleep(0.2)

    def update(self):  # updates the info for storage and further procedures
        self.data_value.update(
            {
                "username": self.username,
                "name": [self.firstName, self.lastName],
                "track": track,
                "deposit": deposit,
                "returning amount": 0,
            }
        )
        self.dh_object.content[self.accountNumber] = self.data_value

    def filing(self):  # dumps the file
        self.dh_object.dump_file()

    def get_new_info(self):
        self.firstName = input("[?] Enter First Name: ")
        self.lastName = input("[?] Enter Last Name: ")
        self.username = input("[?] Enter Username: ")
        self.email = input("[?] Enter email: ")
        self.phoneNumber = input("[?] Enter Phone Number: ")
        self.password = input("[?] Enter Password: ")

        pin = random.sample(range(1, 10), 4)  # generates account number
        self.accountNumber = "".join(map(str, pin))  # assigns account number
        time.sleep(0.2)
        print("\n=================================================")
        print(f"YOUR ACCOUNT NUMBER IS {self.accountNumber} ")
        print("==================================================")

        print(
            " (Do not forget your account number otherwise you wont be able to use your account again)"
        )
        print(
            ".........................................................................................\n"
        )

    def new_customer(self):
        print("1. New Account \n2. Old Account")
        # while True:
        reply = input("ENTER: ")
        print("::::::::::::::::::::::::::::")
        print("")
        time.sleep(0.2)

        if reply == "1":
            self.get_new_info()
            self.update()
            self.diff_account()
            self.update()
            self.filing()
            # break

        elif reply == "2":
            while True:
                acc_num = input("ENTER YOUR ACCOUNT NUMBER: ")
                print(":::::::::::::::::::::::::::::\n")
                time.sleep(0.2)
                self.dh_object.load_file()
                find = self.dh_object.search(acc_num)
                if not find:
                    print("---------------------")
                    print("ACCOUNT NOT FOUND\n")
                    continue

                acc = find["account type"]
                print("=============================")
                print(f"YOU HAVE A {acc}")
                print("=============================\n")
                time.sleep(0.2)
                while True:
                    print(
                        "1) TO DEPOSIT \n2) TO WITHDRAW \n3) TO VIEW BALANCE AND HISTORY \n4) TO EXIT"
                    )

                    options = input("ENTER: ")
                    print(":::::::::::::::\n")
                    time.sleep(0.2)
                    if options == "3":
                        h = DataHandling()
                        h.customer_history(acc_num)
                    elif options == "4":
                        break

                    elif acc == "Checking Account":
                        c = CheckingAccount(5000, self.dh_object, acc_num)
                        c.current_time()
                        if options == "1":
                            c.previous()
                            self.dh_object.content[acc_num]["balance"] = c.balance
                        elif options == "2":
                            c.withdraw()
                            self.dh_object.content[acc_num]["balance"] = c.balance
                            self.dh_object.content[acc_num][
                                "returning amount"
                            ] = c.returning_amount
                        else:
                            print("\n---------------------")
                            print("Invalid entry\n")
                        
                        self.dh_object.dump_file()

                        time.sleep(0.2)
                        print("\n=======================================")
                        print("YOUR BALANCE IS:", c.balance_enquiry())
                        print("=========================================\n")
                        time.sleep(0.2)

                    elif acc == "Savings Account":
                        save = SavingsAccount(0.01, 500, self.dh_object, acc_num)
                        save.current_time()
                        if options == "1":
                            save.previous()
                            self.dh_object.content[acc_num]["balance"] = save.balance
                        elif options == "2":
                            save.withdraw()
                            self.dh_object.content[acc_num]["balance"] = save.balance
                        else:
                            print("\n---------------------")
                            print("Invalid entry\n")

                        self.dh_object.dump_file()

                        time.sleep(0.2)
                        print("\n=======================================")
                        print("YOUR BALANCE IS:", save.balance_enquiry())
                        print("=========================================\n")
                        time.sleep(0.2)

                    elif acc == "Loan Account":
                        loan = LoanAccount(0, 0.05, 12, self.dh_object, acc_num)
                        loan.current_time()
                        if options == "1":
                            loan.final()
                            self.dh_object.content[acc_num]["balance"] = loan.balance
                        elif options == "2":
                            loan.withdraw()
                            time.sleep(0.2)
                            print("\n=======================================")
                            print("YOUR BALANCE IS:", loan.balance_enquiry())
                            print("=========================================\n")
                            time.sleep(0.2)
                            self.dh_object.content[acc_num]["balance"] = loan.balance
                        else:
                            print("\n---------------------")
                            print("Invalid entry\n")

                        self.dh_object.dump_file()

                        time.sleep(0.2)
                        print("\n=======================================")
                        print("YOUR BALANCE IS:", loan.balance_enquiry())
                        print("=========================================\n")
                        time.sleep(0.2)

                    else:
                        print("\n---------------------")
                        print("Invalid Account Type\n")
                        time.sleep(0.2)

                
                break

                time.sleep(0.2)

        else:
            print("\n---------------------")
            print("Invalid entry\n")
        time.sleep(0.2)

        # break
