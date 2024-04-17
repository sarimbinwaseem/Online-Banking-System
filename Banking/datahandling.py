import time
from Banking.filing import FileMaking


class DataHandling(FileMaking):
    """
    DataHandling: This class extends FileMaking and provides methods for
    searching and retrieving customer account data from the loaded file.
    It also has a method customer_history() to display the transaction history 
    of a customer.
    """

    def __init__(self):
        # super().__init__()
        pass

    def __getitem__(self, key):
        return self.content[key]

    def search(
        self, acc_num
    ):  # returns bank account number after searching in the content
        if acc_num in self.content:
            self.value = self.content[acc_num]
            return self.value
        else:
            return None

    def customer_history(self, account):  # prints a customer's details
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
                print(
                    f"""\nDATE: {key} 
    -------------------------
    Withdrawn: {value}"""
                )
            print("\nX:X:X:X:X:X:X:X:X:X:X:X:X:X")

            for key, value in info["deposit"].items():
                print("-------------------------")
                print(
                    f"""\nDATE: {key} 
    -------------------------
    Deposited: {value}"""
                )

            if info["account type"] == "Checking Account":
                time.sleep(1)
                print("\n==============================================")
                print(f" HAVE TO RETURN AMOUNT: {info['returning amount']}")
                print("=================================================")

            elif info["account type"] == "Loan Account":
                time.sleep(1)
                print("\n==============================================")
                print(f" HAVE TO RETURN AMOUNT: {info['loan']}")
                print("=================================================\n")
        except:
            print("\n-----------------------------")
            print("INVALID ACCOUNT NUMBER")
            print("--------------------------------")
            time.sleep(1)
            a = input("ENTER YOUR ACCOUNT NUMBER: ")
            print("")
            self.customer_history(a)
