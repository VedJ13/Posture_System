import cv2
import mediapipe as mp
import streamlit as st
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
from components.state import get_shared_state

@st.cache_resource
def load_detector():
    opts = vision.PoseLandmarkerOptions(
        base_options=mp_python.BaseOptions(model_asset_path="pose_landmarker_lite.task"),
        running_mode=vision.RunningMode.IMAGE,
    )
    return vision.PoseLandmarker.create_from_options(opts)


class PostureProcessor:
    def recv(self, frame):
        import av

        shared = get_shared_state()

        img = frame.to_ndarray(format="bgr24")

        # Mark camera as active
        with shared["lock"]:
            shared["camera_on"] = True

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        detector = load_detector()

        posture = "No Pose"
        color = (120, 120, 120)
        diff = 0.0

        try:
            result = detector.detect(mp_img)

            if result.pose_landmarks:
                lms = result.pose_landmarks[0]
                h, w, _ = img.shape

                left = lms[11]
                right = lms[12]

                diff = abs(left.y - right.y)

                with shared["lock"]:
                    bad_t = shared["bad_thresh"]
                    warn_t = shared["warn_thresh"]

                if diff > bad_t:
                    posture, color = "Bad Posture", (0, 0, 255)
                elif diff > warn_t:
                    posture, color = "Slightly Bent", (0, 200, 255)
                else:
                    posture, color = "Good Posture", (0, 220, 100)

                # Draw points
                for lm in lms:
                    cv2.circle(img, (int(lm.x * w), int(lm.y * h)), 4, color, -1)

                # Draw shoulder line
                cv2.line(
                    img,
                    (int(left.x * w), int(left.y * h)),
                    (int(right.x * w), int(right.y * h)),
                    color,
                    2,
                )

        except Exception:
            posture = "No Pose"

        # Overlay text
        cv2.rectangle(img, (10, 10), (330, 60), (40, 40, 40), -1)
        cv2.putText(
            img,
            posture,
            (18, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        # Update shared state
        with shared["lock"]:
            shared["posture"] = posture
            shared["last_diff"] = diff

        return av.VideoFrame.from_ndarray(img, format="bgr24")
