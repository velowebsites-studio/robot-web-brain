import streamlit as st

st.set_page_config(page_title="Desktop Robot Companion", layout="wide", initial_sidebar_state="collapsed")

# Hide Streamlit UI elements
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0px !important;}
        body {background-color: #0d0f12;}
    </style>
""", unsafe_allow_html=True)

robot_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #0b0c0e;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Segoe UI', system-ui, sans-serif;
            overflow: hidden;
            color: white;
            user-select: none;
        }

        /* Floating Stage Animation */
        .robot-wrapper {
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            animation: floatHover 3.5s ease-in-out infinite alternate;
        }

        @keyframes floatHover {
            0% { transform: translateY(0px); }
            100% { transform: translateY(-12px); }
        }

        /* Top Antenna */
        .antenna-stem {
            position: absolute;
            top: -28px;
            width: 8px;
            height: 30px;
            background: linear-gradient(180deg, #ffffff, #cccccc);
            border-radius: 4px;
            z-index: 1;
        }

        .antenna-ball {
            position: absolute;
            top: -42px;
            width: 22px;
            height: 22px;
            background-color: #00f0ff;
            border-radius: 50%;
            box-shadow: 0 0 15px #00f0ff;
            z-index: 2;
        }

        /* Floating Hands */
        .hand {
            position: absolute;
            width: 38px;
            height: 55px;
            background: linear-gradient(145deg, #2b2e33, #15171a);
            border: 2px solid #ffffff;
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.5);
            top: 100px;
            transition: all 0.5s cubic-bezier(0.25, 1, 0.5, 1);
            z-index: 3;
        }

        .hand-left {
            left: -48px;
        }

        .hand-right {
            right: -48px;
        }

        /* GESTURE ANIMATIONS */
        /* Scratch Head Gesture */
        .scratch-head .hand-right {
            transform: translateY(-110px) translateX(-35px) rotate(-60deg);
        }

        /* Scratch Side/Itch Gesture */
        .scratch-side .hand-left {
            transform: translateY(30px) translateX(25px) rotate(45deg);
        }

        /* Adjust Visor / Self Check Gesture */
        .check-self .hand-left {
            transform: translateY(-40px) translateX(30px) rotate(20deg);
        }
        .check-self .hand-right {
            transform: translateY(-40px) translateX(-30px) rotate(-20deg);
        }

        /* Main Rounded Egg-Head Chassis */
        .robot-head {
            width: 290px;
            height: 270px;
            background: linear-gradient(145deg, #ffffff, #d8d8d8);
            border-radius: 120px 120px 100px 100px;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            box-shadow: 0 25px 55px rgba(0,0,0,0.7), inset 0 8px 18px #ffffff;
            z-index: 2;
        }

        /* Black Curved Visor */
        .visor {
            width: 240px;
            height: 185px;
            background-color: #0c0d0e;
            border-radius: 75px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 18px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.95), 0 0 5px rgba(255,255,255,0.2);
            position: relative;
        }

        /* Bright Cyan Pixel Eyes */
        .eyes-container {
            display: flex;
            justify-content: space-around;
            width: 150px;
        }

        .eye {
            width: 44px;
            height: 44px;
            background-color: #00f0ff;
            border-radius: 16px;
            box-shadow: 0 0 20px #00f0ff;
            transition: transform 0.08s ease-out, height 0.12s ease;
        }

        .mouth {
            width: 50px;
            height: 10px;
            background-color: #00f0ff;
            border-radius: 10px;
            box-shadow: 0 0 15px #00f0ff;
            transition: all 0.15s ease;
        }

        .status-badge {
            margin-top: 30px;
            padding: 8px 18px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            font-size: 14px;
            color: #00f0ff;
            letter-spacing: 0.5px;
        }

        #webcam {
            display: none;
        }
    </style>

    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.js" crossorigin="anonymous"></script>
</head>
<body>

    <video id="webcam" autoplay playsinline></video>

    <div class="robot-wrapper" id="robotWrapper" onclick="interact()">
        <div class="antenna-ball"></div>
        <div class="antenna-stem"></div>
        <div class="hand hand-left"></div>
        <div class="robot-head">
            <div class="visor">
                <div class="eyes-container">
                    <div class="eye" id="leftEye"></div>
                    <div class="eye" id="rightEye"></div>
                </div>
                <div class="mouth" id="robotMouth"></div>
            </div>
        </div>
        <div class="hand hand-right"></div>
    </div>

    <div class="status-badge" id="status">Tap face to start ultra-realistic bot!</div>

    <script>
        let isActivated = false;
        let currentGesture = "";

        // Randomized Organic Blinking System
        function scheduleBlink() {
            const nextBlink = Math.random() * 3000 + 1500;
            setTimeout(() => {
                triggerBlink();
                scheduleBlink();
            }, nextBlink);
        }

        function triggerBlink() {
            const leftEye = document.getElementById('leftEye');
            const rightEye = document.getElementById('rightEye');

            leftEye.style.height = '4px';
            rightEye.style.height = '4px';

            setTimeout(() => {
                leftEye.style.height = '44px';
                rightEye.style.height = '44px';
            }, 120);
        }

        // Random Organic Hand Gestures (Triggers every 7 - 14 seconds automatically)
        function scheduleRandomGestures() {
            const nextGestureTime = Math.random() * 7000 + 7000;
            setTimeout(() => {
                if (isActivated) {
                    triggerRandomGesture();
                }
                scheduleRandomGestures();
            }, nextGestureTime);
        }

        function triggerRandomGesture() {
            const wrapper = document.getElementById('robotWrapper');
            const gestures = ['scratch-head', 'scratch-side', 'check-self'];
            const randomPick = gestures[Math.floor(Math.random() * gestures.length)];

            wrapper.className = 'robot-wrapper ' + randomPick;

            // Hold gesture for 2.5 seconds then return hands to floating position
            setTimeout(() => {
                wrapper.className = 'robot-wrapper';
            }, 2500);
        }

        function interact() {
            if (!isActivated) {
                isActivated = true;
                document.getElementById('status').innerText = 'Bot Online & Listening';
                speak("Hey Micheal! Systems operational. I'm ready to hang out at your desk.");
                scheduleBlink();
                scheduleRandomGestures();
                initCameraTracking();
                initVoice();
            } else {
                triggerRandomGesture();
                speak("Just adjusting my visor!");
            }
        }

        function speak(text) {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            const mouth = document.getElementById('robotMouth');

            utterance.onstart = () => {
                mouth.style.height = "22px";
                mouth.style.borderRadius = "0 0 15px 15px";
            };
            
            utterance.onend = () => {
                mouth.style.height = "10px";
                mouth.style.borderRadius = "10px";
            };

            window.speechSynthesis.speak(utterance);
        }

        function initCameraTracking() {
            const videoElement = document.getElementById('webcam');

            const faceMesh = new FaceMesh({
                locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`
            });

            faceMesh.setOptions({
                maxNumFaces: 1,
                refineLandmarks: true,
                minDetectionConfidence: 0.5,
                minTrackingConfidence: 0.5
            });

            faceMesh.onResults(onResults);

            const camera = new Camera(videoElement, {
                onFrame: async () => {
                    await faceMesh.send({ image: videoElement });
                },
                width: 640,
                height: 480
            });

            camera.start();
        }

        function onResults(results) {
            if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {
                const landmarks = results.multiFaceLandmarks[0];
                const nose = landmarks[1];

                const moveX = (0.5 - nose.x) * 35;
                const moveY = (nose.y - 0.5) * 35;

                const leftEye = document.getElementById('leftEye');
                const rightEye = document.getElementById('rightEye');

                leftEye.style.transform = `translate(${moveX}px, ${moveY}px)`;
                rightEye.style.transform = `translate(${moveX}px, ${moveY}px)`;
            }
        }

        function initVoice() {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) return;

            const recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = false;

            recognition.onresult = (event) => {
                const last = event.results.length - 1;
                const speech = event.results[last][0].transcript.toLowerCase();

                if (speech.includes('hello') || speech.includes('hi')) {
                    speak("Hey Micheal! How are you doing today?");
                } else if (speech.includes('olivia')) {
                    speak("Hello Olivia! Great to see you!");
                } else {
                    speak("I heard you say " + speech);
                }
            };

            recognition.onend = () => { recognition.start(); };
            recognition.start();
        }
    </script>
</body>
</html>
"""

st.components.v1.html(robot_html, height=650)
