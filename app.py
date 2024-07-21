import streamlit as st
import pandas as pd
from datetime import date

# Load the Excel data
def load_data():
    try:
        df = pd.read_excel('1stsem.xlsx')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Save the Excel data
def save_data(df):
    try:
        df.to_excel('1stsem.xlsx', index=False)
        st.success("Details updated successfully!")
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Normalize strings for comparison
def normalize_string(s):
    return str(s).strip().lower()

# Normalize dates for comparison
def normalize_date(d):
    return pd.to_datetime(d).strftime('%Y-%m-%d')

# Check login credentials
def check_credentials(df, student_id, dob):
    normalized_uid = normalize_string(student_id)
    normalized_dob = normalize_date(dob)
    for i, row in df.iterrows():
        row_uid = normalize_string(row['uid'])
        row_dob = normalize_date(row['dob'])

        if row_uid == normalized_uid and row_dob == normalized_dob:
            return i, row
    return None, None

# Streamlit app
st.title('User Login and Data Update')

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Define functions for page navigation
def goto_login():
    st.session_state.page = 'login'
    st.session_state.user_data = None
    st.session_state.row_index = None

def goto_update():
    st.session_state.page = 'update'

# Login page
if st.session_state.page == 'login':
    st.subheader('Login')
    student_id = st.text_input('Student ID')
    dob = st.date_input('Date of Birth', min_value=date(1900, 1, 1), max_value=date.today())

    if st.button('Login'):
        df = load_data()
        if not df.empty:
            dob_str = dob.strftime('%Y-%m-%d')  # Convert date to string for comparison
            row_index, user_data = check_credentials(df, student_id, dob_str)
            if user_data is not None:
                st.success('Login successful!')
                st.session_state.user_data = user_data
                st.session_state.row_index = row_index
                goto_update()
            else:
                st.error('Login failed! Incorrect ID or Date of Birth.')

# Update page
if st.session_state.page == 'update' and st.session_state.user_data is not None:
    st.subheader('Update Your Details')
    user_data = st.session_state.user_data
    row_index = st.session_state.row_index

    name = st.text_input('Name', user_data['name'])
    department = st.text_input('Department', user_data['department'])
    gender = st.text_input('Gender', user_data['gender'])
    dob = st.date_input('Date of Birth', pd.to_datetime(user_data['dob']), min_value=date(1900, 1, 1), max_value=date.today())
    email = st.text_input('Email', user_data['email'])
    mobile = st.text_input('Mobile', user_data['mobile'])
    aadhar = st.text_input('Aadhar', user_data['aadhar'])
    fathers_name = st.text_input("Father's Name", user_data['fathersname'])
    mothers_name = st.text_input("Mother's Name", user_data['mothersname'])

    if st.button('Update'):
        df = load_data()
        df.loc[row_index, 'name'] = name
        df.loc[row_index, 'department'] = department
        df.loc[row_index, 'gender'] = gender
        df.loc[row_index, 'dob'] = dob.strftime('%Y-%m-%d')
        df.loc[row_index, 'email'] = email
        df.loc[row_index, 'mobile'] = mobile
        df.loc[row_index, 'aadhar'] = aadhar
        df.loc[row_index, 'fathersname'] = fathers_name
        df.loc[row_index, 'mothersname'] = mothers_name
        save_data(df)

    if st.button('Logout'):
        goto_login()

if __name__ == '__main__':
    st.write('User Login and Data Update App')
