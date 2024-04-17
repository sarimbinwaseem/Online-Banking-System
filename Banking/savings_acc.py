import time
from Banking.account import Account


class SavingsAccount(Account):  # child class of account
    def __init__(
        self, ir, min_amount, instance, account_number
    ):  # ir=0.01 (1% per month), min_amount=500
        self.interestRate, self.minimumAmount = ir, min_amount
        super().__init__(instance, account_number, balance=0)
        self.data_value.update({"account type": "Savings Account"})

    def previous(self):  ##gets balance
        self.balance = self.instance.content[self.accountNumber]["balance"]
        Account.deposit(self)

    def acc_created(self):  # stores account creation date
        Account.current_time(self)
        track.update({self.curr_date: "none, ACCOUNT CREATED"})

    def withdraw(self):  # works as per our saving account withdrawal policy
        self.balance = self.instance.content[self.accountNumber]["balance"]
        while True:
            try:
                self.cash_out = float(input("Enter the withdraw amount: "))
                if self.cash_out < 0:
                    raise ValueError
                if (
                    self.balance >= self.minimumAmount and self.cash_out <= self.balance
                ):
                    super().time_management()
                    bonus = round(((self.balance * self.interestRate) * self.months), 2)
                    self.balance -= self.cash_out
                    print(
                        "============================================================================"
                    )
                    print(f"You are back after {self.months} months")
                    print(
                        f"Your withdrawn amount is {self.cash_out + bonus} with a bonus of {bonus}"
                    )
                    print(
                        "============================================================================\n"
                    )
                    time.sleep(1)
                    existing_transactions = self.instance.content[self.accountNumber][
                        "track"
                    ]
                    existing_transactions[self.curr_date] = self.cash_out + bonus
                    self.instance.content[self.accountNumber][
                        "track"
                    ] = existing_transactions
                    break

                else:
                    print("\n BANK BALANCE INSUFFICIENT")
                    min_bal = self.balance - self.minimumAmount
                    print("========================================")
                    print(f"you can only withdraw {min_bal} amount")
                    print("========================================\n")

            except ValueError:
                print("--------------------------------------------")
                print("Invalid input. Please enter a valid amount.")
                time.sleep(1)
