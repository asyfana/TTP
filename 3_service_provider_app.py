import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_calendar import calendar


# Sample data storage (mock data)
services = [
    {"id": 1, "type": "Cleaning House", "description": "Thorough cleaning service for homes.", "provider": "Alice"},
    {"id": 2, "type": "Fix Electricity", "description": "Electrical repairs and installations.", "provider": "Bob"},
    {"id": 3, "type": "Plumbing", "description": "Plumbing services for pipes, sinks, and toilets.", "provider": "Charlie"}
]

requests = [
    {"id": 1, "service_id": 1, "client": "John", "requested_time": "2024-10-25 10:00", "status": "Pending"},
    {"id": 2, "service_id": 2, "client": "Eve", "requested_time": "2024-10-26 14:00", "status": "Pending"},
    {"id": 3, "service_id": 3, "client": "Mike", "requested_time": "2024-10-27 09:00", "status": "Pending"}
]

accepted_jobs = [
    {"id": 1, "service_id": 1, "client": "Sarah", "requested_time": "2024-10-23 08:00", "status": "Approved"},
    {"id": 2, "service_id": 2, "client": "David", "requested_time": "2024-10-24 11:00", "status": "Approved"},
    {"id": 3, "service_id": 3, "client": "Jane", "requested_time": "2024-10-25 15:00", "status": "Approved"}
]

cancellation_notifications = [
    {
        "id": 1,
        "service_id": 1,
        "client": "Alice",
        "reason": "Unexpected personal emergency",
        "cancellation_time": "2024-10-28 09:00"
    },
    {
        "id": 2,
        "service_id": 2,
        "client": "Bob",
        "reason": "Found another provider with lower cost",
        "cancellation_time": "2024-10-29 14:30"
    },
    {
        "id": 3,
        "service_id": 3,
        "client": "Charlie",
        "reason": "Schedule conflict",
        "cancellation_time": "2024-10-30 16:45"
    }
]

# Helper functions to simulate database operations
def get_service_by_id(service_id):
    for service in services:
        if service["id"] == service_id:
            return service
    return None

# UI for service providers
st.title("Household Service Provider App")

st.sidebar.header("Menu")
menu = st.sidebar.selectbox("Choose an option", [
    "Register Service", 
    "Service Requests", 
    "Accepted Jobs", 
    "Attach Evidence & Receive Payment", 
    "Cancellation Notifications",
    "Calendar"
])

# 1. Register Service Page
if menu == "Register Service":
    st.header("Register Your Household Service")
    service_type = st.selectbox("Choose service type", ["Cleaning House", "Fix Electricity", "Plumbing", "Gardening", "Other"])
    other_service_type = ""
    
    # Display an input box if 'Other' is selected
    if service_type == "Other":
        other_service_type = st.text_input("Please specify your service type")
    
    description = st.text_area("Service Description")
    provider_name = st.text_input("Your Name")
    
    if st.button("Register Service"):
        selected_service_type = other_service_type if service_type == "Other" else service_type
        if selected_service_type and description and provider_name:
            services.append({
                "id": len(services) + 1,
                "type": selected_service_type,
                "description": description,
                "provider": provider_name
            })
            st.success("Service registered successfully!")
        else:
            st.warning("Please fill all the fields!")


# 2. Page for Service Requests
elif menu == "Service Requests":
    st.header("View Service Requests from Clients")
    if requests:
        for request in requests:
            service = get_service_by_id(request["service_id"])
            if service:
                # Create a bordered section for each request with a gray border
                st.markdown(
                    f"""
                    <div style="border: 2px solid gray; padding: 10px; margin: 10px 0;">
                        <strong>Service:</strong> {service['type']} - {service['description']}<br>
                        <strong>Client:</strong> {request['client']}, <strong>Requested Time:</strong> {request['requested_time']}<br>
                    """,
                    unsafe_allow_html=True
                )

                # Unique keys for radio buttons and input fields
                action = st.radio(f"Action for Request {request['id']}", ["Approve", "Reject"], key=f"action_{request['id']}")
                if action == "Reject":
                    reason = st.text_input(f"Reason for rejection (Request {request['id']})", key=f"reason_{request['id']}_reason")

                if st.button(f"Submit Request {request['id']}", key=f"submit_{request['id']}"):
                    if action == "Approve":
                        request["status"] = "Approved"
                        st.success(f"Request {request['id']} approved.")
                    elif action == "Reject" and reason:
                        request["status"] = "Rejected"
                        st.warning(f"Request {request['id']} rejected with reason: {reason}")
                
                st.markdown("</div>", unsafe_allow_html=True)  # Closing the div for the request



