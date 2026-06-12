import streamlit as st
import json
import random
import string
from pathlib import Path

st.set_page_config(page_title="Bank Management System", page_icon="🏦")


class Bank:
    database = "data.json"

    # Load data
    if Path(database).exists():
        try:
            with open(database, "r") as f:
                data = json.load(f)
        except:
            data = []
    else:
        data = []

    @staticmethod
    def update():
        with open(Bank.database, "w") as f:
            json.dump(Bank.data, f, indent=4)

    @staticmethod
    def accountGenerate():
        alpha = ''.join(random.choices(string.ascii_letters, k=3))
        num = ''.join(random.choices(string.digits, k=3))
        sp = ''.join(random.choices("!@#$%&*", k=1))

        acc = list(alpha + num + sp)
        random.shuffle(acc)
        return ''.join(acc)


st.title("🏦 Bank Management System")

menu = st.sidebar.selectbox(
    "Select Operation",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Show Details",
        "Update Account",
        "Delete Account"
    ]
)

# ---------------- CREATE ----------------
if menu == "Create Account":
    st.header("Create Account")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18)
    email = st.text_input("Email")
    pin = st.text_input("PIN", type="password")

    if st.button("Create Account"):
        if not name or not email or not pin:
            st.error("All fields required")
        elif len(pin) != 4:
            st.error("PIN must be 4 digits")
        else:
            account = {
                "name": name,
                "age": age,
                "email": email,
                "pin": pin,
                "accountNo": Bank.accountGenerate(),
                "balance": 0
            }

            Bank.data.append(account)
            Bank.update()

            st.success("Account Created Successfully")
            st.write("Account Number:", account["accountNo"])


# ---------------- DEPOSIT ----------------
elif menu == "Deposit Money":
    st.header("Deposit Money")

    accountNo = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        user = next(
            (u for u in Bank.data
             if u["accountNo"] == accountNo and u["pin"] == pin),
            None
        )

        if user:
            user["balance"] += amount
            Bank.update()
            st.success("Deposit Successful")
            st.write("Balance:", user["balance"])
        else:
            st.error("User Not Found")


# ---------------- WITHDRAW ----------------
elif menu == "Withdraw Money":
    st.header("Withdraw Money")

    accountNo = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        user = next(
            (u for u in Bank.data
             if u["accountNo"] == accountNo and u["pin"] == pin),
            None
        )

        if not user:
            st.error("User Not Found")

        elif amount > user["balance"]:
            st.error("Insufficient Balance")

        else:
            user["balance"] -= amount
            Bank.update()
            st.success("Withdrawal Successful")
            st.write("Balance:", user["balance"])


# ---------------- SHOW DETAILS ----------------
elif menu == "Show Details":
    st.header("Account Details")

    accountNo = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show"):
        user = next(
            (u for u in Bank.data
             if u["accountNo"] == accountNo and u["pin"] == pin),
            None
        )

        if user:
            st.json(user)
        else:
            st.error("User Not Found")


# ---------------- UPDATE ----------------
elif menu == "Update Account":
    st.header("Update Account")

    accountNo = st.text_input("Account Number")
    pin = st.text_input("Current PIN", type="password")

    name = st.text_input("New Name")
    email = st.text_input("New Email")
    new_pin = st.text_input("New PIN", type="password")

    if st.button("Update"):
        user = next(
            (u for u in Bank.data
             if u["accountNo"] == accountNo and u["pin"] == pin),
            None
        )

        if user:
            if name:
                user["name"] = name
            if email:
                user["email"] = email
            if new_pin:
                user["pin"] = new_pin

            Bank.update()
            st.success("Account Updated Successfully")
        else:
            st.error("User Not Found")


# ---------------- DELETE ----------------
elif menu == "Delete Account":
    st.header("Delete Account")

    accountNo = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        user = next(
            (u for u in Bank.data
             if u["accountNo"] == accountNo and u["pin"] == pin),
            None
        )

        if user:
            Bank.data.remove(user)
            Bank.update()
            st.success("Account Deleted Successfully")
        else:
            st.error("User Not Found")