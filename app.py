import streamlit as st
import cv2
import numpy as np
import os
import json
from datetime import datetime

st.set_page_config(page_title="Desktop Robot Dashboard", layout="centered")

# Set up storage
USER_DIR = "registered_users"
TASKS_FILE = "tasks.json"

if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)

if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, "w") as f:
        json.dump([], f)

# Initialize session state for user and mouth animation
if "active_user" not in st.session_state:
    st.session_state["active_user"] = "Micheal"

if "is_speaking" not in st.session_state:
    st.session_state["is_speaking"] = False

# Function to render animated CSS Robot Face
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

# Browser native text-to-speech
def speak_browser(text):
    js_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance({json.dumps(text)});
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# --- APP LAYOUT ---
st.title("🤖 Desktop Robot Brain")

# Step 1: Render Animated Robot Face
render_robot_face(is_speaking=st.session_state["is_speaking"])

# Step 2: User Switcher
user_option = st.radio("Active User:", ["Micheal", "Olivia"], horizontal=True)
st.session_state["active_user"] = user_option
current_user = st.session_state["active_user"]

# Step 3: Conversational Chat Interface
st.markdown("---")
st.subheader(f"💬 Chatting with **{current_user}**")

def generate_response(user_input, user_name):
    msg = user_input.lower()
    if "hello" in msg or "hi" in msg or "hey" in msg:
        if user_name == "Micheal":
            return "Hey Micheal! Welcome back to your desk. Ready to get to work?"
        else:
            return "Hi Olivia! Great to see you! Hope you have an awesome day!"
    elif "how are you" in msg:
        return f"I'm doing great, {user_name}! All my circuits are running at 100 percent."
    elif "remind" in msg or "task" in msg or "alarm" in msg:
        return f"Got it, {user_name}! I will keep that saved in my memory for you."
    elif "bye" in msg:
        return f"Goodbye {user_name}! Talk to you soon."
    else:
        return f"I heard you say '{user_input}', {user_name}!"

user_message = st.text_input("Type a message to your robot:", key="chat_input")

if st.button("Send Message"):
    if user_message:
        reply = generate_response(user_message, current_user)
        st.session_state["is_speaking"] = True
        st.write(f"🤖 **Robot:** {reply}")
        speak_browser(reply)

# Step 4: Tasks & Reminders
st.markdown("---")
st.subheader("📅 Task & Reminder Memory")

with open(TASKS_FILE, "r") as f:
    task_list = json.load(f)

new_task = st.text_input("Add a reminder for the desk robot:", placeholder="e.g., Set an alarm for 3 PM")

if st.button("Save Task"):
    if new_task:
        timestamp = datetime.now().strftime("%I:%M %p")
        task_list.append({"user": current_user, "task": new_task, "time": timestamp})
        with open(TASKS_FILE, "w") as f:
            json.dump(task_list, f)
        st.success("Task saved to robot memory!")

if task_list:
    st.write("**Stored Tasks:**")
    for item in task_list:
        st.write(f"- [{item['time']}] **{item['user']}**: {item['task']}")
