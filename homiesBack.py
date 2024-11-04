import streamlit as st
#import gspread
#from oauth2client.service_account import ServiceAccountCredentials
#from datetime import datetime

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import streamlit as st
import warnings
import sys
import datetime
from datetime import datetime

warnings.filterwarnings("ignore")

# st.title("Welcome Boss!")
# df = pd.read_excel(r"C:\Users\Asus\Downloads\TTP Codings\Homies_users_Database.xlsx")
# df= df.reset_index(drop=True)
# df


# Load the data (replace 'sales_data.csv' with your actual file path)
data = pd.read_csv(r"sales_data.csv")
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# Extract year and month columns for filtering
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month

# Title
st.title("Homies Backend Sales Dashboard")

# Filter Section on Main Page
st.subheader("Filter Options")

# Year Selection
selected_year = st.selectbox("Select Year", sorted(data['Year'].dropna().unique()), index=0)

# Month Selection (optional)
months = ["All"] + [datetime(2024, m, 1).strftime('%B') for m in range(1, 13)]
selected_month = st.selectbox("Select Month", months)

# Filter data based on selections
if selected_month != "All":
    filtered_data = data[(data['Year'] == selected_year) & (data['Month'] == months.index(selected_month))]
else:
    filtered_data = data[data['Year'] == selected_year]

# Generate the line chart of sales over time
st.subheader("Sales Trend")
daily_sales = filtered_data.groupby('Date')['Sales'].sum()
st.line_chart(daily_sales)

# Show total sales for the selected period
total_sales = daily_sales.sum()
st.subheader(f"Total Sales for {selected_month} {selected_year}" if selected_month != "All" else f"Total Sales for {selected_year}")
st.write(f"${total_sales}")

# Display Raw Data Table
st.subheader("Raw Data")
st.write(filtered_data[['Date', 'Service', 'ServiceProvider', 'Sales']])

# Top 5 Most Popular Services
st.subheader("Top 5 Most Popular Services")
service_counts = filtered_data['Service'].value_counts().nlargest(5)
st.bar_chart(service_counts)

# Revenue by Service Category
st.subheader("Revenue by Service Category")
revenue_by_service = filtered_data.groupby('Service')['Sales'].sum()
st.bar_chart(revenue_by_service)

# Customer Booking Patterns by Day of the Week
st.subheader("Booking Patterns by Day of the Week")
filtered_data['DayOfWeek'] = filtered_data['Date'].dt.day_name()
day_of_week_counts = filtered_data['DayOfWeek'].value_counts()
st.bar_chart(day_of_week_counts)

# Service Provider Performance
st.subheader("Service Provider Performance")
provider_performance = filtered_data.groupby('ServiceProvider')['Sales'].sum()
st.bar_chart(provider_performance)




# # Google Sheets authentication
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", 
#          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# # Load your credentials from the downloaded JSON file
# creds = ServiceAccountCredentials.from_json_keyfile_name("path_to_credentials.json", scope)
# client = gspread.authorize(creds)

# # Access your Google Sheet
# sheet = client.open("Homies_Service_App").sheet1  # Sheet name or ID

# # Mock data for services and service providers
# services = ["Mopping", "Living Room Cleaning", "Folding Clothes", "Plumbi  ng", "Electrician"]
# service_providers = {
#     "Mopping": ["John", "Emily", "Sarah"],
#     "Living Room Cleaning": ["Alice", "David"],
#     "Folding Clothes": ["Mila", "Sophie"],
#     "Plumbing": ["Mike", "Tom"],
#     "Electrician": ["Henry", "Liam"]
# }

# # User roles
# roles = ['Customer', 'Service Provider']

# # User authentication (mock)
# def authenticate_user(username, password):
#     if username == "user" and password == "password":
#         return True
#     else:
#         return False

# # Function to save booking to Google Sheets
# def save_booking_to_google_sheets(username, service, provider, location, date, time):
#     # Append data to Google Sheets
#     sheet.append_row([username, service, provider, location, str(date), str(time)])
#     st.success(f"Service booked with {provider} at {location} on {date} at {time}.")

# # Function to retrieve booking history from Google Sheets
# def view_booking_history(username):
#     records = sheet.get_all_records()
#     user_bookings = [record for record in records if record['username'] == username]

#     if user_bookings:
#         for booking in user_bookings:
#             st.write(f"Service: {booking['service']}, Provider: {booking['provider']}, Location: {booking['location']}, "
#                      f"Date: {booking['date']}, Time: {booking['time']}")
#     else:
#         st.info("No booking history found.")

# # Main Streamlit App
# def main():
#     st.title("Homies: Household Services App")

#     # Sidebar for login/signup
#     st.sidebar.title("Login/Signup")
#     role = st.sidebar.radio("Select your role", roles)

#     username = st.sidebar.text_input("Username")
#     password = st.sidebar.text_input("Password", type="password")

#     if st.sidebar.button("Sign In"):
#         if authenticate_user(username, password):
#             st.sidebar.success(f"Welcome, {username}!")
#             if role == "Customer":
#                 customer_dashboard(username)
#             elif role == "Service Provider":
#                 provider_dashboard(username)
#         else:
#             st.sidebar.error("Invalid credentials")

#     elif st.sidebar.button("Sign Up"):
#         st.sidebar.info("Sign-up feature coming soon!")

# # Customer Dashboard
# def customer_dashboard(username):
#     st.header(f"Welcome, {username}!")

#     # Booking options
#     st.subheader("Book a Service")
#     service_choice = st.selectbox("Select a service", services)

#     # Display available service providers for selected service
#     if service_choice:
#         providers = service_providers.get(service_choice, [])
#         selected_provider = st.selectbox("Select a service provider", providers)

#         # Schedule booking
#         if selected_provider:
#             st.write(f"Selected Provider: {selected_provider}")

#             # Get location
#             user_location = st.text_input("Enter your location")
#             appointment_time = st.time_input("Select a time")
#             appointment_date = st.date_input("Select a date", datetime.now())

#             if st.button("Confirm Booking"):
#                 if user_location and appointment_time and appointment_date:
#                     # Save booking to Google Sheets
#                     save_booking_to_google_sheets(username, service_choice, selected_provider, user_location, appointment_date, appointment_time)
#                 else:
#                     st.error("Please fill all fields to confirm the booking.")

#     # View booking history
#     st.subheader("Your Bookings")
#     if st.button("View Booking History"):
#         view_booking_history(username)

# # Service Provider Dashboard
# def provider_dashboard(username):
#     st.header(f"Welcome, {username} (Service Provider)!")

#     # Registration as a service provider
#     st.subheader("Register Your Services")
#     provider_services = st.multiselect("Select services you can provide", services)

#     if st.button("Register Services"):
#         if provider_services:
#             st.success(f"Services registered: {', '.join(provider_services)}.")
#         else:
#             st.error("Please select at least one service.")

#     # View available jobs
#     st.subheader("Available Jobs")
#     if st.button("Search for Jobs"):
#         st.info("Available jobs feature coming soon!")

#     # View accepted jobs
#     st.subheader("View Accepted Jobs")
#     if st.button("View Accepted Jobs"):
#         st.info("Accepted jobs feature coming soon!")

#     # Start a job
#     st.subheader("Start Job")
#     if st.button("Start Job"):
#         st.info("Job starting feature coming soon!")

# # Entry point
# if __name__ == "__main__":
#     main()
