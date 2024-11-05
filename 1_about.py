import streamlit as st
import folium
from streamlit_folium import st_folium
from PIL import Image
from utils import display_footer

def about_page():
    # Page Title and Subtitle
    st.markdown("<h1 style='text-align: center; font-size: 2.8em;'>Welcome to Homies</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Your Trusted Cleaning Partner</h3>", unsafe_allow_html=True)
    st.write(
        "<p style='text-align: center; font-size: 1.2em; color: #666;'>Exceptional quality and reliability for household cleaning services in Kuala Lumpur.</p>",
        unsafe_allow_html=True
    )

    # Use columns for a structured, clean look
    col1, col2 = st.columns(2, gap="large")
    
    # Column 1: Company Info
    with col1:
        st.markdown("<h4 style='color: #333;'>Our Story</h4>", unsafe_allow_html=True)
        st.write("Homies was founded with the mission to bring comfort and cleanliness into every home.")
        
        st.markdown("<h4 style='color: #333; margin-top: 1em;'>Our Mission</h4>", unsafe_allow_html=True)
        st.write("To provide high-quality, reliable, and affordable household services that make life easier and homes sparkle.")

    # Column 2: Map with customized style
    with col2:
        st.markdown("<h4>Our Location</h4>", unsafe_allow_html=True)
        st.write("Headquartered in the bustling Kuala Lumpur City Centre (KLCC), Malaysia.")
        
        # Map setup with rounded corners
        klcc_location = [3.1579, 101.7123]
        m = folium.Map(location=klcc_location, zoom_start=15)
        folium.Marker(klcc_location, tooltip="Homies Headquarters", icon=folium.Icon(color="blue")).add_to(m)

        # Display map with rounded borders
        st_folium(m, width=360, height=240)
    
    # Testimonials section with cleaner layout
    st.markdown("<h3 style='text-align: center; margin-top: 40px;'>What Our Clients Say</h3>", unsafe_allow_html=True)
    
    # Use columns for testimonials with consistent styling
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("⭐️⭐️⭐️⭐️⭐️")
        st.write('"Fantastic service! My house has never been this clean."')
        st.write("<i>- Sarah L.</i>", unsafe_allow_html=True)
    with col2:
        st.write("⭐️⭐️⭐️⭐️⭐️")
        st.write('"Professional and thorough. Highly recommend!"')
        st.write("<i>- John D.</i>", unsafe_allow_html=True)
    with col3:
        st.write("⭐️⭐️⭐️⭐️⭐️")
        st.write('"Timely and efficient. I’m a repeat customer!"')
        st.write("<i>- Anna K.</i>", unsafe_allow_html=True)
    
    # Call-to-action Button with centered alignment and better styling
    st.markdown(
        """
        <div style='text-align: center; margin-top: 50px;'>
            <h2 style='font-size: 1.8em;'>Ready for a Sparkling Clean Home?</h2>
            <a href='#' style='background-color: #1E90FF; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-size: 1.2em;'>Book Now</a>
        </div>
        """, 
        unsafe_allow_html=True
    )

    display_footer()