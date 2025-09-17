import streamlit as st
import pandas as pd
import random
import speech_recognition as sr
from datetime import datetime
import os
import altair as alt
import uuid

# --- PAGE CONFIG ---
st.set_page_config(page_title="Emergency Alert System", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.signed_up = False
    st.session_state.alert_count = 0
    st.session_state.alert_locations = []

# --- CSV VALIDATION AND RESET ---
def validate_and_reset_csv():
    expected_columns = ["Message", "Department", "Location", "Timestamp", "Priority"]
    if os.path.exists("emergency_log.csv"):
        try:
            log_df = pd.read_csv("emergency_log.csv")
            log_df.columns = log_df.columns.str.strip()
            if log_df.columns.tolist() != expected_columns:
                st.warning("Detected incompatible CSV format. Resetting emergency_log.csv to match new structure.")
                os.remove("emergency_log.csv")
                st.session_state.alert_count = 0
                st.session_state.alert_locations = []
                return False
            return True
        except Exception as e:
            st.warning(f"Error reading emergency_log.csv: {str(e)}. Resetting the file.")
            os.remove("emergency_log.csv")
            st.session_state.alert_count = 0
            st.session_state.alert_locations = []
            return False
    return False

# --- LOGIN/SIGNUP PAGE ---
def show_login_page():
    st.title("🔐 Login / Sign Up")
    login_option = st.radio("Select an option:", ["Login", "Sign Up"])

    if login_option == "Sign Up":
        new_username = st.text_input("Create a username")
        new_password = st.text_input("Create a password", type="password")
        aadhaar = st.text_input("Enter your Aadhaar Number (Mock Validation)")
        if st.button("Submit Sign Up"):
            if len(aadhaar) == 12 and aadhaar.isdigit():
                st.success("✅ Sign-up successful. Please login to continue.")
                st.session_state.signed_up = True
            else:
                st.error("❌ Invalid Aadhaar number. Must be 12 digits.")

    if login_option == "Login" or st.session_state.get("signed_up"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.success("✅ Logged in successfully as Admin")
                st.rerun()
            else:
                st.warning("❌ Incorrect username or password")

# --- MAIN INTERFACE ---
def show_main_interface():
    # Validate CSV at the start of the main interface
    validate_and_reset_csv()

    # --- SIDEBAR INFO ---
    st.sidebar.title("📘 About ")
    st.sidebar.markdown("""
        **Emergency Alert System** 
        This intelligent tool uses **NLP** and **voice input** to detect whether a person is in an **emergency situation** and simulate sending **location-based alerts**.

        ### What It Solves:
        - Detects messages containing **danger/emergency keywords** (e.g., "stuck in a remote place")
        - Assigns **priority levels** to alerts
        - Accepts **text or speech**
        - Shares **simulated GPS location**
        - Informs relevant **emergency departments**
        - Includes a **map**, **alert frequency chart**, and **alert history summary**
        - **Future Support for Haptic Feedback Alerts (for mobile use)**
        - **New: Filterable logs, downloadable logs, department-based charts, and log clearing**
    """)
    # Logout Button
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.signed_up = False
        st.rerun()

    # --- TITLE ---
    st.title("Emergency Alert System")
    st.markdown("Check messages for emergency indicators and simulate notifying the authorities.")

    # --- INPUT AREA ---
    st.subheader("Receive a Message")
    input_method = st.radio("Choose input type:", ["Type a message", "Use your voice"])
    message = ""
    emergency_contacts = [
        "🔥 Fire Department (101)",
        "🚑 Accident Control (102)",
        "🏥 Ambulance (102)",
        "🆘 General Emergency (112)",
        "🚓 Police Department",
        "🌍 Disaster Response - Earthquake Unit",
        "🌊 Disaster Response - Flood Relief",
        "⛰️ Disaster Response - Geological Unit",
        "🌪️ Disaster Response - Weather Unit",
        "🌊 Coastal Emergency Services",
        "🏗️ Structural Emergency Rescue"
    ]
    selected_contacts = st.multiselect("Select Emergency Contacts to Notify (Optional):", emergency_contacts)

    if input_method == "Type a message":
        user_input = st.text_area("Type your message below:")
        if st.button("🔍 Analyze Message"):
            message = user_input
    else:
        if st.button("Start Voice Input"):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                st.info("🎤 Listening for 5 seconds...")
                audio = recognizer.listen(source, phrase_time_limit=5)
                try:
                    message = recognizer.recognize_google(audio)
                    st.success(f"You said: '{message}'")
                except:
                    st.error("❌ Could not recognize your voice.")
                    message = ""

    # --- EMERGENCY CHECK ---
    if message:
        emergency_keywords = {
            "fire": "🔥 Fire Department (101)",
            "burn": "🔥 Fire Department (101)",
            "blast": "🔥 Fire Department (101)",
            "accident": "🚑 Accident Control (102)",
            "injured": "🏥 Ambulance (102)",
            "hurt": "🏥 Ambulance (102)",
            "help": "🆘 General Emergency (112)",
            "emergency": "⚠️ Emergency",
            "stuck": "🆘 Rescue",
            "save": "🆘 Rescue",
            "rescue": "🆘 Rescue",
            "remote": "🆘 Rescue",
            "danger": "⚠️ Emergency",
            "heart": "🏥 Ambulance",
            "attack": "🏥 Ambulance",
            "robbery": "🚓 Police Department",
            "thief": "🚓 Police Department",
            "earthquake": "🌍 Disaster Response - Earthquake Unit",
            "quake": "🌍 Disaster Response - Earthquake Unit",
            "flood": "🌊 Disaster Response - Flood Relief",
            "water": "🌊 Flood Relief",
            "landslide": "⛰️ Disaster Response - Geological Unit",
            "rockfall": "⛰️ Disaster Response - Geological Unit",
            "cyclone": "🌪️ Disaster Response - Weather Unit",
            "storm": "⛈️ Disaster Response - Weather Department",
            "wind": "⛈️ Weather Department",
            "tsunami": "🌊 Coastal Emergency Services",
            "wave": "🌊 Coastal Emergency Services",
            "collapse": "🏗️ Structural Emergency Rescue",
            "building": "🏗️ Structural Emergency Rescue",
            "fallen": "🏗️ Structural Emergency Rescue"
        }

        matched_departments = [dept for k, dept in emergency_keywords.items() if k in message.lower()]
        matched_departments = list(set(matched_departments + selected_contacts))

        if matched_departments:
            st.error("Emergency detected!")
            # Determine Priority Level
            keyword_count = sum(1 for k in emergency_keywords if k in message.lower())
            if keyword_count >= 3:
                priority = "High"
                priority_icon = "🔴"
            elif keyword_count == 2:
                priority = "Medium"
                priority_icon = "🟡"
            else:
                priority = "Low"
                priority_icon = "🟢"
            st.markdown(f"⚠️ **Priority Level:** {priority_icon} {priority}")

            st.success("Alert sent to emergency services!", icon="🚨")

            lat = 28.60 + random.uniform(-0.01, 0.01)
            lon = 77.20 + random.uniform(-0.01, 0.01)
            st.session_state.alert_count += 1
            st.session_state.alert_locations.append((lat, lon))

            st.markdown(f"📤 **Message Sent:** _{message}_")
            st.markdown(f"📍 **Simulated Location:** `{lat:.4f}, {lon:.4f}`")

            st.markdown("📞 **Alerted Departments:**")
            for dept in matched_departments:
                st.markdown(f"- {dept}")

            st.subheader("🗺️ Alert Location Map")
            df_map = pd.DataFrame([[lat, lon]], columns=['lat', 'lon'])
            st.map(df_map, zoom=15)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for dept in matched_departments:
                log_entry = pd.DataFrame([[message, dept, f"{lat:.4f}, {lon:.4f}", timestamp, priority]],
                                        columns=["Message", "Department", "Location", "Timestamp", "Priority"])
                log_entry.to_csv("emergency_log.csv", mode='a',
                                header=not os.path.exists("emergency_log.csv"), index=False)

            st.success("📝 Emergency logged successfully.")
        else:
            st.success("✅ No emergency detected in the message.")

    # --- SIDEBAR METRICS ---
    st.sidebar.metric("🚨 Alerts Triggered", st.session_state.alert_count)

    # --- LAST LOCATION INFO ---
    if st.session_state.alert_locations:
        st.subheader("📍 Last Alert Location")
        lat, lon = st.session_state.alert_locations[-1]
        st.markdown(f"📌 **Lat, Lon:** `{lat:.4f}, {lon:.4f}`")

    # --- ALERT HISTORY SUMMARY ---
    st.markdown("---")
    st.header("📈 Alert History Summary")
    if os.path.exists("emergency_log.csv"):
        try:
            log_df = pd.read_csv("emergency_log.csv")
            log_df.columns = log_df.columns.str.strip()
            expected_columns = ["Message", "Department", "Location", "Timestamp", "Priority"]
            if log_df.columns.tolist() != expected_columns:
                st.warning("Detected incompatible CSV format in summary. Resetting emergency_log.csv.")
                os.remove("emergency_log.csv")
                st.session_state.alert_count = 0
                st.session_state.alert_locations = []
                st.rerun()
            summary_df = log_df.groupby("Department").size().reset_index(name="Alert Count")
            st.dataframe(summary_df)
        except Exception as e:
            st.warning(f"Error reading emergency_log.csv for summary: {str(e)}. Resetting the file.")
            os.remove("emergency_log.csv")
            st.session_state.alert_count = 0
            st.session_state.alert_locations = []
            st.rerun()

    # --- LOG VIEW ---
    st.markdown("---")
    st.header("📂 View Emergency Logs")
    if os.path.exists("emergency_log.csv"):
        try:
            log_df = pd.read_csv("emergency_log.csv")
            log_df.columns = log_df.columns.str.strip()
            expected_columns = ["Message", "Department", "Location", "Timestamp", "Priority"]
            if log_df.columns.tolist() != expected_columns:
                st.warning("Detected incompatible CSV format in logs. Resetting emergency_log.csv.")
                os.remove("emergency_log.csv")
                st.session_state.alert_count = 0
                st.session_state.alert_locations = []
                st.rerun()

            # Filter Logs
            st.subheader("🔍 Filter Logs")
            filter_keyword = st.text_input("Search by Message Keyword")
            filter_department = st.selectbox("Filter by Department", ["All"] + sorted(log_df["Department"].unique()))
            filter_priority = st.selectbox("Filter by Priority", ["All"] + sorted(log_df["Priority"].unique()))
            filtered_df = log_df
            if filter_keyword:
                filtered_df = filtered_df[filtered_df["Message"].str.contains(filter_keyword, case=False, na=False)]
            if filter_department != "All":
                filtered_df = filtered_df[filtered_df["Department"] == filter_department]
            if filter_priority != "All":
                filtered_df = filtered_df[filtered_df["Priority"] == filter_priority]
            
            st.dataframe(filtered_df)

            # Export Logs
            st.subheader("💾 Export Logs")
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download Filtered Emergency Logs",
                data=csv,
                file_name="emergency_log_export.csv",
                mime="text/csv"
            )

            # Clear Logs
            st.subheader("🗑️ Clear Logs")
            if st.button("Clear Emergency Logs"):
                try:
                    os.remove("emergency_log.csv")
                    st.session_state.alert_count = 0
                    st.session_state.alert_locations = []
                    st.success("✅ Emergency logs cleared successfully.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error clearing logs: {str(e)}")
        except Exception as e:
            st.warning(f"Error reading emergency_log.csv: {str(e)}. Resetting the file.")
            os.remove("emergency_log.csv")
            st.session_state.alert_count = 0
            st.session_state.alert_locations = []
            st.rerun()
    else:
        st.info("No logs found yet.")

    # --- ALERT FREQUENCY CHART ---
    st.markdown("---")
    st.header("📊 Real-Time Alert Frequency by Department")
    if os.path.exists("emergency_log.csv"):
        try:
            log_df = pd.read_csv("emergency_log.csv")
            log_df.columns = log_df.columns.str.strip()
            expected_columns = ["Message", "Department", "Location", "Timestamp", "Priority"]
            if log_df.columns.tolist() != expected_columns:
                st.warning("Detected incompatible CSV format in chart. Resetting emergency_log.csv.")
                os.remove("emergency_log.csv")
                st.session_state.alert_count = 0
                st.session_state.alert_locations = []
                st.rerun()
            log_df['Timestamp'] = pd.to_datetime(log_df['Timestamp'], format='%Y-%m-%d %H:%M:%S')
            log_df['Hour-Minute'] = log_df['Timestamp'].dt.strftime('%H:%M')
            chart_data = log_df.groupby(['Hour-Minute', 'Department']).size().reset_index(name='Alerts')
            chart = alt.Chart(chart_data).mark_line(point=True).encode(
                x='Hour-Minute',
                y='Alerts',
                color='Department:N',
                tooltip=['Hour-Minute', 'Department', 'Alerts']
            ).properties(width=700, height=400, title="Number of Alerts by Department Over Time")
            st.altair_chart(chart, use_container_width=True)
        except Exception as e:
            st.warning(f"Error processing alert frequency chart: {str(e)}. Resetting the file.")
            os.remove("emergency_log.csv")
            st.session_state.alert_count = 0
            st.session_state.alert_locations = []
            st.rerun()
    else:
        st.info("No alert data available to display chart.")

    # --- FOOTER ---
    st.markdown("---")
    st.markdown("🔧 | Powered by NLP, Speech Recognition, Simulated GPS & Realtime Dashboards")

# --- MAIN APP LOGIC ---
if not st.session_state.logged_in:
    show_login_page()
else:
    show_main_interface()