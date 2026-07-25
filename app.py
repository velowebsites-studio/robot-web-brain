import streamlit as st
import cv2
import numpy as np
import os
import json
from datetime import datetime

st.set_page_config(page_title="Robot Web Brain", layout="centered")

st.title("🤖 Desktop Robot Dashboard")

# Storage setup
USER_DIR = "registered_users"
TASKS_FILE = "tasks.json"

if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)

if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, "w") as f:
        json.dump([], f)

# 1. Camera Capture Section
st.subheader("📸 Step 1: Face Scan")
camera_image = st.camera_input("Scan your face...")

current_user = None

if camera_image:
    bytes_data = camera_image.getvalue()
    cv_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # User Profile Saver / Active User Switch
    user_name = st.text_input("Who is in the frame right now?", placeholder="e.g., Micheal or Olivia")

    if st.button("Confirm User Profile"):
        if user_name:
            clean_name = user_name.strip().capitalize()
            file_path = os.path.join(USER_DIR, f"{clean_name.lower()}.jpg")
            cv2.imwrite(file_path, cv_img)
            current_user = clean_name
            st.success(f"Profile active: **{clean_name}**!")
        else:
            st.error("Please enter a name first.")

# 2. Personalized Greetings
st.markdown("---")
st.subheader("💬 Step 2: Robot Response")

if current_user == "Micheal":
    st.info("🤖 **Robot says:** 'Welcome back, Micheal! Ready to get to work at your desk?'")
elif current_user == "Olivia":
    st.success("🤖 **Robot says:** 'Hey Olivia! Hope you are having an amazing day!'")
elif current_user:
    st.write(f"🤖 **Robot says:** 'Hello {current_user}! Profile loaded.'")
else:
    st.write("🤖 *Awaiting face confirmation above...*")

# 3. Tasks & Alarms Manager
st.markdown("---")
st.subheader("📅 Step 3: Desk Task & Reminder Memory")

# Load existing tasks
with open(TASKS_FILE, "r") as f:
    task_list = json.load(f)

new_task = st.text_input("Add a task or alarm for the robot:", placeholder="e.g., Remind me to stretch at 3:00 PM")

if st.button("Save Task to Memory"):
    if new_task:
        timestamp = datetime.now().strftime("%I:%M %p")
        task_list.append({"user": current_user or "General", "task": new_task, "time": timestamp})
        with open(TASKS_FILE, "w") as f:
            json.dump(task_list, f)
        st.balloons()
        st.success("Task stored in memory!")

# Display stored tasks
if task_list:
    st.write("**Current Desk Reminders:**")
    for item in task_list:
        st.write(f"- [{item['time']}] **{item['user']}**: {item['task']}")
