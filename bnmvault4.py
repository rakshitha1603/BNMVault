import streamlit as st
import pandas as pd
import altair as alt
import pymongo
from PIL import Image



st.title("BNM VAULT")

def connect_db():
    conn = pymongo.MongoClient("mongodb://localhost:27017")
    db = conn['BNMvault']
    return db

# function to find the current user details and cache the result
@st.cache_resource()
def get_username():
    return [None]

# function to store the current user details
def set_username(user):
    username = get_username()
    username[0] = user
    
# function to check the login status and cache the result
@st.cache_resource()
def get_login_status():
    return [False]

# def student_login(username, password):
#     db=connect_db()
#     user_collection=db.students
#     user = user_collection.find_one({"USN":username , "Password": password})
#     if user:
#         # st.success("login successful!")
#         return 1
#     else:
#         # st.error("invalid username or password. please enter again.")
#         return 0

def student_login(username, password):
    db = connect_db()
    user_collection = db.students
    user = user_collection.find_one({"USN": username, "Password": password})

    if user:
        return 1
    else:
        return 0


# def student_login(username, password):
#     return username == "student" and password == "student123"

# Function to check admin login credentials
def admin_login(user,username, password):
    return username == user['Username'] and password == user['Password']


def set_login_status(logged_in):
    login_status = get_login_status()
    # login_status[0] = logged_in
    login_status.clear()
    login_status.append(logged_in)

# Function to add a student
def add_student():
    db=connect_db()
    user_col = db['students']
    st.subheader("Add Student")
    student_usn = st.text_input("USN")
    student_pswd=st.text_input("Password")
    student_FName = st.text_input("First Name")
    student_Lname= st.text_input("Last Name")
    student_age = st.text_input("Age")
    student_gen = st.text_input("Gender")
    student_dob = st.date_input("DOB")
    student_mail=st.text_input("Email")
    # Add more student details (email, dob, etc.)
    add_student_button = st.button("Add Student")

    if add_student_button:
        user = user_col.find_one({"USN": student_usn})
        if not user:
        # Add the student to a database or data frame
            user_col.insert_one({"USN":student_usn,"Password":student_pswd,"First Name":student_FName,"Last Name":student_Lname,"Age":student_age,"Gender":student_gen,"DOB":str(student_dob),"Email":student_mail})
            st.success("Student added successfully!")
        # Example: student_data = pd.DataFrame(...)
        else:
            st.error("User already exists.")
        
# Function to add attendance
def add_attendance():
    db=connect_db()
    user_col = db['students']
    st.subheader("Add Attendance")
    date = st.date_input("Date")
    student_usn = st.text_input("Student USN")
    subject_options = ["Math", "Operating System", "English", "Computer Organization"]
    selected_subject = st.selectbox("Select Subject", subject_options)
    classes_present = st.number_input("Classes Present", min_value=0)
    # classes_absent = st.number_input("Classes Absent", min_value=0)
    total_classes = st.number_input("Total Classes", min_value=0)
    
    # Calculate attendance percentage based on classes present and total classes
    attendance_percentage = (classes_present / total_classes) * 100 if total_classes > 0 else 0
    st.write(f"Attendance Percentage: {attendance_percentage:.2f}%")
    num_absent = total_classes-classes_present
    st.write(f"Total Classes Absent: {num_absent: d}")
    
    add_attendance_button = st.button("Add Attendance")

    if add_attendance_button:
        user = user_col.find_one({"USN": student_usn})
        if user:
        # Add the student to a database or data frame
            user_col.update_one({"USN":student_usn},{'$set':{f'Attendance.{selected_subject}':{'Classes Present':classes_present,'Total Classes':total_classes}}})
            st.success("Attendance updated successfully!")
        # Example: student_data = pd.DataFrame(...)
        else:
            st.error("User does not exists.")


# Function to add marks
def add_marks():
    db=connect_db()
    user_col = db['students']
    st.subheader("Add Marks")
    student_usn = st.text_input("Student USN")
    subject_options = ["Math", "Operating System", "English", "Computer Organization"]
    selected_subject = st.selectbox("Select Subject", subject_options)
    marks_obtained = st.number_input("Marks Obtained", min_value=0, max_value=100)
    total_marks = st.number_input("Total Marks", min_value=0, max_value=100)
    add_marks_button = st.button("Add Marks")

    if add_marks_button:
        # Calculate percentage based on marks obtained and total marks
        marks_percentage = (marks_obtained / total_marks) * 100 if total_marks > 0 else 0
        user = user_col.find_one({"USN": student_usn})
        if user:
        # Add the student to a database or data frame
            user_col.update_one({"USN":student_usn},{'$set':{f'Marks.{selected_subject}':{'Marks Obtained':marks_obtained,'Total Marks':total_marks}}})
            st.success("Marks updated successfully!")
        # Example: student_data = pd.DataFrame(...)
        else:
            st.error("User does not exists.")

