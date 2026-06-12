 # Import required modules
import json          # Used to store data in JSON file
import random        # Used to generate random account number
import string        # Provides letters and digits
from pathlib import Path  # Used to check whether file exists


# Bank Class
class Bank:

    # File name where all account data is stored
    database = "data.json"

    # List that holds all account records
    data = []

    # Load old data from JSON file when program starts
    if Path(database).exists():
        try:
            with open(database, "r") as fs:
                data = json.load(fs)
        except Exception:
            data = []

    # Save updated data into JSON file
    @staticmethod
    def update():
        with open(Bank.database, "w") as fs:
            json.dump(Bank.data, fs, indent=4)

    # Generate a random account number
    @staticmethod
    def accountGenerate():

        # Generate 3 random letters
        alpha = ''.join(random.choices(string.ascii_letters, k=3))

        # Generate 3 random digits
        num = ''.join(random.choices(string.digits, k=3))

        # Generate 1 special character
        spchar = ''.join(random.choices("!@#$%&*", k=1))

        # Combine all characters
        account_id = list(alpha + num + spchar)

        # Shuffle them randomly
        random.shuffle(account_id)

        # Convert list back to string
        return ''.join(account_id)

    # Find user using account number and PIN
    def find_user(self):

        accountNo = input("Enter Account Number: ")
        pin = input("Enter PIN: ")

        # Search through all accounts
        for user in Bank.data:

            # Check account number and PIN match
            if user["accountNo"] == accountNo and user["pin"] == pin:
                return user

        # Return None if user not found
        return None

    # Create a new account
    def create_account(self):

        age = int(input("Enter your age: "))

        # Age validation
        if age < 18:
            print("You are not eligible.")
            return

        # PIN validation
        pin = input("Enter 4-digit PIN: ")

        if len(pin) != 4 or not pin.isdigit():
            print("PIN must be exactly 4 digits.")
            return

        # Store account information in dictionary
        info = {
            "name": input("Enter your name: "),
            "age": age,
            "email": input("Enter your email: "),
            "pin": pin,
            "accountNo": self.accountGenerate(),
            "balance": 0
        }

        # Add account to list
        Bank.data.append(info)

        # Save account in JSON file
        Bank.update()

        print("\nAccount Created Successfully!")
        print("Account Number:", info["accountNo"])

    # Deposit money into account
    def depositMoney(self):

        # Find user first
        user = self.find_user()

        if not user:
            print("User not found")
            return

        amount = int(input("Enter deposit amount: "))

        # Check amount validity
        if amount <= 0:
            print("Invalid amount")
            return

        # Add money to balance
        user["balance"] += amount

        # Save changes
        Bank.update()

        print("Deposit Successful")
        print("Balance:", user["balance"])

    # Withdraw money from account
    def withdrawMoney(self):

        # Find user first
        user = self.find_user()

        if not user:
            print("User not found")
            return

        amount = int(input("Enter withdraw amount: "))

        # Check balance before withdrawal
        if amount > user["balance"]:
            print("Insufficient Balance")
            return

        # Deduct amount
        user["balance"] -= amount

        # Save changes
        Bank.update()

        print("Withdraw Successful")
        print("Balance:", user["balance"])

    # Display account details
    def showDetails(self):

        user = self.find_user()

        if not user:
            print("User not found")
            return

        print("\nAccount Details")

        # Print all key-value pairs
        for key, value in user.items():
            print(f"{key}: {value}")

    # Update account information
    def updateAccount(self):

        user = self.find_user()

        if not user:
            print("User not found")
            return

        # User can update any field
        name = input("New Name (Enter to skip): ")
        email = input("New Email (Enter to skip): ")
        pin = input("New PIN (Enter to skip): ")

        # Update only if value entered
        if name:
            user["name"] = name

        if email:
            user["email"] = email

        if pin:
            user["pin"] = pin

        # Save updated data
        Bank.update()

        print("Account Updated Successfully")

    # Delete account
    def delete(self):

        user = self.find_user()

        if not user:
            print("User not found")
            return

        check = input("Delete Account? (Y/N): ")

        # Delete only if user confirms
        if check.lower() == "y":
            Bank.data.remove(user)

            # Save changes
            Bank.update()

            print("Account Deleted Successfully")


# Create object of Bank class
user = Bank()


# Program starts from here
if __name__ == "__main__":

    while True:

        # Display menu
        print("\n1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Account Details")
        print("5. Update Account")
        print("6. Delete Account")
        print("7. Exit")

        try:
            choice = int(input("Enter your choice: "))

        # Handle invalid input
        except ValueError:
            print("Please enter a number!")
            continue

        # Call methods based on user choice
        if choice == 1:
            user.create_account()

        elif choice == 2:
            user.depositMoney()

        elif choice == 3:
            user.withdrawMoney()

        elif choice == 4:
            user.showDetails()

        elif choice == 5:
            user.updateAccount()

        elif choice == 6:
            user.delete()

        elif choice == 7:
            print("Thank You")
            break

        else:
            print("Invalid Choice")