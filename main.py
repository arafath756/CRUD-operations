import mysql.connector
import streamlit as st
import pandas as pd
import datetime as dt 
# streamlit run main.py

# establish connection to mysql server
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "abc123",
    database = "crud_new1"
)
mycursor = mydb.cursor()
print("connection establishment")

# create streamlit app
def main():
    st.title("Student registration form");

    # display option for CRUD operations
    option = st.selectbox("select an operation",("create","read","update","delete"))
    if option == "create":
        st.subheader("create record")
        name = st.text_input("enter your name")
        fname = st.text_input("enter your father name")
        dob = st.date_input("date of birth",value=None,
        min_value = dt.date(1700,1,1),
        max_value = dt.date(2024,12,31))
        gmail = st.text_input("enter email")
        cnumber = st.text_input("contact number")
        if st.button("submit"):
            sql = "insert into users(name, fname, gmail, cnumber, dob) values(%s, %s, %s, %s, %s)"
            val = (name, fname, gmail, cnumber, dob)
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("record created successfully")

    elif option == "read":
        st.subheader("read record")
        
        mycursor.execute("select * from users")
        result = mycursor.fetchall()
        df = pd.DataFrame(result,columns = mycursor.column_names)
        st.dataframe(df)
    
    elif option == "update":
        st.subheader("update record")
        id = st.number_input("Enter ID",min_value = 1)
        name = st.text_input("Enter new name")
        fname = st.text_input("Enter new father name")
        dob = st.date_input("date of birth",value=None,
        min_value = dt.date(1700,1,1),
        max_value = dt.date(2024,12,31))
        gmail = st.text_input("Enter new Email")
        cnumber = st.text_input("Enter new Contact number")
        if st.button("update"):
            sql = "Update users set name = %s, fname = %s, gmail = %s, dob = %s, cnumber = %s where id = %s"
            val = (name,fname,gmail,dob,cnumber,id)
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("Record update successfully")

    elif option == "delete":
        st.subheader("delete record")
        id = st.number_input("Enter ID",min_value = None)
        if st.button("delete"):
            sql = "delete from users where id = %s"
            val = (id,)
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("record deleted successfully")

if __name__ == "__main__":
    main()

