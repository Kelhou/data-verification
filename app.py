import streamlit as st
import pandas as pd
from datetime import date

# Load the Excel data and format the date correctly
def load_data():
    try:
        df = pd.read_excel('1stsem.xlsx')
        df['dob'] = pd.to_datetime(df['dob']).dt.date  # Ensure dob is formatted as date
        df['gender'] = df['gender'].str.capitalize()  # Capitalize gender to match selectbox options
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Save the Excel data
def save_data(df):
    try:
        df['dob'] = pd.to_datetime(df['dob']).dt.strftime('%Y-%m-%d')  # Ensure dob is saved as string in correct format
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
st.markdown("<h1 style='text-align: center;'>Verification & Data Updation for 1st Semester Students Enrolled in Data Entry and Office Assistant Course</h1>", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'row_index' not in st.session_state:
    st.session_state.row_index = None

# Define functions for page navigation
def goto_login():
    st.session_state.page = 'login'
    st.session_state.user_data = None
    st.session_state.row_index = None

def goto_update():
    st.session_state.page = 'update'

# Handle navigation based on session state
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
                st.session_state.page = 'update'  # Change page to update
            else:
                st.error('Login failed! Incorrect ID or Date of Birth.')

if st.session_state.page == 'update' and st.session_state.user_data is not None:
    st.markdown("<h2 style='text-align: center;'>Update Your Information: Fill Empty Fields (nan) and Correct Errors</h2>", unsafe_allow_html=True)
    user_data = st.session_state.user_data
    row_index = st.session_state.row_index

    name = st.text_input('Name', user_data['name'])
    department = st.text_input('Department', user_data['department'])
    gender = st.selectbox('Gender', ['Male', 'Female'], index=['Male', 'Female'].index(user_data['gender'].capitalize()))
    dob = st.date_input('Date of Birth', user_data['dob'], min_value=date(1900, 1, 1), max_value=date.today())
    email = st.text_input('Email', user_data['email'])
    mobile = st.text_input('Mobile', user_data['mobile'])
    aadhar = st.text_input('Aadhar', user_data['aadhar'])
    fathersname = st.text_input("Father's Name", user_data['fathersname'])
    mothersname = st.text_input("Mother's Name", user_data['mothersname'])

    # Validation
    valid_mobile = len(mobile) == 10 and mobile.isdigit()
    valid_aadhar = len(aadhar) == 12 and aadhar.isdigit()

    if st.button('Update'):
        if not valid_mobile:
            st.error("Mobile number must be a 10-digit number.")
        elif not valid_aadhar:
            st.error("Aadhar number must be a 12-digit number.")
        else:
            df = load_data()
            df.loc[row_index, 'name'] = name
            df.loc[row_index, 'department'] = department
            df.loc[row_index, 'gender'] = gender
            df.loc[row_index, 'dob'] = dob.strftime('%Y-%m-%d')
            df.loc[row_index, 'email'] = email
            df.loc[row_index, 'mobile'] = mobile
            df.loc[row_index, 'aadhar'] = aadhar
            df.loc[row_index, 'fathersname'] = fathersname
            df.loc[row_index, 'mothersname'] = mothersname
            save_data(df)

    if st.button('Logout'):
        goto_login()

# Removing default footer
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

