import streamlit as st
import cv2
import numpy as np
import os
import json
import base64
from datetime import datetime
from gtts import gTTS
from io import BytesIO

st.set_page_config(page_title="Desktop Robot Companion", layout="centered")

# Storage setup
USER_DIR = "registered_users"
CHAT_FILE = "chat_history.json"

if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)

if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w") as f:
        json.dump([], f)

# Maintain active user in session state
if "active_user" not in st.session_state:
    st.session_state["active_user"] = "Micheal"

current_user = st.session_state["active_user"]

# Function to render animated SVG/CSS Robot Face
def render_robot_face(is_speaking=False):
    mouth_animation = "animation: speak 0.3s infinite alternate;" if is_speaking else ""
    
    html_code = f"""
    <style>
        .robot-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #1a1a2e;
            padding: 20px;
            border-radius: 25px;
            box-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
            margin-bottom: 20px;
        }}
        .robot-head {{
            width: 220px;
            height: 180px;
            background: #16213e;
            border: 4px solid #00ffcc;
            border-radius: 35px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-around;
            padding: 20px;
            position: relative;
        }}
        .eyes-container {{
            display: flex;
            justify-content: space-between;
            width: 140px;
        }}
        .eye {{
            width: 45px;
            height: 45px;
            background-color: #00ffcc;
            border-radius: 50%;
            box-shadow: 0 0 15px #00ffcc;
            animation: blink 4s infinite;
        }}
        .mouth {{
            width: 80px;
            height: 12px;
            background-color: #00ffcc;
            border-radius: 10px;
            box-shadow: 0 0 10px #00ffcc;
            {mouth_animation}
        }}
        @keyframes blink {{
            0%, 90%, 100% {{ transform: scaleY(1); }}
            95% {{ transform: scaleY(0.1); }}
        }}
        @keyframes speak {{
            0% {{ height: 8px; width: 70px; }}
            100% {{ height: 30px; width: 90px; border-radius: 15px; }}
        }}
    </style>
    <div class="robot-container">
        <div class="robot-head">
            <div class="eyes-container">
                <div class="eye"></div>
                <div class="eye"></div>
            </div>
            <div class="mouth"></div>
        </div>
    </div>
    """
    st.components.v1.html(html_code, height=240)

# Function to turn text into spoken audio
def speak_and_play(text):
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    audio_b64 = base64.b64encode(fp.read()).decode()
    audio_html = f'<audio autoplay src="data:audio/mp3;base64,{audio_b64}"></audio>'
    st.components.v1.html(audio_html, height=0)

# --- APP LAYOUT ---
st.title("🤖 Desktop Companion Robot")

# Select / Switch Active User
user_option = st.radio("Active User Detected:", ["Micheal", "Olivia"], horizontal=True)
st.session_state["active_user"] = user_option

# 1. Render Robot Animated Face
render_robot_face(is_speaking=st.session_state.get("speaking", False))

# 2. Chat Conversation Interface
st.markdown(f"### Chatting with **{user_option}**")

# Simple conversational response engine
def generate_robot_response(user_input, user_name):
    msg = user_input.lower()
    
    if "hello" in msg or "hi" in msg or "hey" in msg:
        if user_name == "Micheal":
            return "Hey Micheal! Good to see you back at your desk. What are we working on today?"
        else:
            return "Hi Olivia! Wonderful to see you! How is your day going?"
            
    elif "how are you" in msg:
        return f"I'm feeling great, {user_name}! All my circuits are running smoothly."
        
    elif "remind me" in msg or "task" in msg:
        return f"Got it, {user_name}! I will keep that noted in my desk memory for you."
        
    elif "bye" in msg or "goodnight" in msg:
        return f"Goodbye {user_name}! Have a fantastic rest of your day."
        
    else:
        return f"I heard you say '{user_input}', {user_name}! That sounds interesting."

# User Chat Input
user_message = st.text_input(f"Talk to your robot ({user_option}):", key="chat_input")

if st.button("Send Message"):
    if user_message:
        reply = generate_robot_response(user_message, user_option)
        
        # Trigger face animation and audio speech
        st.session_state["speaking"] = True
        st.write(f"🤖 **Robot:** {reply}")
        speak_and_play(reply)
