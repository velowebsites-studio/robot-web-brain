import streamlit as st
import cv2
import numpy as np
import os
import json

st.set_page_config(page_title="Desktop Robot Companion", layout="centered")

# Maintain active user in session state
if "active_user" not in st.session_state:
    st.session_state["active_user"] = "Micheal"

current_user = st.session_state["active_user"]

# Function to render cute 3D White Robot Face matching your picture
def render_robot_face(is_speaking=False):
    mouth_style = "height: 18px; width: 60px; border-radius: 0 0 20px 20px;" if is_speaking else "height: 8px; width: 45px; border-radius: 10px;"
    
    html_code = f"""
    <style>
        .robot-stage {{
            display: flex;
            justify-content: center;
            align-items: center;
            background: radial-gradient(circle, #2c302e 0%, #0f1110 100%);
            padding: 30px;
            border-radius: 30px;
            margin-bottom: 20px;
        }}
        .robot-head-outer {{
            width: 220px;
            height: 200px;
            background: linear-gradient(145deg, #ffffff, #dcdcdc);
            border-radius: 80px 80px 70px 70px;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5), inset 0 5px 10px #ffffff;
        }}
        /* Left Ear Nodule */
        .robot-head-outer::before {{
            content: '';
            position: absolute;
            left: -18px;
            top: 70px;
            width: 20px;
            height: 50px;
            background: #e6e6e6;
            border-radius: 15px 0 0 15px;
            box-shadow: inset 2px 0 5px rgba(0,0,0,0.1);
        }}
        /* Right Ear Nodule */
        .robot-head-outer::after {{
            content: '';
            position: absolute;
            right: -18px;
            top: 70px;
            width: 20px;
            height: 50px;
            background: #e6e6e6;
            border-radius: 0 15px 15px 0;
            box-shadow: inset -2px 0 5px rgba(0,0,0,0.1);
        }}
        /* Black Glass Screen */
        .screen-visor {{
            width: 175px;
            height: 140px;
            background-color: #121314;
            border-radius: 50px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 15px;
            box-shadow: inset 0 0 15px rgba(0,0,0,0.9);
        }}
        .eyes-row {{
            display: flex;
            justify-content: space-around;
            width: 120px;
        }}
        .eye-pixel {{
            width: 32px;
            height: 32px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 0 12px #ffffff;
            animation: blink 4s infinite;
        }}
        .mouth-pixel {{
            background-color: #ffffff;
            box-shadow: 0 0 10px #ffffff;
            transition: all 0.2s ease;
            {mouth_style}
        }}
        @keyframes blink {{
            0%, 90%, 100% {{ transform: scaleY(1); }}
            95% {{ transform: scaleY(0.1); }}
        }}
    </style>
    <div class="robot-stage">
        <div class="robot-head-outer">
            <div class="screen-visor">
                <div class="eyes-row">
                    <div class="eye-pixel"></div>
                    <div class="eye-pixel"></div>
                </div>
                <div class="mouth-pixel"></div>
            </div>
        </div>
    </div>
    """
    st.components.v1.html(html_code, height=280)

# Native browser voice output
def speak_browser(text):
    js_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance({json.dumps(text)});
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# --- DASHBOARD ---
st.title("🤖 White Companion Bot")

# 1. Render Cute 3D White Bot Head
render_robot_face(is_speaking=st.session_state.get("speaking", False))

# 2. Select Detected User
user_option = st.radio("Recognized Profile:", ["Micheal", "Olivia"], horizontal=True)
st.session_state["active_user"] = user_option

# 3. Intelligent Responses
def generate_robot_response(user_input, user_name):
    msg = user_input.lower()
    
    if "hello" in msg or "hi" in msg or "hey" in msg:
        if user_name == "Micheal":
            return "Hey Micheal! Good to see you back at your desk. What are we making today?"
        else:
            return "Hi Olivia! Great to see you! Hope you are having an amazing day!"
            
    elif "how are you" in msg:
        return f"I am feeling awesome, {user_name}! Ready to chat."
        
    elif "remind" in msg or "task" in msg:
        return f"Got it, {user_name}! Saved to desk memory."
        
    elif "bye" in msg:
        return f"Goodbye {user_name}! Have a great day!"
        
    else:
        return f"I heard you say {user_input}, {user_name}!"

# Chat Bar
user_message = st.text_input(f"Talk to your robot ({user_option}):", key="chat_input")

if st.button("Speak to Robot"):
    if user_message:
        reply = generate_robot_response(user_message, user_option)
        st.session_state["speaking"] = True
        st.write(f"🤖 **Robot:** {reply}")
        speak_browser(reply)
