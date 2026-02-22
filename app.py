import streamlit as st
from pathlib import Path
import json
import random
import string

# ----------------------------
# Bank Class
# ----------------------------

class Bank:
    database = "data.json"
    data = []

    # Load Data
    if Path(database).exists():
        with open(database) as fs:
            data = json.loads(fs.read())
    else:
        data = []

    @classmethod
    def update(cls):
        with open(cls.database, 'w') as fs:
            json.dump(cls.data, fs)

    @staticmethod
    def generateAcc():
        digits = random.choices(string.digits, k=4)
        alpha = random.choices(string.ascii_letters, k=4)
        acc_id = digits + alpha
        random.shuffle(acc_id)
        return "".join(acc_id)


bank = Bank()

st.title("🏦Bank Management System")

menu = st.sidebar.selectbox(
    "Select Operation",
    ["Create Account", "Deposit Money", "Withdraw Money",
     "Check Details", "Update Details", "Delete Account"]
)

# ----------------------------
# CREATE ACCOUNT
# ----------------------------
if menu == "Create Account":
    st.subheader("Create New Account")

    name = st.text_input("Enter Name")
    age = st.number_input("Enter Age", min_value=0)
    phone = st.text_input("Enter Phone Number")
    email = st.text_input("Enter Email")
    pin = st.text_input("Enter 4 Digit PIN", type="password")

    if st.button("Create Account"):
        if age > 18 and len(pin) == 4 and len(phone) == 10:
            info = {
                "name": name,
                "age": age,
                "phoneNo": int(phone),
                "email": email,
                "pin": int(pin),
                "account_no": Bank.generateAcc(),
                "balance": 0
            }
            Bank.data.append(info)
            Bank.update()
            st.success(f"Account Created Successfully! 🎉")
            st.write("Your Account Number:", info["account_no"])
        else:
            st.error("Invalid Credentials ❌")

# ----------------------------
# DEPOSIT
# ----------------------------
elif menu == "Deposit Money":
    st.subheader("Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Enter Amount", min_value=0)

    if st.button("Deposit"):
        user = [i for i in Bank.data if i['account_no'] == acc and str(i['pin']) == pin]

        if not user:
            st.error("User Not Found ❌")
        elif amount <= 0 or amount > 10000:
            st.error("Invalid Amount ❌")
        else:
            user[0]['balance'] += amount
            Bank.update()
            st.success("Amount Credited Successfully ✅")

# ----------------------------
# WITHDRAW
# ----------------------------
elif menu == "Withdraw Money":
    st.subheader("Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Enter Amount", min_value=0)

    if st.button("Withdraw"):
        user = [i for i in Bank.data if i['account_no'] == acc and str(i['pin']) == pin]

        if not user:
            st.error("User Not Found ❌")
        elif amount <= 0 or amount > 10000:
            st.error("Invalid Amount ❌")
        elif user[0]['balance'] < amount:
            st.error("Insufficient Balance ❌")
        else:
            user[0]['balance'] -= amount
            Bank.update()
            st.success("Amount Debited Successfully ✅")

# ----------------------------
# CHECK DETAILS
# ----------------------------
elif menu == "Check Details":
    st.subheader("Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show Details"):
        user = [i for i in Bank.data if i['account_no'] == acc and str(i['pin']) == pin]

        if not user:
            st.error("User Not Found ❌")
        else:
            st.write("Name:", user[0]['name'])
            st.write("Age:", user[0]['age'])
            st.write("Phone:", user[0]['phoneNo'])
            st.write("Email:", user[0]['email'])
            st.write("Balance:", user[0]['balance'])

# ----------------------------
# UPDATE DETAILS
# ----------------------------
elif menu == "Update Details":
    st.subheader("Update Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    user = [i for i in Bank.data if i['account_no'] == acc and str(i['pin']) == pin]

    if user:
        new_name = st.text_input("New Name", user[0]['name'])
        new_phone = st.text_input("New Phone", str(user[0]['phoneNo']))
        new_email = st.text_input("New Email", user[0]['email'])
        new_pin = st.text_input("New PIN", type="password")

        if st.button("Update"):
            user[0]['name'] = new_name
            user[0]['phoneNo'] = int(new_phone)
            user[0]['email'] = new_email
            if new_pin:
                user[0]['pin'] = int(new_pin)
            Bank.update()
            st.success("Details Updated Successfully ✅")
    else:
        st.warning("Enter valid credentials above 👆")

# ----------------------------
# DELETE ACCOUNT
# ----------------------------
elif menu == "Delete Account":
    st.subheader("Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        user = [i for i in Bank.data if i['account_no'] == acc and str(i['pin']) == pin]

        if not user:
            st.error("User Not Found ❌")
        else:
            Bank.data.remove(user[0])
            Bank.update()
            st.success("Account Deleted Successfully 🗑️")