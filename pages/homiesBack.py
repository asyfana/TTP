import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
data = pd.read_csv(r"C:\Users\Asus\Downloads\TTP Codings\sales_data.csv")
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


