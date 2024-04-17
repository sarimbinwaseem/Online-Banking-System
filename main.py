import random
import time
from Banking.customer import Customer
from Banking.admin import Admin
# contains account number
data = {}

# contains username password balance etc passed as a value to data{}
data_value = {}  

# has another dictionary passed to d containing time/date etc. 
# key: date, value: day
track = {}  

# contains all deposit history
deposit = {} 



class Start:
    """
    Start: This class is responsible for starting the banking system and handling user input to navigate between customer
    and administrative functionalities.
    generates opening interface
    """
    def __init__(self):
        self.customer = Customer()

    def starting(self):
        print("                              @:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@")
        print('                              @        ~    WELCOME TO SSR BANK    ~      @')
        print("                              @:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@:@")
        time.sleep(1)

        #loops for smooth execution
        while True: 
            print('\n1. Admin  \n2. Customer')
            response = input("ENTER: ")
            print("::::::::::::::::::::\n")
            time.sleep(1)
            if response == '2':
               self.customer.new_customer()

            elif response == '1':
                a = Admin()
                username_a = input("Username: ")
                password_a = input("Password: ")
                with open('me.txt') as admin_file:
                    admin_read = admin_file.read()
                    admin_object = admin_read.split()

                # checks whether the credentials match
                if username_a == admin_object[0] and password_a == admin_object[1]:
                    a.admin_interface()
                    break
                else:
                    print('INVALID USERNAME OR PASSWORD')

            else:
                print('Invalid entry')

def main():
    session = Start()
    session.starting()

if __name__ == "__main__":
    main()