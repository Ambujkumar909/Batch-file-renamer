import streamlit as st
import pandas as pd
import os
import base64

# --- Page Configuration ---
st.set_page_config(page_title="Activity Logger", layout="wide")

# --- Custom CSS for a permanent dark theme and UI modifications ---
st.markdown("""
<style>
    /* Main app background */
    body {
        background-color: #0F1116;
    }
    [data-testid="stAppViewContainer"] > .main {
        background-color: #0F1116 !important;
        padding-top: 80px; /* Space for the top logo */
        padding-bottom: 50px;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }

    /* Make all text white for readability */
    .stApp, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp label, .stMarkdown, body, .st-emotion-cache-1y4p8pa {
        color: #FAFAFA !important;
    }

    /* Style input widgets for dark mode */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background-color: #1a1a1a;
        color: #FAFAFA;
        border: 1px solid #3d3d3d;
        border-radius: 0.25rem;
    }
    
    /* Style selectbox */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a1a1a;
        color: #FAFAFA;
        border: 1px solid #3d3d3d;
    }

    /* Style buttons */
    .stButton > button {
        border-color: #3d3d3d;
        color: #FAFAFA;
        background-color: #262730;
    }
    .stButton > button:hover {
        border-color: #007bff;
        color: #007bff;
        background-color: #262730;
    }
    .stButton > button:focus {
        border-color: #007bff;
        color: #007bff;
        background-color: #262730;
        box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.5);
    }

    /* Style the dataframe */
    .stDataFrame {
        background-color: #1a1a1a;
    }
    thead[data-testid="stDataFrameResizableHandle"] {
        background-color: #262730;
    }
    
    /* Existing CSS for header layout */
    div[data-testid="stHorizontalBlock"] > div:first-child {
        flex-grow: 1;
    }
    div[data-testid="stHorizontalBlock"] > div:not(:first-child) {
        flex-grow: 0;
    }

    /* --- From ui_custom.py --- */
    /* Hide hamburger menu, footer, and deploy button */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stAppDeployButton"] { display: none !important; }

    /* Custom logo positioning */
    .custom-logo {
        position: fixed;
        top: -20px;
        left: 40px;
        z-index: 1000;
    }

    /* "Powered by" text positioning */
    .bottom-right-text {
        position: fixed;
        bottom: 10px;
        right: 20px;
        color: white;
        font-family: 'Arial', sans-serif;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)


# --- App State Management ---
if 'page' not in st.session_state:
    st.session_state.page = 'main_form'
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False
if 'user_employee_code' not in st.session_state:
    st.session_state.user_employee_code = None

# --- Constants and File Setup ---
CSV_FILE = 'submissions.csv'
CSV_HEADER = [
    'Employee Code', 'Full Name','SAP Usage', 'SAP/ECC Username', 'Activity Name', 'Description of Activity',
    'Frequency', 'Avg. Time per Instance (mins)', 'Is this core?',
    'Can be automated?'
]
ADMIN_PASSWORD = "password123"

if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=CSV_HEADER).to_csv(CSV_FILE, index=False)

# --- Helper Functions ---
def append_to_csv(data_list):
    """Appends a list of dictionaries to the submissions CSV."""
    try:
        df_new = pd.DataFrame(data_list)
        df_new.to_csv(CSV_FILE, mode='a', header=False, index=False)
        return True
    except Exception as e:
        st.error(f"Failed to save data: {e}")
        return False

def navigate_to(page_name):
    """Function to switch pages and force a rerun for instant navigation."""
    st.session_state.page = page_name
    st.rerun()

def add_logo(svg_file_path=".svg file"):
    """Injects the custom logo and footer into the page."""
    try:
        with open(svg_file_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
        svg_base64 = base64.b64encode(svg_content.encode()).decode()
        
        st.markdown(
            f"""
            <div class="custom-logo">
                <img src="data:image/svg+xml;base64,{svg_base64}" width="150">
            </div>
            <div class="bottom-right-text">
                Powered by D'Decor
            </div>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning(f'"{svg_file_path}" not found. Logo and footer will not be displayed.')


# --- Inject Custom UI Elements ---
add_logo()

def add_footer():
    """Injects the custom logo and footer into the page."""
    try:
       
        st.markdown(
            f"""
            
            <div class="bottom-right-text">
                Powered by D'Decor
            </div>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning(f'Logo and footer will not be displayed.')

add_footer()

# --- Common Header with Navigation ---
def app_header(page_title):
    """Creates a consistent header for all pages."""
    cols = st.columns([1, 4, 1])
    with cols[0]:
        if st.session_state.page != 'main_form':
            if st.button("🏠 Back to Main Form", use_container_width=True):
                navigate_to('main_form')
    with cols[1]:
        st.title(page_title)
    with cols[2]:
        pass
    

# --- UI Sections / "Pages" ---

# 1. Main Data Entry Form
def main_form_page():
    # --- Main Header and Navigation ---
    cols = st.columns([4, 1.2, 1])
    with cols[0]:
        st.title("📝 Employee Activity Log")
    with cols[1]:
        if st.button("👤 Go to My Activities", use_container_width=True):
            navigate_to('user_login')
    with cols[2]:
        if st.button("🔒 Admin Login", use_container_width=True, type="secondary"):
            navigate_to('admin_login')
    

    # --- Employee Details ---
    st.subheader("Your Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        employee_code = st.text_input("Employee Code", placeholder="e.g., EMP123")
    with col2:
        full_name = st.text_input("Full Name", placeholder="e.g., Jane Doe")
    with col3:
        num_activities = st.number_input("Number of Activities", min_value=1, max_value=20, value=1, step=1)
    sap_col1, sap_col2, sap_col3 = st.columns(3)
    with sap_col1:
        sap_usage = st.selectbox(
            "Are you using SAP for work?",
            ("No", "Yes- ECC", "Yes- HANA"),
	    key="sap_usage"
        )
    with sap_col2:
        sap_user_name = "" # Initialize as empty
        if sap_usage != "No":
            sap_user_name = st.text_input("SAP/ECC User Name",key="sap_user_name")
    st.divider()

    # --- Dynamic Activity Entry Form ---
    if employee_code and full_name:
        with st.form(key="activity_entry_form"):
            st.subheader(f"Log Your {num_activities} Activities")
            
            header_cols = st.columns((3, 4, 2, 2, 2, 2))
            with header_cols[0]: st.markdown("**Activity Name**")
            with header_cols[1]: st.markdown("**Description of Activity**")
            with header_cols[2]: st.markdown("**Frequency**")
            with header_cols[3]: st.markdown("**Avg. Time (mins)**")
            with header_cols[4]: st.markdown("**Is Core?**")
            with header_cols[5]: st.markdown("**Can be Automated?**")

            all_activities_data = []
            for i in range(num_activities):
                activity_data = {}
                row_cols = st.columns((3, 4, 2, 2, 2, 2))
                
                with row_cols[0]:
                    activity_data['Activity Name'] = st.text_input("Activity Name", label_visibility="collapsed", key=f"name_{i}")
                with row_cols[1]:
                    activity_data['Description of Activity'] = st.text_area("Description", label_visibility="collapsed", key=f"desc_{i}", height=50)
                with row_cols[2]:
                    activity_data['Frequency'] = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "Quarterly", "Ad-hoc"], label_visibility="collapsed", key=f"freq_{i}")
                with row_cols[3]:
                    activity_data['Avg. Time per Instance (mins)'] = st.number_input("Time", min_value=0, step=15, label_visibility="collapsed", key=f"time_{i}")
                with row_cols[4]:
                    activity_data['Is this core?'] = st.selectbox("Core?", ["Yes", "No"], label_visibility="collapsed", key=f"core_{i}")
                with row_cols[5]:
                    activity_data['Can be automated?'] = st.selectbox("Automated?", ["Yes", "No", "Maybe"], label_visibility="collapsed", key=f"auto_{i}")

                activity_data['Employee Code'] = employee_code
                activity_data['Full Name'] = full_name
                activity_data['SAP Usage'] = st.session_state.sap_usage
                activity_data['SAP/ECC Username'] = st.session_state.get('sap_user_name', 'N/A') if st.session_state.sap_usage != "No" else "N/A"

                
                all_activities_data.append(activity_data)

            submitted = st.form_submit_button("Submit All Activities", type="primary", use_container_width=True)

            if submitted:
                valid_activities = [d for d in all_activities_data if d.get('Activity Name')]
                if valid_activities:
                    final_data_to_save = [{col: activity.get(col) for col in CSV_HEADER} for activity in valid_activities]
                    if append_to_csv(final_data_to_save):
                        st.success(f"Successfully submitted {len(valid_activities)} activities for {full_name}!")
                else:
                    st.warning("Please fill in at least one Activity Name before submitting.")

# 2. Admin Login Page
def admin_login_page():
    app_header("🔒 Admin Login")
    password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login", type="primary"):
        if password == ADMIN_PASSWORD:
            st.session_state.admin_authenticated = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Incorrect password.")

# 3. Admin Dashboard Page
def admin_dashboard_page():
    cols = st.columns([4, 1])
    with cols[0]:
        st.title("👑 Admin Dashboard")
        st.markdown("Viewing all submissions from all employees.")
    with cols[1]:
        if st.button("Logout", type="secondary", use_container_width=True):
            st.session_state.admin_authenticated = False
            navigate_to('main_form')
    
    try:
        df = pd.read_csv(CSV_FILE)
        
        if not df.empty:
            st.subheader("Submissions")
            
            filter_col1, filter_col2 = st.columns([1, 2]) 
            with filter_col1:
                filter_code = st.text_input(
                    "Filter by Employee Code:", 
                    placeholder="Type code..."
                )
            
            if filter_code:
                filtered_df = df[df['Employee Code'].astype(str).str.contains(filter_code, case=False, na=False)]
            else:
                filtered_df = df
            
            st.success(f"Displaying {len(filtered_df)} entries.")
            st.dataframe(filtered_df)
        else:
             st.info("No submissions have been made yet.")

    except pd.errors.EmptyDataError:
        st.info("No submissions have been made yet.")
    except Exception as e:
        st.error(f"Could not load data: {e}")

# 4. User "Login" Page
def user_login_page():
    app_header("👤 My Activities Dashboard")
    
    col1, _ = st.columns([1, 2])
    with col1:
        employee_code = st.text_input(
            "Enter Your Employee Code to View Your Submissions", 
            key="user_emp_code"
        )

    if st.button("View My Activities", type="primary"):
        if employee_code:
            st.session_state.user_employee_code = employee_code
            navigate_to('user_dashboard')
        else:
            st.warning("Please enter an Employee Code.")

# 5. User Dashboard Page
def user_dashboard_page():
    employee_code = st.session_state.user_employee_code
    app_header(f"Dashboard for {employee_code}")

    try:
        df = pd.read_csv(CSV_FILE)
        user_df = df[df['Employee Code'].astype(str).str.lower() == str(employee_code).lower()]
        
        if not user_df.empty:
            # --- NEW: Display user details at the top ---
            first_row = user_df.iloc[0]
            full_name = first_row['Full Name']
            sap_username = first_row['SAP/ECC Username']

            st.subheader("Employee Details")
            details_cols = st.columns(3)
            details_cols[0].metric("Employee Name", full_name)
            details_cols[1].metric("Employee Code", employee_code)
            if pd.notna(sap_username) and sap_username != "N/A":
                 details_cols[2].metric("SAP/ECC Username", sap_username)
            
            st.divider()
            st.subheader("Your Logged Activities")

            # --- NEW: Display only activity-related columns in the table ---
            activity_columns = [
                'Activity Name', 'Description of Activity', 'Frequency', 
                'Avg. Time per Instance (mins)', 'Is this core?', 'Can be automated?'
            ]
            activity_df = user_df[activity_columns]
            st.dataframe(activity_df)
        else:
            st.info("No submissions found for this Employee Code.")
            
    except pd.errors.EmptyDataError:
        st.info("No submissions have been made yet.")
    except Exception as e:
        st.error(f"Could not load data: {e}")


# --- Main App Router ---
if st.session_state.page == 'main_form':
    main_form_page()
elif st.session_state.page == 'admin_login':
    if st.session_state.admin_authenticated:
        admin_dashboard_page()
    else:
        admin_login_page()
elif st.session_state.page == 'user_login':
    user_login_page()
elif st.session_state.page == 'user_dashboard':
    if st.session_state.user_employee_code:
        user_dashboard_page()
    else:
        user_login_page()
