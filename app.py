import streamlit as st
import cv2
import numpy as np
import os
import urllib.request

st.set_page_config(page_title="Robot Face Scanner", layout="centered")

st.title("🤖 Desktop Robot Web Brain")
st.write("Live webcam face scanner & profile saver...")

# Create user storage directory
USER_DIR = "registered_users"
if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)

# Download the cascade XML file if it doesn't exist locally
CASCADE_FILE = "haarcascade_frontalface_default.xml"
if not os.path.exists(CASCADE_FILE):
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    urllib.request.urlretrieve(url, CASCADE_FILE)

# Load face detector safely
face_cascade = cv2.CascadeClassifier(CASCADE_FILE)

# 1. Capture live camera frame
camera_image = st.camera_input("Scan your face...")

if camera_image:
    bytes_data = camera_image.getvalue()
    cv_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    # 2. Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        st.success(f"Face detected! Found {len(faces)} person(s) in frame.")
    else:
        st.info("No face clearly detected. Center yourself in the frame.")

    # 3. Save User Profile
    st.markdown("---")
    user_name = st.text_input("Who is in the frame right now?", placeholder="Enter name (e.g., Michael or Olivia)")

    if st.button("Save Profile to Robot Memory"):
        if user_name:
            file_path = os.path.join(USER_DIR, f"{user_name.lower().strip()}.jpg")
            cv2.imwrite(file_path, cv_img)
            st.balloons()
            st.success(f"Saved profile for **{user_name}**! The robot memory is updated.")
        else:
            st.error("Please enter a name first.")
