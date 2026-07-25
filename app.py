import streamlit as st
import cv2
import numpy as np
import os

st.set_page_config(page_title="Robot Face Scanner", layout="centered")

st.title("🤖 Desktop Robot Web Brain")
st.write("Live webcam face scanner & profile saver...")

# Create user storage directory
USER_DIR = "registered_users"
if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)

# 1. Capture live camera frame
camera_image = st.camera_input("Scan your face...")

if camera_image:
    bytes_data = camera_image.getvalue()
    cv_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # Simple image presence check
    if cv_img is not None:
        st.success(" Camera image captured successfully!")

    # 2. Save User Profile
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
