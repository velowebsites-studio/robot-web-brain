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
            background-color: #0d0f12;
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

        /* Robot Stage Container */
        .robot-wrapper {
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
        }

        /* Hands / Arms */
        .arm {
            position: absolute;
            width: 35px;
            height: 100px;
            background: linear-gradient(145deg, #ffffff, #dcdcdc);
            border-radius: 20px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
            top: 110px;
            transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
            z-index: 1;
        }

        .arm-left {
            left: -35px;
            transform-origin: top right;
            transform: rotate(15deg);
        }

        .arm-right {
            right: -35px;
            transform-origin: top left;
            transform: rotate(-15deg);
        }

        /* Hand Checking Self Out Animation */
        .inspecting .arm-left {
            transform: rotate(115deg) translateY(-20px) translateX(10px);
        }
        .inspecting .arm-right {
            transform: rotate(-30deg) translateY(10px);
        }

        /* Sleepy Arms Droop */
        .sleepy .arm-left {
            transform: rotate(5deg) translateY(25px);
        }
        .sleepy .arm-right {
            transform: rotate(-5deg) translateY(25px);
        }

        /* Main Head Chassis */
        .robot-head {
            width: 310px;
            height: 270px;
            background: linear-gradient(145deg, #ffffff, #e0e0e0);
            border-radius: 100px 100px 85px 85px;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            box-shadow: 0 25px 60px rgba(0,0,0,0.7), inset 0 8px 15px #ffffff;
            z-index: 2;
            transition: transform 0.4s ease;
        }

        /* Ear Nodules */
        .robot-head::before {
            content: '';
            position: absolute;
            left: -20px;
            top: 95px;
            width: 22px;
            height: 65px;
            background: #d0d0d0;
            border-radius: 18px 0 0 18px;
        }
        .robot-head::after {
            content: '';
            position: absolute;
            right: -20px;
            top: 95px;
            width: 22px;
            height: 65px;
            background: #d0d0d0;
            border-radius: 0 18px 18px 0;
        }

        /* Visor Screen */
        .visor {
            width: 250px;
            height: 190px;
            background-color: #101214;
            border-radius: 65px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 22px;
            box-shadow: inset 0 0 22px rgba(0,0,0,0.95);
            position: relative;
        }

        .eyes-container {
            display: flex;
            justify-content: space-around;
            width: 160px;
        }

        .eye {
            width: 44px;
            height: 44px;
            background-color: #00f0ff;
            border-radius: 14px;
            box-shadow: 0 0 18px #00f0ff;
            transition: transform 0.08s ease-out, height 0.15s ease, background-color 0.4s ease;
        }

        .mouth {
            width: 55px;
            height: 10px;
            background-color: #00f0ff;
            border-radius: 10px;
            box-shadow: 0 0 14px #00f0ff;
            transition: all 0.2s ease;
        }

        /* Expression Modifiers */
        .bored .eye {
            background-color: #ffaa00;
            box-shadow: 0 0 18px #ffaa00;
            height: 20px;
            border-radius: 6px;
        }

        .bored .mouth {
            background-color: #ffaa00;
            box-shadow: 0 0 14px #ffaa00;
            width: 40px;
            height: 6px;
        }

        .sleepy .eye {
            background-color: #aa55ff;
            box-shadow: 0 0 18px #aa55ff;
            height: 8px;
            border-radius: 4px;
        }

        .sleepy .mouth {
            background-color: #aa55ff;
            box-shadow: 0 0 14px #aa55ff;
            width: 25px;
            height: 12px;
            border-radius: 50%;
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
            transition: color 0.3s ease;
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
        <div class="arm arm-left"></div>
        <div class="robot-head">
            <div class="visor">
                <div class="eyes-container">
                    <div class="eye" id="leftEye"></div>
                    <div class="eye" id="rightEye"></div>
                </div>
                <div class="mouth" id="robotMouth"></div>
            </div>
        </div>
        <div class="arm arm-right"></div>
    </div>

    <div class="status-badge" id="status">Tap face to activate robot!</div>

    <script>
        let isActivated = false;
        let lastInteractionTime = Date.now();
        let currentState = "awake"; // awake, bored, sleepy, inspecting
        let blinkTimeout;

        // Organic Blinking System
        function scheduleBlink() {
            const nextBlink = Math.random() * 3500 + 1500; // Random interval 1.5s - 5s
            blinkTimeout = setTimeout(() => {
                triggerBlink();
                scheduleBlink();
            }, nextBlink);
        }

        function triggerBlink() {
            const leftEye = document.getElementById('leftEye');
            const rightEye = document.getElementById('rightEye');
            
            if (currentState === 'sleepy') return; // Don't blink if eyes are already closed/sleepy

            const origLeftHeight = leftEye.style.height;
            const origRightHeight = rightEye.style.height;

            leftEye.style.height = '4px';
            rightEye.style.height = '4px';

            setTimeout(() => {
                leftEye.style.height = origLeftHeight;
                rightEye.style.height = origRightHeight;
            }, 120);
        }

        // Behavior State Machine (Checks every second)
        setInterval(() => {
            if (!isActivated) return;

            const idleTime = (Date.now() - lastInteractionTime) / 1000;
            const wrapper = document.getElementById('robotWrapper');
            const status = document.getElementById('status');

            if (idleTime > 30 && currentState !== 'sleepy') {
                // Sleepy State
                currentState = 'sleepy';
                wrapper.className = 'robot-wrapper sleepy';
                status.innerText = 'State: Sleepy... (Zzz)';
                status.style.color = '#aa55ff';
                speak("Yawn... Getting a bit sleepy at my desk.");
            } else if (idleTime > 15 && idleTime <= 30 && currentState !== 'bored' && currentState !== 'inspecting') {
                // Bored State / Inspecting self
                currentState = 'inspecting';
                wrapper.className = 'robot-wrapper inspecting';
                status.innerText = 'State: Checking itself out...';
                status.style.color = '#ffaa00';
                
                setTimeout(() => {
                    if (currentState === 'inspecting') {
                        currentState = 'bored';
                        wrapper.className = 'robot-wrapper bored';
                        status.innerText = 'State: Bored (Awaiting user)';
                    }
                }, 4000);
            }
        }, 1000);

        function interact() {
            lastInteractionTime = Date.now();
            const wrapper = document.getElementById('robotWrapper');
            const status = document.getElementById('status');

            if (!isActivated) {
                isActivated = true;
                status.innerText = 'State: Active & Listening';
                speak("Hello Micheal! Systems fully active. Let's build something!");
                scheduleBlink();
                initCameraTracking();
                initVoice();
            } else {
                // Wake up / Reset state
                currentState = 'awake';
                wrapper.className = 'robot-wrapper';
                status.innerText = 'State: Active & Focused';
                status.style.color = '#00f0ff';
                speak("I'm awake and paying attention!");
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
                // Face detected -> Reset idle timer!
                lastInteractionTime = Date.now();

                if (currentState !== 'awake') {
                    currentState = 'awake';
                    document.getElementById('robotWrapper').className = 'robot-wrapper';
                    document.getElementById('status').innerText = 'State: Active (Face Detected)';
                    document.getElementById('status').style.color = '#00f0ff';
                }

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
                lastInteractionTime = Date.now();
                const last = event.results.length - 1;
                const speech = event.results[last][0].transcript.toLowerCase();

                if (speech.includes('hello') || speech.includes('hi')) {
                    speak("Hey Micheal! How are you doing today?");
                } else if (speech.includes('wake up')) {
                    speak("I am wide awake and ready!");
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