def main():
    connect_db()
    # Check if user is logged in
   
    logged_in = get_login_status()[0]
    

    # If the user is not logged in, show the login page
    if not logged_in:
        render_login_page()
    elif logged_in == 'Student':
        # If the user is logged in, show the main app page
        render_user_page()
    elif logged_in == 'Admin':
        render_admin_page()

def render_login_page():
    db=connect_db()
    user_collection=db.students
    st.title("Login Portal")

    login_option = st.radio("Select User Type", ["Student", "Admin"])

    if login_option == "Student":
        st.subheader("Student Login")
        username = st.text_input("USN")
        password = st.text_input("Password", type="password")
        submitted = st.button("Login")

        # if submitted:
        #     user = user_collection.find_one({"USN": username})
        #     if user:
        #         # set_login_status(True)
        #         student_login(username, password)
        #         set_login_status('Student')
        #         st.experimental_rerun()
        #         # Redirect to student dashboard or perform actions
        #     else:
        #         st.error("Invalid student credentials")

        if submitted:
            user = user_collection.find_one({"USN": username})
            if user and student_login(username, password):
                set_username(username)
                set_login_status('Student')
                st.experimental_rerun()
            else:
                st.error("Invalid student credentials")


    elif login_option == "Admin":
        st.subheader("Admin Login")
        admin_username = st.text_input("Admin Username")
        admin_password = st.text_input("Admin Password", type="password")
        admin_submitted = st.button("Login as Admin")

        if admin_submitted:
            user = user_collection.find_one({"Username": admin_username})
            if admin_login(user,admin_username, admin_password):
                st.success("Admin login successful!")
                # set_login_status(True)
                set_login_status('Admin')
                st.experimental_rerun()
                # Redirect to admin dashboard or perform admin actions
            else:
                st.error("Invalid admin credentials")

    # # image=Image.open("bnmit.png")
    # # st.markdown(
    # #     unsafe_allow_html=True)
    # # st.image(image)
    # with st.form("login_form"):
    #     st.subheader("Login")
    #     username = st.text_input('Username')
    #     password = st.text_input('Password', type='password')
    #     # Every form must have a submit button.
    #     submitted = st.form_submit_button("Submit")

    #     # if form is submitted
    #     if submitted:
    
    #         # check if login credentials are correct
    #         if(username == "Akshitha" and password=="123456"):
    #             # save the current user's details
                
    #             # set the login_status to True to render the main_page
    #             set_login_status(True)
    #             st.experimental_rerun()
def render_admin_page():
    st.title("Admin Dashboard")
    menu_options = ["Add Student", "Add Attendance", "Add Marks", "Search by USN"]
    selected_option = st.sidebar.selectbox("Select an Option", menu_options)

    if selected_option == "Add Student":
        add_student()
    elif selected_option == "Add Attendance":
        add_attendance()
    elif selected_option == "Add Marks":
        add_marks()
    elif selected_option == "Search by USN":
        search_by_usn()
        # search_by_usn()

    # Logout button
    if st.sidebar.button("Logout"):
        set_login_status(False)
        st.experimental_rerun()

def search_by_usn():
    db = connect_db()
    user_col = db['students']
    usn = st.text_input("Enter USN to search")
    submit = st.button("Search")
    if submit:
        user = user_col.find_one({"USN": usn})
        if user:
            st.subheader(f"Student details of {user['First Name']}")
            col1,col2 = st.columns(2)
            col1.text_input(f"First Name", value=f"{user['First Name']}",disabled=True)
            col2.text_input(f"Last Name",value=f"{user['Last Name']}",disabled=True)
            col1.text_input(f"Age",value=f"{user['Age']}",disabled=True)
            col2.text_input(f"Gender",value=f"{user['Gender']}",disabled=True)
            col1.text_input(f"DOB",value=f"{user['DOB']}",disabled=True)
            col2.text_input(f"Email",value=f"{user['Email']}",disabled=True)
            # Redirect to admin dashboard or perform admin actions
        else:
            st.error("Student doesnt exist")


