import mysql.connector
import streamlit as st
import pandas as pd
import datetime as dt 
from io import StringIO
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

def load_csv(uploaded_file):
    try:
        # Read CSV file into DataFrame
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error reading the CSV file: {e}")
        return None
    
# create streamlit app
def main():
    st.title("Student registration form");

    # display option for CRUD operations
    option = st.selectbox("select an operation",("create","read","update","delete"))
    if option == "create":
        st.subheader("Upload and Add CSV Data")
        uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
        
        if uploaded_file is not None:
            df = load_csv(uploaded_file)
            if df is not None:
                st.write("Data preview:", df.head())

                if st.button("Upload CSV to Database"):
                    # Ensure all necessary columns are present in the DataFrame
                    required_columns = ['name', 'fname', 'gmail', 'cnumber', 'dob']
                    if all(col in df.columns for col in required_columns):
                        for i, row in df.iterrows():
                            sql = "INSERT INTO users (name, fname, gmail, cnumber, dob) VALUES (%s, %s, %s, %s, %s)"
                            mycursor.execute(sql, tuple(row[required_columns]))
                        mydb.commit()
                        st.success("CSV Data Uploaded Successfully!")
                    else:
                        st.error("CSV file must contain the following columns: ")

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
