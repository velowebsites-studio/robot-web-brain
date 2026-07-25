import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import os

# Set up page title and layout
st.set_page_config(page_title="Robot Face & Emotion Scanner", layout="centered")

st.title("🤖 Desktop Robot Web Brain")
st.write("Auto-scanning webcam for faces and emotional states...")

# Create directory to store user profiles if it doesn't exist
USER_DIR = "registered_users"
if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)

# 1. Capture live camera frame directly in the browser
camera_image = st.camera_input("Scanning face...")

if camera_image:
    # Convert image buffer to OpenCV format
    bytes_data = camera_image.getvalue()
    cv_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # 2. Analyze Facial Expression / Emotion
    try:
        analysis = DeepFace.analyze(cv_img, actions=['emotion'], enforce_detection=True)
        dominant_emotion = analysis[0]['dominant_emotion']
        
        # Display detected emotion status
        st.subheader(f"Detected Mood: **{dominant_emotion.capitalize()}**")

        # Custom responses based on emotional state
        if dominant_emotion in ['sad', 'fear', 'angry']:
            st.warning("You seem a bit stressed or overwhelmed today. Take a quick breather!")
        elif dominant_emotion == 'happy':
            st.success("You look like you're in a great mood today!")
        else:
            st.info("Real-time emotion scan complete.")

    except Exception as e:
        st.write("No face detected clearly yet. Please center yourself in the frame.")

    # 3. Name Registration Flow
    st.markdown("---")
    user_name = st.text_input("Who is in the frame right now?", placeholder="Enter your name (e.g., Michael, Olivia)")

    if st.button("Save Profile to Robot Memory"):
        if user_name:
            user_path = os.path.join(USER_DIR, f"{user_name.lower().strip()}.jpg")
            cv2.imwrite(user_path, cv_img)
            st.success(f"Saved facial profile for **{user_name}**! The robot will remember you now.")
        else:
            st.error("Please enter a name before saving.")
