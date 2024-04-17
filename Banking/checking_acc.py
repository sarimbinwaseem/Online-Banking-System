import time
from Banking.account import Account


class CheckingAccount(Account):
    """
    Child class of account
    CheckingAccount, SavingsAccount, and LoanAccount:
    These classes inherit from the Account class and implement
    the withdraw() method based on the specific rules for each account type.
    They also have additional methods for account creation and handling specific
    account operations.
    """

    def __init__(self, credit_limit, instance, account_number):  # c=5000
        super().__init__(instance, account_number, balance=0)
        self.creditLimit = credit_limit  # per day
        self.data_value.update({"account type": "Checking Account"})

    def previous(self):  # gets balance
        self.balance = self.instance.content[self.accountNumber]["balance"]
        Account.deposit(self)

    def acc_created(self):  # stores the account creation date
        Account.current_time(self)
        track.update({self.curr_date: "none, ACCOUNT CREATED"})

    def withdraw(self):  # ir=0.1 (10%) works based on of withdrawal policy
        self.interest_rate = 0.1
        self.balance = self.instance.content[self.accountNumber]["balance"]
        self.returning_amount = self.instance.content[self.accountNumber][
            "returning amount"
        ]

        while True:
            try:
                self.cash_out = float(input("Enter the withdraw amount: "))
                if self.cash_out < 0:
                    raise ValueError
                elif self.cash_out > self.balance:
                    extra = (
                        self.cash_out - self.balance
                    )  # to check extra money cashed out

                    if extra > self.creditLimit:
                        print("\n======================================")
                        print("You have exceeded your credit limit")
                        print("=======================================\n")
                        time.sleep(1)
                        self.balance = 0
                        self.exceed = (
                            extra - self.creditLimit
                        )  # credit limit exceeded or not
                        interest_rate = self.exceed * self.interest_rate
                        returns = extra + interest_rate
                        self.returning_amount += returns
                        print(
                            "\n========================================================"
                        )
                        print(
                            "the amount that u will return is: ", self.returning_amount
                        )
                        print(
                            "==========================================================\n"
                        )
                        time.sleep(1)
                        break

                    else:
                        self.balance = 0
                        self.returning_amount += extra
                        print(
                            "\n========================================================"
                        )
                        print(
                            "The amount that u have to return is: ",
                            self.returning_amount,
                        )
                        print(
                            "==========================================================\n"
                        )
                        time.sleep(1)

                else:
                    self.balance -= self.cash_out

                existing_transactions = self.instance.content[self.accountNumber][
                    "track"
                ]
                existing_transactions[self.curr_date] = self.cash_out
                self.instance.content[self.accountNumber][
                    "track"
                ] = existing_transactions
                break

            except ValueError:
                print("\n--------------------------------------------")
                print("Invalid input. Please enter a valid amount.")
