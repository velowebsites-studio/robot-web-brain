import streamlit as st

st.set_page_config(page_title="Desktop Robot", layout="wide", initial_sidebar_state="collapsed")

# Hide Streamlit header/footer for full-screen view
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0px !important;}
        body {background-color: #0f1110;}
    </style>
""", unsafe_allow_html=True)

# Interactive HTML/JS Robot Face with Camera Tracking
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
            font-family: sans-serif;
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

        /* Visor */
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

        .eye {
            width: 42px;
            height: 42px;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 0 15px #ffffff;
            transition: transform 0.05s ease-out;
        }

        .mouth {
            width: 60px;
            height: 10px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 0 12px #ffffff;
            transition: all 0.1s ease;
        }

        .status-text {
            margin-top: 25px;
            font-size: 16px;
            color: #00ffcc;
            text-align: center;
        }

        #webcam {
            display: none; /* Hidden camera element for processing */
        }
    </style>

    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.js" crossorigin="anonymous"></script>
</head>
<body>

    <video id="webcam" autoplay playsinline></video>

    <div class="robot-head" onclick="activateRobot()">
        <div class="visor">
            <div class="eyes-container">
                <div class="eye" id="leftEye"></div>
                <div class="eye" id="rightEye"></div>
            </div>
            <div class="mouth" id="robotMouth"></div>
        </div>
    </div>

    <div class="status-text" id="status">Tap face to enable camera & voice tracking!</div>

    <script>
        let isActivated = false;

        function activateRobot() {
            if (!isActivated) {
                isActivated = true;
                document.getElementById('status').innerText = "Starting camera tracking...";
                speak("Camera tracking enabled! I am watching for your face, Micheal.");
                initCameraTracking();
            }
        }

        function speak(text) {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
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
            document.getElementById('status').innerText = "Tracking your head & expressions live!";
        }

        function onResults(results) {
            if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {
                const landmarks = results.multiFaceLandmarks[0];

                // Nose tip landmark index: 1
                const nose = landmarks[1];

                // Map face position to eye displacement (-15px to 15px)
                // Note: video is mirrored horizontally
                const moveX = (0.5 - nose.x) * 40; 
                const moveY = (nose.y - 0.5) * 40;

                const leftEye = document.getElementById('leftEye');
                const rightEye = document.getElementById('rightEye');
                const mouth = document.getElementById('robotMouth');

                leftEye.style.transform = `translate(${moveX}px, ${moveY}px)`;
                rightEye.style.transform = `translate(${moveX}px, ${moveY}px)`;

                // Track mouth opening landmark gap (Upper lip: 13, Lower lip: 14)
                const upperLip = landmarks[13];
                const lowerLip = landmarks[14];
                const mouthGap = Math.abs(lowerLip.y - upperLip.y);

                if (mouthGap > 0.05) {
                    // Open mouth when user opens mouth/talks
                    mouth.style.height = "25px";
                    mouth.style.borderRadius = "0 0 15px 15px";
                } else {
                    mouth.style.height = "10px";
                    mouth.style.borderRadius = "10px";
                }
            }
        }
    </script>
</body>
</html>
"""

st.components.v1.html(robot_html, height=600)
