import time
from Banking.account import Account


class LoanAccount(Account):  # child class of account
    def __init__(
        self, pa, ir, ld, instance, account_number
    ):  # pa=0 , ir=0.1, ld=12 months
        self.principleAmount, self.interestRate, self.loanDuration = pa, ir, ld
        super().__init__(instance, account_number, balance=0)

    def acc_created(self):  # stores account creation date
        Account.current_time(self)
        track.update({self.curr_date: "none, ACCOUNT CREATED"})

    def loan(self):  # provides loan
        self.principleAmount = float(
            input("Please enter the amount u want as a loan from bank:")
        )
        try:
            if self.principleAmount > 0:
                print("::::::::::::::::::::::::::::::::::::::::::::::::")
                print(": Congratulations you have been grated the loan :")
                print(":::::::::::::::::::::::::::::::::::::::::::::::")
                self.balance += self.principleAmount
            else:
                raise ValueError
        except ValueError:
            print("\n--------------------------")
            print("INVALID INPUT\n")
            time.sleep(1)
            self.loan()

    def withdraw(self):  # for withdrawal
        self.balance = self.instance.content[self.accountNumber]["balance"]
        while True:
            try:
                self.cash_out = float(input("Enter the withdraw amount: "))
                if self.cash_out < 0:
                    raise ValueError
                if self.cash_out < self.balance:
                    self.balance -= self.cash_out
                    break

                else:
                    print("======================")
                    print("Insufficient balance")
                    print("======================\n")
                    time.sleep(1)
                    break
            except ValueError:
                print("\n_____________________________________________")
                print("Invalid input. Please enter a valid amount.")

    def calculation(self):  # calculates returning amount with interest
        self.cal = self.principleAmount * self.interestRate
        self.final_cal = self.principleAmount + self.cal
        data_value.update({"account type": "Loan Account", "loan": self.final_cal})
        time.sleep(1)
        print("\n=============================================")
        print(f"you will RETURN the amount {self.final_cal}")
        print("===============================================")

    def final(self):  # function for the payed back loan
        self.balance = self.instance.content[self.accountNumber]["balance"]
        self.principleAmount = self.instance.content[self.accountNumber]["loan"]
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
                    print("+ CONGRATULATION! YOU HAVE PAID YOUR LOAN OFF.+")
                    print("+++++++++++++++++++++++++++++++++++++++++++++++")

                dep = float(input("Enter the amount for returning loan: "))
                if dep > 0:
                    existing_transactions = self.instance.content[self.accountNumber][
                        "deposit"
                    ]
                    existing_transactions[self.curr_date] = dep
                    self.instance.content[self.accountNumber][
                        "deposit"
                    ] = existing_transactions

                    self.principleAmount -= dep

                    existing_transactions = self.instance.content[self.accountNumber]
                    existing_transactions["loan"] = self.principleAmount
                    self.instance.content[self.accountNumber] = existing_transactions
                    break
                
                raise ValueError

            except ValueError:
                print("--------------------------------------------")
                print("Invalid input. Please enter a valid amount.")
                time.sleep(1)
