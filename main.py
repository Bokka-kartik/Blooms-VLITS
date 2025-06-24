# import streamlit as st
# from auth import authenticate_user, register_user

# st.set_page_config(page_title="AI Question Bank System", layout="wide")

# if "logged_in" not in st.session_state:
#     st.session_state["logged_in"] = False

# if not st.session_state["logged_in"]:
#     col1,col2=st.columns(2)
#     with col1:
#         st.image("vignan.png",use_container_width=True)
#     with col2:
#         st.title("Vignan Automated Question Bank System")

#         tab1, tab2 = st.tabs(["***Login***", "***Sign Up***"])

#         with tab1:
#             username = st.text_input("Username")
#             password = st.text_input("Password", type="password")
#             if st.button("Login"):
#                 role = authenticate_user(username, password)
#                 if role:
#                     st.session_state["logged_in"] = True
#                     st.session_state["username"] = username
#                     st.session_state["role"] = role
#                     st.rerun()
#                 else:
#                     st.error("Invalid username or password!")

#         with tab2:
#             new_username = st.text_input("New Username")
#             new_password = st.text_input("New Password", type="password")
#             role = st.selectbox("Role", ["user", "admin"])
#             if st.button("Register"):
#                 if register_user(new_username, new_password, role):
#                     st.success("✅ Registration Successful! You can now log in.")
#                 else:
#                     st.error("⚠️ Username already exists!")

# else:
#     if st.session_state["role"] == "admin":
#         import admin_dashboard
#         admin_dashboard.show_admin_dashboard()
#     else:
#         import user_dashboard
#         user_dashboard.show_user_dashboard()
# import streamlit as st
# from auth import authenticate_user, register_user

# st.set_page_config(page_title="AI Question Bank System", layout="wide")

# # Custom CSS for fixing scrolling and button styling
# st.markdown(
#     """
#     <style>
#         /* Fix image scrolling issue */
#         .stImage img {
#             height: 700px !important; /* Adjust as needed */
#             object-fit: cover;
#         }

#         /* Rounded buttons and hover effect */
#         div.stButton > button {
#             border-radius: 25px; /* Rounded corners */
#             background-color: #009999; /* Initial button color */
#             color: white;
#             padding: 10px 20px;
#             border: none;
#             transition: background-color 0.3s ease;
#         }

#         /* Hover effect */
#         div.stButton > button:hover {
#             background-color: red !important; /* Change to red on hover */
#             color: white !important;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Session State for Login
# if "logged_in" not in st.session_state:
#     st.session_state["logged_in"] = False

# if not st.session_state["logged_in"]:
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.image("vignan.png", use_container_width=True)

#     with col2:
#         st.title("Vignan Automated Question Bank System")

#         tab1, tab2 = st.tabs(["***Login***", "***Sign Up***"])

#         with tab1:
#             username = st.text_input("Username")
#             password = st.text_input("Password", type="password")
#             if st.button("Login"):
#                 role = authenticate_user(username, password)
#                 if role:
#                     st.session_state["logged_in"] = True
#                     st.session_state["username"] = username
#                     st.session_state["role"] = role
#                     st.rerun()
#                 else:
#                     st.error("Invalid username or password!")

#         with tab2:
#             new_username = st.text_input("New Username")
#             new_password = st.text_input("New Password", type="password")
#             role = st.selectbox("Role", ["user", "admin"])
#             if st.button("Register"):
#                 if register_user(new_username, new_password, role):
#                     st.success("✅ Registration Successful! You can now log in.")
#                 else:
#                     st.error("⚠️ Username already exists!")

# else:
#     if st.session_state["role"] == "admin":
#         import admin_dashboard
#         admin_dashboard.show_admin_dashboard()
#     else:
#         import user_dashboard
#         user_dashboard.show_user_dashboard()
import streamlit as st
from auth import authenticate_user, register_user

st.set_page_config(page_title="AI Question Bank System", layout="wide")

# Custom CSS for fixing scrolling, button styling, and centering buttons
st.markdown(
    """
    <style>
        /* Fix image scrolling issue */
        .stImage img {
            height: 400px !important;
            object-fit: cover;
        }

        /* Button Styling: Same size, rounded, and centered */
        .custom-button {
            display: flex;
            justify-content: center;
        }

        div.stButton > button {
            width: 200px !important;  /* Fixed width */
            height: 45px !important;  /* Fixed height */
            border-radius: 25px !important; /* Rounded corners */
            background-color: #009999 !important; /* Initial button color */
            color: black !important;
            font-color:black;
            font-size: 16px !important;
            font-weight: bold !important;
            border: none !important;
            transition: background-color 0.3s ease-in-out;
        }

        /* Hover effect */
        div.stButton > button:hover {
            background-color: red !important; /* Change to red on hover */
            color: black !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Session State for Login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    col1, col2 = st.columns(2)

    with col1:
        st.image("vignan.png", use_container_width=True)

    with col2:
        st.title("Vignan Automated Question Bank System")

        tab1, tab2 = st.tabs(["***Login***", "***Sign Up***"])

        with tab1:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            # Centered button
            col_btn = st.columns([1, 2, 1])  # Empty space on both sides
            with col_btn[1]:
                st.markdown('<div class="custom-button">', unsafe_allow_html=True)
                if st.button("Login"):
                    role = authenticate_user(username, password)
                    if role:
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = username
                        st.session_state["role"] = role
                        st.rerun()
                    else:
                        st.error("Invalid username or password!")
                st.markdown("</div>", unsafe_allow_html=True)

        with tab2:
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            role = st.selectbox("Role", ["user", "admin"])

            # Centered button
            col_btn = st.columns([1, 2, 1])
            with col_btn[1]:
                st.markdown('<div class="custom-button">', unsafe_allow_html=True)
                if st.button("Register"):
                    if register_user(new_username, new_password, role):
                        st.success("✅ Registration Successful! You can now log in.")
                    else:
                        st.error("⚠️ Username already exists!")
                st.markdown("</div>", unsafe_allow_html=True)

else:
    if st.session_state["role"] == "admin":
        import admin_dashboard
        admin_dashboard.show_admin_dashboard()
    else:
        import user_dashboard
        user_dashboard.show_user_dashboard()
