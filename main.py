import cv2
import mediapipe as mp
import numpy as np

# ----------- Angle Calculation -----------
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180:
        angle = 360 - angle
    return angle


# ----------- MediaPipe Setup -----------
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="pose_landmarker.task"),
    running_mode=VisionRunningMode.VIDEO,
    num_poses=1
)

pose = PoseLandmarker.create_from_options(options)

# ----------- Webcam -----------
cap = cv2.VideoCapture(0)

# ----------- Video Recording Setup -----------
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

out = cv2.VideoWriter(
    'knee_rehab_demo.mp4',
    cv2.VideoWriter_fourcc(*'mp4v'),
    20,
    (frame_width, frame_height)
)

counter = 0
stage = None
frame_timestamp = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Process frame
    result = pose.detect_for_video(mp_image, frame_timestamp)
    frame_timestamp += 1

    if result.pose_landmarks:
        landmarks = result.pose_landmarks[0]

        # LEFT leg
        left_hip = [landmarks[23].x, landmarks[23].y]
        left_knee = [landmarks[25].x, landmarks[25].y]
        left_ankle = [landmarks[27].x, landmarks[27].y]

        # RIGHT leg
        right_hip = [landmarks[24].x, landmarks[24].y]
        right_knee = [landmarks[26].x, landmarks[26].y]
        right_ankle = [landmarks[28].x, landmarks[28].y]

        # Choose visible leg
        if landmarks[25].visibility > landmarks[26].visibility:
            hip, knee, ankle = left_hip, left_knee, left_ankle
            leg = "Left"
        else:
            hip, knee, ankle = right_hip, right_knee, right_ankle
            leg = "Right"

        # Calculate angle
        angle = calculate_angle(hip, knee, ankle)

        # Convert to pixel coords
        hip_px = (int(hip[0]*w), int(hip[1]*h))
        knee_px = (int(knee[0]*w), int(knee[1]*h))
        ankle_px = (int(ankle[0]*w), int(ankle[1]*h))

        # Draw lines
        cv2.line(frame, hip_px, knee_px, (255, 255, 255), 2)
        cv2.line(frame, knee_px, ankle_px, (255, 255, 255), 2)

        # Draw joints
        cv2.circle(frame, hip_px, 6, (0, 0, 255), -1)
        cv2.circle(frame, knee_px, 6, (0, 255, 0), -1)
        cv2.circle(frame, ankle_px, 6, (255, 0, 0), -1)

        # ----------- Rep Counter -----------
        if angle > 140:
            stage = "up"

        if angle < 90 and stage == "up":
            stage = "down"
            counter += 1

        # ----------- Feedback -----------
        if angle > 140:
            feedback = "Stand Straight"
        elif angle > 90:
            feedback = "Go Lower"
        else:
            feedback = "Good Position"

        # ----------- Display -----------
        cv2.putText(frame, f'Angle: {int(angle)}',
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(frame, f'Feedback: {feedback}',
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.putText(frame, f'Reps: {counter}',
                    (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.putText(frame, f'Leg: {leg}',
                    (50, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        cv2.putText(frame, "Recording...",
                    (400, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Save frame to video
    out.write(frame)

    cv2.imshow("AI Knee Rehab Analyzer", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()