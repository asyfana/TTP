import streamlit as st
from customer import customer_page
from cleaner import cleaner_page
from about import about_page

# Set up the sidebar and app title
st.sidebar.image("homies.jpg", width=100)
st.sidebar.title("Homies: Household Services Booking")
page = st.sidebar.selectbox("Select Page", ["Customer", "Cleaner", "About Us"])

# Page router
if page == "Customer":
    customer_page()
elif page == "Cleaner":
    cleaner_page()
elif page == "About Us":
    about_page()
