from abc import ABC, abstractmethod
from Banking.datahandling import DataHandling


class Account(ABC):
    """
    abstract class having all basic methods required for sub-classes
    Account (abstract class): This is an abstract base class that defines common attributes and methods for different types of bank accounts.
    It has methods for depositing, withdrawing, and checking the balance of an account.
    The withdraw() method is defined as an abstract method, which needs to be implemented in the derived classes.
    """

    def __init__(self, instance, account_number, balance=0):
        self.instance = instance  # object passed
        self.accountNumber = account_number
        self.balance = balance
        self.data_value = {}

    def deposit(self):
        """deposits amount"""

        while True:
            try:
                self.dep = float(input("Enter the amount to deposit:"))
                if self.dep > 0:
                    self.balance += self.dep
                    existing_transactions = self.instance.content[self.accountNumber][
                        "deposit"
                    ]
                    existing_transactions[self.curr_date] = self.dep
                    self.instance.content[self.accountNumber][
                        "deposit"
                    ] = existing_transactions
                    break
                else:
                    print("Invalid deposit")
            except ValueError:
                print("Invalid input. Please enter a valid amount.")

    @abstractmethod
    def withdraw(self):
        pass

    def balance_enquiry(self):
        self.data_value.update({"balance": self.balance})
        return self.balance

    def current_time(self):
        """takes date as an input and checks it for being out of range"""

        while True:
            try:
                self.curr_date = input(
                    "Enter the current date in (YYYY MM DD) format: "
                )
                print("---------------------------------------------------")
                a = self.curr_date.split()
                b = list(map(int, a))

                if (
                    b[0] < 2023 or 12 < b[1] or b[1] <= 0 or 31 < b[2] or b[2] < 1
                ):  # FOR PRINTING WITH IN RANGE
                    raise ValueError
                else:
                    break

            except ValueError:
                print("Invalid input. Please enter a valid date.")

    def time_management(self, months=0):  # checks if it has been a month
        self.months = months
        year, month, day = map(int, self.curr_date.split())

        extract = DataHandling()
        extract.load_file()  # loads file into self.content
        find = self.instance.content[self.accountNumber]["track"]  # track is a key here

        last_element = list(find.items())[-1]
        last_key = last_element[0]  # ????
        self.last_date = last_key

        l_year, l_month, l_day = map(int, self.last_date.split())
        self.duration = ((year * 365) + (month * 30) + day) - (
            (l_year * 365) + (l_month * 30) + l_day
        )
        if self.duration > 30:
            while True:
                self.duration -= 30
                self.months += 1
                if self.duration < 30:
                    break
        else:
            print("Your duration is less than a month")


def main():
    acc = Account(23, 33)
    acc.current_time()


if __name__ == "__main__":
    main()
