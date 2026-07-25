import streamlit as st
import json

st.set_page_config(page_title="Desktop Robot", layout="wide", initial_sidebar_state="collapsed")

# Hide Streamlit header, footer, and margins to make the face fill the screen
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0px !important;}
        body {background-color: #0f1110;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Full-screen Interactive Robot Face with Voice & Eye Motion
robot_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #0f1110;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
            color: white;
        }

        .robot-head {
            width: 320px;
            height: 280px;
            background: linear-gradient(145deg, #ffffff, #e6e6e6);
            border-radius: 110px 110px 90px 90px;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            box-shadow: 0 20px 50px rgba(0,0,0,0.6), inset 0 8px 15px #ffffff;
            cursor: pointer;
        }

        /* Ear nodules */
        .robot-head::before {
            content: '';
            position: absolute;
            left: -22px;
            top: 100px;
            width: 25px;
            height: 70px;
            background: #d8d8d8;
            border-radius: 20px 0 0 20px;
        }
        .robot-head::after {
            content: '';
            position: absolute;
            right: -22px;
            top: 100px;
            width: 25px;
            height: 70px;
            background: #d8d8d8;
            border-radius: 0 20px 20px 0;
        }

        /* Screen Visor */
        .visor {
            width: 260px;
            height: 200px;
            background-color: #121314;
            border-radius: 70px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 25px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.9);
            position: relative;
        }

        .eyes-container {
            display: flex;
            justify-content: space-around;
            width: 170px;
        }

        .eye-socket {
            width: 50px;
            height: 50px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .eye {
            width: 42px;
            height: 42px;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 0 15px #ffffff;
            transition: transform 0.1s ease-out;
        }

        .mouth {
            width: 60px;
            height: 10px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 0 12px #ffffff;
            transition: all 0.15s ease;
        }

        .talking {
            animation: speakMouth 0.3s infinite alternate;
        }

        @keyframes speakMouth {
            0% { height: 8px; width: 50px; border-radius: 10px; }
            100% { height: 28px; width: 70px; border-radius: 0 0 20px 20px; }
        }

        .status-text {
            margin-top: 25px;
            font-size: 16px;
            color: #888888;
            text-align: center;
        }
    </style>
</head>
<body>

    <div class="robot-head" onclick="activateRobot()">
        <div class="visor">
            <div class="eyes-container">
                <div class="eye-socket"><div class="eye" id="leftEye"></div></div>
                <div class="eye-socket"><div class="eye" id="rightEye"></div></div>
            </div>
            <div class="mouth" id="robotMouth"></div>
        </div>
    </div>

    <div class="status-text" id="status">Tap the robot head to start audio & listening!</div>

    <script>
        let isActivated = false;

        // Eye Movement Logic (Eyes track touch/cursor)
        document.addEventListener('mousemove', (e) => {
            moveEyes(e.clientX, e.clientY);
        });

        document.addEventListener('touchmove', (e) => {
            if (e.touches.length > 0) {
                moveEyes(e.touches[0].clientX, e.touches[0].clientY);
            }
        });

        function moveEyes(targetX, targetY) {
            const eyes = [document.getElementById('leftEye'), document.getElementById('rightEye')];
            eyes.forEach(eye => {
                const rect = eye.getBoundingClientRect();
                const eyeX = rect.left + rect.width / 2;
                const eyeY = rect.top + rect.height / 2;
                
                const angle = Math.atan2(targetY - eyeY, targetX - eyeX);
                const distance = Math.min(12, Math.hypot(targetX - eyeX, targetY - eyeY) / 15);
                
                const moveX = Math.cos(angle) * distance;
                const moveY = Math.sin(angle) * distance;
                
                eye.style.transform = `translate(${moveX}px, ${moveY}px)`;
            });
        }

        // Tap to Activate Audio & Speech Recognition
        function activateRobot() {
            if (!isActivated) {
                isActivated = true;
                document.getElementById('status').innerText = "Robot Active! Speak to me...";
                speak("Hello Micheal! I am ready. How can I help you at your desk today?");
                startListening();
            }
        }

        // Speak function
        function speak(text) {
            const mouth = document.getElementById('robotMouth');
            mouth.classList.add('talking');

            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            
            utterance.onend = function() {
                mouth.classList.remove('talking');
            };

            window.speechSynthesis.speak(utterance);
        }

        // Voice Listening Function
        function startListening() {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                document.getElementById('status').innerText = "Speech recognition not supported on this browser.";
                return;
            }

            const recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            recognition.onresult = function(event) {
                const last = event.results.length - 1;
                const spokenText = event.results[last][0].transcript.toLowerCase();
                document.getElementById('status').innerText = 'You said: "' + spokenText + '"';

                // Conversational responses
                if (spokenText.includes('hello') || spokenText.includes('hi') || spokenText.includes('hey')) {
                    speak("Hey Micheal! Good to see you!");
                } else if (spokenText.includes('how are you')) {
                    speak("I am feeling great! Everything is working smoothly.");
                } else if (spokenText.includes('olivia')) {
                    speak("Hello Olivia! Hope you are having an awesome day!");
                } else {
                    speak("I heard you say " + spokenText);
                }
            };

            recognition.onerror = function() {
                setTimeout(() => { recognition.start(); }, 1000);
            };

            recognition.onend = function() {
                recognition.start(); // Keep listening automatically
            };

            recognition.start();
        }
    </script>
</body>
</html>
"""

st.components.v1.html(robot_html, height=600)