def render_user_page():
    db = connect_db()
    user_col = db['students']
    
    st.markdown(
        """
    <style>
    section[data-testid="stSidebar"] div.stButton button {
    width: 300px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        # Create buttons for the dashboard
        st.header(f"Welcome, {user_col.find({'USN':get_username()[0]})[0]['First Name']}")
        st.subheader(" Your Dashboard")
        menu_options = ["Attendance", "Academics", "Fees", "Events"]
        selected_option = st.sidebar.selectbox("Select an Option", menu_options)
        logout_button = st.button("Logout")


    if selected_option == "Attendance":
        render_attendance_page(user_col)
    elif selected_option == "Academics":
        render_academic_results_page(user_col)
    elif selected_option == "Fees":
        render_fees_page()
    elif selected_option == "Events":
        render_events_page()
        # Add the logout button

    # Handle button clicks
    if logout_button:
        set_login_status(False)
        st.experimental_rerun()

    # Show the corresponding page based on the button clicked
    # if attendance_button:
    #     render_attendance_page()
    # elif academic_results_button:
    #     render_academic_results_page()
    # elif fees_button:
    #     render_fees_page()
    # elif events_button:
    #     render_events_page()

def render_attendance_page(user_col):
    st.subheader("Attendance Page")
    st.write("Attendance Data:")
    # col1,col2 = st.columns([1,1])
    mylist = []
    subject = [i for i in user_col.find({'USN':get_username()[0]})[0]['Attendance'].keys()]
    for i in range(len(subject)):
        classes_present = user_col.find({'USN':get_username()[0]})[0]['Attendance'][subject[i]]['Classes Present']
        total_classes = user_col.find({'USN':get_username()[0]})[0]['Attendance'][subject[i]]['Total Classes']
        attendance_percentage = (classes_present / total_classes) * 100 if total_classes > 0 else 0
        mylist.append(attendance_percentage)
    # print(user_col.find({'USN':get_username()[0]})[0]['Attendance'][subject[0]]['Classes Present'])
    attendance_data = pd.DataFrame({
    'Subject': [i for i in user_col.find({'USN':get_username()[0]})[0]['Attendance'].keys()],
    'Attendance Percentage': mylist
})
    #st.image("attendance_image.png", use_column_width=True)  # Replace with your attendance-related image

    st.dataframe(attendance_data, hide_index=True,use_container_width=True)

    # Attendance chart
    attendance_chart = alt.Chart(attendance_data).mark_bar().encode(
        x='Subject',
        y='Attendance Percentage',
        tooltip=['Subject', 'Attendance Percentage']
    ).properties(
        width=700,
        height=400
    )
    st.altair_chart(attendance_chart)

    st.altair_chart(attendance_data)
    marks_chart = alt.Chart(attendance_data).mark_circle().encode(
        alt.X('Subject:N', title='Subject'),
        alt.Y('Attendance Percentage:Q', title='Attendance Percentage'),
        size='Attendance Percentage:Q',
        color='Subject:N',
        tooltip=['Subject:N', 'Attendence Percentage:Q']
    ).properties(
        width=600,
        height=400,
        title='Attendence Distribution Across Subjects'
    )
    st.altair_chart(marks_chart)

def render_academic_results_page(user_col):
    st.subheader("Academic Results Page")
    #st.image("academic_results_image.png", use_column_width=True)  # Replace with your academic results-related image
    obtained = []
    total = []
    subject = [i for i in user_col.find({'USN':get_username()[0]})[0]['Marks'].keys()]
    st.write("Academic Results Data:")
    print(subject)
    # col1,col2 = st.columns([3,1])
    for i in range(len(subject)):
        marks_obtained = user_col.find({'USN':get_username()[0]})[0]['Marks'][subject[i]]['Marks Obtained']
        total_marks = user_col.find({'USN':get_username()[0]})[0]['Marks'][subject[i]]['Total Marks']
        obtained.append(marks_obtained)
        total.append(total_marks)
    academic_results_data = pd.DataFrame({
    'Subject': subject,
    'Marks Obtained': obtained,
    'Total Marks' : total
})
    st.dataframe(academic_results_data, hide_index=True, use_container_width=True)

    # Academic results chart
    academic_results_chart = alt.Chart(academic_results_data).mark_bar().encode(
        x='Subject',
        y='Marks Obtained'
    ).properties(
        width=700,
        height=400
    )
    st.altair_chart(academic_results_chart)
    marks_chart = alt.Chart(academic_results_data).mark_circle().encode(
        alt.X('Subject:N', title='Subject'),
        alt.Y('Marks Obtained:Q', title='Marks Obtained'),
        size='Marks Obtained:Q',
        color='Subject:N',
        tooltip=['Subject:N', 'Marks Obtained:Q']
    ).properties(
        width=600,
        height=400,
        title='Marks Distribution Across Subjects'
    )
    st.altair_chart(marks_chart)


def render_fees_page():
    st.subheader("Fees Page")
    st.write("Status of Fees:")

    # Display the status of fees (paid or not paid)
    fees_status = st.radio("Fees Status", ["Paid", "Not Paid"])
    st.write(f"Fees Status: {fees_status}")


def render_events_page():
    st.subheader("Events Page")
    st.write("Upcoming Events:")

    # Display events such as internals, holidays, exams
    events_list = ["Internals", "Holidays", "Exams"]

    # Sample dates for the events
    event_dates = {
        "Internals": pd.Timestamp("2023-08-10"),
        "Holidays": pd.Timestamp("2023-09-05"),
        "Exams": pd.Timestamp("2023-10-20")
    }

    selected_events = st.multiselect("Select Events", events_list)

    st.write("Selected Events:")
    # st.write(selected_events)
    for event in selected_events:
        if event in event_dates:
            st.write(f"- {event}: {event_dates[event].strftime('%Y-%m-%d')}")
        else:
            st.write(f"- {event}")

if __name__ == "__main__":
    main()