# 3. Accepted Jobs Page
elif menu == "Accepted Jobs":
    st.header("Check and Manage Accepted Jobs")
    if accepted_jobs:
        for job in accepted_jobs:
            service = get_service_by_id(job["service_id"])
            if service and job["status"] == "Approved":
                st.markdown(
                    f"""
                    <div style="border: 2px solid gray; padding: 10px; margin: 10px 0;">
                        <strong>Service:</strong> {service['type']} - {service['description']}<br>
                        <strong>Client:</strong> {job['client']}, <strong>Scheduled Time:</strong> {job['requested_time']}<br>
                    """,
                    unsafe_allow_html=True
                )
                
                new_time = st.date_input(f"Reschedule Job {job['id']}", value=datetime.now())
                if st.button(f"Reschedule {job['id']}"):
                    job["requested_time"] = new_time.strftime("%Y-%m-%d %H:%M")
                    st.success(f"Job {job['id']} rescheduled to {job['requested_time']}")
                
                st.markdown("</div>", unsafe_allow_html=True)  # Closing the div for the job


# 4. Attach Evidence & Receive Payment Page
elif menu == "Attach Evidence & Receive Payment":
    st.header("Attach Evidence of Work & Receive Payment")
    if accepted_jobs:
        for job in accepted_jobs:
            if job["status"] == "Approved":
                service = get_service_by_id(job["service_id"])
                st.markdown(
                    f"""
                    <div style="border: 2px solid gray; padding: 10px; margin: 10px 0;">
                        <strong>Service:</strong> {service['type']} - {service['description']}<br>
                        <strong>Client:</strong> {job['client']}
                    """,
                    unsafe_allow_html=True
                )
                
                # File input for work evidence
                screenshot = st.file_uploader(f"Upload Evidence Screenshot for Job {job['id']}", type=["jpg", "png"])
                
                # Additional file input for payment evidence
                payment_evidence = st.file_uploader(f"Upload Payment Evidence for Job {job['id']}", type=["jpg", "png", "pdf"], key=f"payment_{job['id']}")

                if st.button(f"Confirm Job Completion {job['id']}"):
                    if screenshot and payment_evidence:
                        st.image(screenshot)
                        st.success("Evidence uploaded. Payment will be processed.")
                    elif not screenshot:
                        st.warning("Please upload work evidence screenshot.")
                    elif not payment_evidence:
                        st.warning("Please upload payment evidence.")
                
                st.markdown("</div>", unsafe_allow_html=True)  # Closing the div for the job



# 5. Cancellation Notifications Page
elif menu == "Cancellation Notifications":
    st.header("Cancellation Notifications")
    if cancellation_notifications:
        for cancellation in cancellation_notifications:
            service = get_service_by_id(cancellation["service_id"])
            if service:
                st.markdown(
                    f"""
                    <div style="border: 2px solid gray; padding: 10px; margin: 10px 0;">
                        <strong>Service:</strong> {service['type']} - {service['description']}<br>
                        <strong>Client:</strong> {cancellation['client']}<br>
                        <strong>Reason for Cancellation:</strong> {cancellation['reason']}
                    """,
                    unsafe_allow_html=True
                )
                
                if st.button(f"Acknowledge Cancellation {cancellation['id']}"):
                    st.info(f"Cancellation by {cancellation['client']} acknowledged.")
                
                st.markdown("</div>", unsafe_allow_html=True)  # Closing the div for the notification


# New: Calendar Page
if menu == "Calendar":

    # Preparing calendar events with brief titles only
    events = []
    detailed_info = {}

    for job in accepted_jobs:
        service = get_service_by_id(job["service_id"])
        if service:
            event_date = datetime.strptime(job["requested_time"], "%Y-%m-%d %H:%M")
            
            # Short description for the calendar
            events.append({
                "title": f"{service['type']}",
                "start": event_date.isoformat(),
                "end": (event_date + timedelta(hours=2)).isoformat(),  # Assuming each job takes 2 hours
            })
            
            # Detailed job info to be displayed outside the calendar
            detailed_info[event_date.date()] = detailed_info.get(event_date.date(), []) + [{
                "Client": job["client"],
                "Type": service["type"],
                "Time": event_date.strftime('%I:%M %p'),
                "Details": f"Service for {service['type']}, requested by {job['client']}."
            }]

    # Display the calendar with only short descriptions
    st.header("Manage Schedule with Calendar")
    calendar(events=events)

    # Display detailed job information below the calendar
    st.subheader("Detailed Job Information")
    for date, jobs in detailed_info.items():
        st.write(f"**{date.strftime('%B %d, %Y')}**")
        for job in jobs:
            st.write(f"- **{job['Time']}**: {job['Details']}")
