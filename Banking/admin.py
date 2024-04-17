import time
from Banking.datahandling import DataHandling


class Admin:
    """
    Admin: This class provides an interface for administrative tasks such as accessing customer details, changing credentials, and printing customer information.
    It interacts with the DataHandling class to retrieve and display customer data.
    """

    @staticmethod
    def interface():
        """loads admin interface"""

        time.sleep(1)
        print("\n:::::::::::::::::::::::::::::::::::::::")
        print(
            """1) ACCESS CUSTOMERS' DETAILS 
2) ACCESS A "PARTICULAR CUSTOMER'S" DETAILS 
3) CHANGE USERNAME AND PASSWORD 
4) TO EXIT"""
        )
        print(":::::::::::::::::::::::::::::::::::::::\n")
        time.sleep(1)

    def set_credentials(self):  # sets new credentials
        self.username = input("Enter new Username: ")
        self.password = input("Enter new Password: ")
        with open("me.txt", "w") as f:
            f.write(f"{self.username} {self.password}")
        print("NEW USERNAME/PASSWORD SET!")

    @staticmethod
    def printing():  # prints all customer history
        obj = DataHandling()
        obj.load_file()
        for key, value in obj.content.items():
            account = key
            print(f"ACCOUNT NUMBER : {key}")
            print("==========================")
            obj.customer_history(account)
            print(
                """+++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++\n \n"""
            )
            time.sleep(2)

    @staticmethod
    def p_printing():  # prints a particular customer's history
        obj = DataHandling()
        pin = input("Enter account number: ")
        obj.customer_history(pin)

    def admin_interface(self):  # provides option for selection
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
                    print("INVALID VALUE")
            except ValueError:
                print("Invalid input. Please enter a valid option.")
