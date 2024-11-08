import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_folium import st_folium
import folium
from geopy.geocoders import Nominatim
from utils import get_available_slots, calculate_cost, generate_pdf, display_footer

def customer_page():
    st.markdown("<h1 style='text-align: center;'>Book Your Cleaning Service</h1>", unsafe_allow_html=True)

    # Service Cards Section
    st.subheader("Available Services")
    col1, col2 = st.columns(2)
    col1.markdown("### Standard Cleaning\nPerfect for regular upkeep.\n**RM50** per session")
    col2.markdown("### Deep Cleaning\nIntensive cleaning for a fresh start.\n**RM100** per session")

    # Booking Form
    st.subheader("Make a Booking")

    customer_name = st.text_input("Customer Name *")
    contact_info = st.text_input("Contact Info *")
    storey_type = st.selectbox("House Type *", ["Single Storey", "Double Storey"])
    booking_type = st.radio("Select Booking Type *", ["One-Time Booking", "Weekly Booking"])
    cleaning_type = st.radio("Select Cleaning Type *", ["Standard Cleaning", "Deep Cleaning"])
    areas_to_clean = st.multiselect("Areas to Clean *", ["Toilet", "Rooms", "Living Room", "Kitchen", "Garage"])
    women_only = st.checkbox("Women-for-Women Service")

    # Date and Time Selection
    st.subheader("Select Date and Time")
    selected_date = st.date_input("Preferred Date", min_value=datetime.now().date())
    available_slots = get_available_slots(selected_date)
    selected_time_slot = st.radio("Available Time Slots", available_slots) if available_slots else None

    # Address Selection using Google Map or Text Input
    st.subheader("Select Your Address")
    address = st.text_input("Type your address or select on the map")
    
    # Initialize map centered on Kuala Lumpur
    map_center = [3.1390, 101.6869]
    if address:
        geolocator = Nominatim(user_agent="homies_app")
        location = geolocator.geocode(address)
        if location:
            map_center = [location.latitude, location.longitude]
            st.write(f"Typed Address: {address}")
        else:
            st.error("Address not found. Please enter a valid address.")

    m = folium.Map(location=map_center, zoom_start=12)
    address_marker = folium.Marker(location=map_center, draggable=True)
    address_marker.add_to(m)
    map_data = st_folium(m, width=700, height=500)

    selected_address = None
    if map_data and 'last_clicked' in map_data:
        selected_address = map_data['last_clicked']

    if areas_to_clean:
        total_cost = calculate_cost(storey_type, areas_to_clean, booking_type, cleaning_type)
        st.write(f"**Estimated Total Cost: RM{total_cost}**")

        if st.button("Submit Cleaning Request"):
            if customer_name and contact_info and areas_to_clean and selected_time_slot and (selected_address or address):
                # Save and display success message, along with receipt download button.
                address = address if address else "Address selected on the map"
                pdf_buffer = generate_pdf(customer_name, contact_info, address, storey_type, booking_type, cleaning_type, areas_to_clean, total_cost, selected_date, selected_time_slot)
                st.download_button("Download Receipt", pdf_buffer, file_name="Homies_Receipt.pdf", mime='application/pdf')
                st.success(f"Request submitted! Total cost: RM{total_cost}")
            else:
                st.error("Complete all required fields (marked with *) before submitting.")
    
    display_footer()