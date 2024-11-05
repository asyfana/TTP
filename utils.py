import streamlit as st
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def get_available_slots(date):
    all_slots = [f"{hour}:00 - {hour + 1}:00" for hour in range(9, 17)]
    booked_slots = ["11:00 - 12:00", "14:00 - 15:00"] if date == datetime.now().date() else []
    return [slot for slot in all_slots if slot not in booked_slots]

def calculate_cost(storey_type, areas_to_clean, booking_type, cleaning_type):
    base_cost = 50 if cleaning_type == "Standard Cleaning" else 100
    area_cost = len(areas_to_clean) * 10
    total_cost = base_cost + area_cost
    if booking_type == "Weekly Booking":
        total_cost *= 4  # Assuming 4 weeks in a month
    if storey_type == "Double Storey":
        total_cost += 50
    return total_cost

def generate_pdf(customer_name, contact_info, address, storey_type, booking_type, cleaning_type, areas_to_clean, total_cost, selected_date, selected_time_slot):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Add logo
    logo_path = "homies.jpg"
    c.drawImage(logo_path, 500, 700, width=1*inch, height=1*inch)
    
    # Add title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Homies: Cleaning Service Receipt")
    
    # Add customer details
    c.setFont("Helvetica", 12)
    details = [
        f"Customer Name: {customer_name}",
        f"Contact Info: {contact_info}",
        f"Address: {address}",
        f"House Type: {storey_type}",
        f"Booking Type: {booking_type}",
        f"Cleaning Type: {cleaning_type}",
        "Areas to Clean: " + ", ".join(areas_to_clean),
        f"Total Cost: RM{total_cost}",
        f"Preferred Date: {selected_date}",
        f"Preferred Time Slot: {selected_time_slot}"
    ]
    
    y = 730
    for detail in details:
        c.drawString(100, y, detail)
        y -= 20

    # Add footer
    c.setFont("Helvetica-Oblique", 10)
    footer_text = [
        "Thank you for using our service!",
        "We appreciate your business and look forward to serving you again.",
        "For any inquiries, please contact us at support@homies.com or call +60 123-456-789."
    ]
    
    y = 50
    for line in footer_text:
        c.drawString(100, y, line)
        y -= 15

    # Save the PDF
    c.save()
    buffer.seek(0)
    return buffer

def display_footer():
    footer = """
    <div style="width: 100%; text-align: center; padding: 10px; font-size: 12px; margin-top: 20px;">
        <p>Homies is part of Homies Holdings Inc., a leader in household services.<br>
        &copy; 2023 Homies™. All rights reserved.</p>
        <p><a href="/terms-and-conditions" style="color: #1E90FF;">Terms and Conditions</a></p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)
